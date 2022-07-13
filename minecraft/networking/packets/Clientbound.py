from minecraft.networking.packets.Packet import Packet
from minecraft.networking.types.basic import *

class StatusResponsePacket(Packet):
    packet_id = 0x00
    packet_name = "status_response"
    definition = [
        ('json_response', String)
    ]

class PingResponsePacket(Packet):
    packet_id = 0x01
    packet_name = "ping_response",
    definition = [
        ('payload', Long)
    ]