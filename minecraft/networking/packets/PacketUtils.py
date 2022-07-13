from minecraft.networking.packets.Serverbound import *
from minecraft.networking.types.basic import VarInt
from .Packet import Packet

packets: dict[bytes, Packet] = {
    b'\x00': HandShakePacket,
    b'\x01': PingRequestPacket
}

def GetPacket(packet) -> Packet:
    lengthLength = VarInt.getLength(packet)
    parsedPacket = packets[packet[lengthLength:lengthLength+1]]()
    parsedPacket.read(packet)
    return parsedPacket

def GetPacketMaybeCombined(packet) -> list[Packet]:
    lengthLength = VarInt.getLength(packet)
    parsedPacket = packets[packet[lengthLength:lengthLength+1]]()
    otherPacket = parsedPacket.read(packet)
    return [parsedPacket, otherPacket]