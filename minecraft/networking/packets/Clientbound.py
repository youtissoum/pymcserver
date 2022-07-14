from minecraft.networking.packets.Packet import Packet
from minecraft.networking.types.basic import *

### "default" packets
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

### login packets
class EncryptionRequestPacket(Packet):
    packet_id = 0x01
    packet_name = "encryption_request"
    definition: list[tuple[str, Type]] = [
        ('server_ID', String),
        ('pub_key', ByteArray),
        ('verify_token', ByteArray)
    ]