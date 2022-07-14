from minecraft.networking.packets.Packet import Packet
from minecraft.networking.types.basic import *

### "default" packets
class HandShakePacket(Packet):
    packet_id = 0x00
    packet_name = "handshake"
    definition = [
        ('protocol_version', VarInt),
        ('server_address', String),
        ('server_port', UShort),
        ('next_state', VarInt)
    ]

class PingRequestPacket(Packet):
    packet_id = 0x01
    packet_name = "ping_request"
    definition = [
        ('payload', Long)
    ]


### login packets
class LoginStartPacket(Packet):
    packet_id = 0x00
    packet_name = "login_start"
    definition: list[tuple[str, Type]] = [
        ('username', String)
    ]

class EncryptionResponsePacket(Packet):
    packet_id = 0x01
    packet_name = "encryption_response"
    definition: list[tuple[str, Type]] = [
        ('shared_secret', ByteArray),
        ('verify_token', ByteArray)
    ]