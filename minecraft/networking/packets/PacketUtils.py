from minecraft.networking.packets.Serverbound import *
from minecraft.networking.types.basic import VarInt
from .Packet import Packet

STATE_DEFAULT = 0
STATE_LOGIN = 1

default_packets: dict[bytes, Packet] = {
    b'\x00': HandShakePacket,
    b'\x01': PingRequestPacket
}

login_packets: dict[bytes, Packet] = {
    b'\x00': LoginStartPacket,
    b'\x01': EncryptionResponsePacket
}

states = [
    default_packets,
    login_packets
]

def GetPacket(packet, state=STATE_DEFAULT) -> Packet:
    lengthLength = VarInt.getLength(packet)
    parsedPacket: Packet = states[state][packet[lengthLength:lengthLength+1]]()
    parsedPacket.read(packet)
    return parsedPacket

def GetPacketMaybeCombined(packet, state=STATE_DEFAULT) -> list[Packet]:
    lengthLength = VarInt.getLength(packet)
    parsedPacket: Packet = states[state][packet[lengthLength:lengthLength+1]]()
    otherPacket = parsedPacket.read(packet)
    return [parsedPacket, otherPacket]