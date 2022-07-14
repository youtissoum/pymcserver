import os
import socket
import sys
import threading
from time import sleep
from minecraft.networking.packets.PacketUtils import GetPacket, GetPacketMaybeCombined
from minecraft.networking.packets.Clientbound import *
from minecraft.networking.encryption import *

STATE_STATUS = 1
STATE_LOGIN = 2

DEFAULT_PACKETS = 0
LOGIN_PACKETS = 1

class ServerThread(threading.Thread):
    def __init__(self, port):
        threading.Thread.__init__(self)
        self.port = port
        self.interrupt = False
        self.clientThreads = []

    def run(self):
        self.open_server()

    def open_server(self):
        self.interrupt = False
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.server.bind(('', self.port))
        server = self.server
        print("\x1b[32mserver ready\x1b[0m")
        while self.interrupt == False:
            print("test")
            server.listen(5)
            client, addr = server.accept()
            print(f"new connection : {addr}")
            thread = ClientHandlerThread(client)
            thread.start()
            self.clientThreads.append(thread)

    def close_server(self):
        self.interrupt = True
        for clientThread in self.clientThreads:
            clientThread.close_connection()
            clientThread.join()
        self.server.close()

class ClientHandlerThread(threading.Thread):
    def __init__(self, connection: socket.socket):
        threading.Thread.__init__(self)
        self.client = connection

    def close_connection(self):
        self.client.close()

    def receive(self, state=DEFAULT_PACKETS) -> Packet:
        data = self.client.recv(1024)
        if not data:
            print(f"reception error")
            self.client.close()
            sys.exit()

        print(f"received {data}")

        return GetPacket(data, state)

    def receive_maybe_combined(self, state=DEFAULT_PACKETS):
        data = self.client.recv(1024)
        if not data:
            print(f"reception error")
            self.client.close()
            sys.exit()

        return GetPacketMaybeCombined(data, state)

    def respond(self, packetType: Packet, values: list):
        packet = packetType()
        packet.write(values)
        self.client.send(packet.packet)

    def status_request(self, otherPacket):
        if otherPacket == b'':
            otherPacket = self.client.recv(1024)

        with open('response.json', 'r') as f:
            data = f.read()

        self.respond(StatusResponsePacket, [data])

        packet = self.receive()

        self.respond(PingResponsePacket, [packet.values[0][1]])

    def login(self, otherPacket):
        print(otherPacket)
        if otherPacket == b'':
            otherPacket = self.client.recv(1024)
            print(f"received {otherPacket}")

        self.priv_key, self.pub_key = generate_pub_and_priv_keys()

        verify_token_normal = os.urandom(4)

        print(verify_token_normal)

        print(load_der(self.pub_key))

        self.respond(EncryptionRequestPacket, [
            "",
            load_der(self.pub_key),
            verify_token_normal
        ])

        packet = None
        packet = self.receive(LOGIN_PACKETS)
        
        print(packet.values[1][1])

        print(self.priv_key.decrypt(packet.values[1][1], PKCS1v15()))

        if rsa_decrypt(packet.values[1][1], self.priv_key) != verify_token_normal:
            print(f"cryptography error (verify tokens did not match)")
            self.client.close()
            sys.exit()

        print("cryptography NOT error")

    def run(self):
        packets = self.receive_maybe_combined()
        
        packet = packets[0]
        if packet.packet_name != "handshake":
            print("invalid entry packet")
            self.client.close()
            return

        if packet.values[0][1] != 758:
            print("protocol version invalid")
            self.client.close()
            return

        if packet.values[3][1] == STATE_STATUS:
            self.status_request(packets[1])
            self.client.close()
            return
        elif packet.values[3][1] == STATE_LOGIN:
            print("test")
            self.login(packets[1])
            self.client.close()
            return