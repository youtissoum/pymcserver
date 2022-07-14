import struct
from minecraft.networking.types.basic import Type, VarInt

class Packet(object):
    packet_id = 0xFF
    packet_name = "RAW_PACKET"
    definition: list[tuple[str, Type]] = []
    values: list[tuple[str, any]] = []

    packet = b""

    def __init__(self):
       pass

    def read(self, packet):
        self.packet = packet

        packet_length = VarInt.read(packet)
        packet_length_length = VarInt.getLength(packet)
        value_to_return = None
        print(packet_length)
        print(len(packet))
        if packet_length < len(packet)-2:
            print("test")
            combined_packet = packet[packet_length+1:]
            packet = packet[:packet_length+1]
            value_to_return = combined_packet
        
        presumedPacketId = int.from_bytes(packet[packet_length_length:packet_length_length+1], byteorder="big")

        if presumedPacketId != self.packet_id:
            print("Packet is not correct")
            return

        packet = packet[packet_length_length+1:]

        print(packet)

        self.values = []

        for normalValue in self.definition:
            value = normalValue[1].read(packet)
            self.values.append((normalValue[0], value))

            valueLength = normalValue[1].getLength(packet)
            packet = packet[valueLength:]

        return value_to_return

    def write(self, values: list):
        if len(values) != len(self.definition):
            print("wrong length")
            return

        packet = struct.pack(">B", self.packet_id)

        values_to_write: list[tuple[Type, any]] = []

        i = 0
        for value in values:
            values_to_write.append((self.definition[i][1], value))

            i += 1

        for value in values_to_write:
            packet += value[0].write(value[1])

        packet = VarInt.write(len(packet)) + packet

        print(f"sent {packet}")

        self.packet = packet