from minecraft.networking.packets.Packet import Packet
from minecraft.networking.types.basic import *

class HandShakePacket(Packet):
    packet_id = 0x00
    packet_name = "handshake"
    definition = [
        ('protocol_version', VarInt),
        ('server_address', String),
        ('server_port', UShort),
        ('next_state', VarInt)
    ]

# Ping Packet
class PingRequestPacket(Packet):
    packet_id = 0x01
    packet_name = "ping_request"
    definition = [
        ('payload', Long)
    ]