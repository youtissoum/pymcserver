from io import BytesIO
import math
from operator import length_hint
import struct

class Type(object):
    @staticmethod
    def read(value: bytes):
        raise NotImplementedError("Value reading not implemented yet")

    @staticmethod
    def write(value):
        raise NotImplementedError("Value writing not implemented yet")

    @staticmethod
    def getLength(value: bytes):
        raise NotImplementedError("Length reading not implemented yet")

class UShort(Type):
    @staticmethod
    def read(value: bytes):
        return struct.unpack(">H", value[:2])[0]

    @staticmethod
    def write(value):
        return struct.pack(">H", value)

    @staticmethod
    def getLength(value: bytes):
        return 2

class Long(Type):
    @staticmethod
    def read(value: bytes):
        return struct.unpack(">q", value[:8])[0]

    @staticmethod
    def write(value):
        return struct.pack(">q", value)

    @staticmethod
    def getLength(value: bytes):
        return 8

class ByteArray(Type):
    @staticmethod
    def read(value: bytes):
        array_length, array_length_length = VarInt.read_and_length(value)
        return value[array_length_length:array_length_length+array_length]

    @staticmethod
    def write(value):
        length = VarInt.write(len(value))

        return length + value

    @staticmethod
    def getLength(value: bytes):
        array_length, array_length_length = VarInt.read_and_length(value)

        return array_length + array_length_length

class String(Type):
    @staticmethod
    def read(value):
        string_length, string_length_length = VarInt.read_and_length(value)
        return value[string_length_length:string_length_length+string_length].decode('utf-8')

    @staticmethod
    def write(value: str):
        length_int = len(value)
        length_varint = VarInt.write(length_int)

        if length_int < 1:
            return b'\x01\x00'
        else:
            return length_varint + value.encode('utf-8')

    @staticmethod
    def getLength(value):
        string_length, string_length_length = VarInt.read_and_length(value)

        return string_length + string_length_length

class VarInt(Type):
    @staticmethod
    def _byte(b):
        return bytes((b, ))

    @staticmethod
    def read(value):
        return VarInt.read_buf(BytesIO(value))

    @staticmethod
    def read_buf(stream):
        shift = 0
        result = 0
        while True:
            i = VarInt._read_one(stream)
            result |= (i & 0x7f) << shift
            shift += 7
            if not (i & 0x80):
                break

        return result

    @staticmethod
    def write(value):
        buf = b''
        while True:
            towrite = value & 0x7f
            value >>= 7
            if value:
                buf += VarInt._byte(towrite | 0x80)
            else:
                buf += VarInt._byte(towrite)
                break
        return buf

    @staticmethod
    def getLength(value):
        stream = BytesIO(value)

        shift = 0
        result = 0
        while True:
            i = VarInt._read_one(stream)
            result |= (i & 0x7f) << shift
            shift += 7
            if not (i & 0x80):
                break

        return math.floor(shift / 7)

    @staticmethod
    def _read_one(stream):
        c = stream.read(1)
        if c == b'':
            raise EOFError("Unpexpected EOF while reading bytes")
        return ord(c)

    @staticmethod
    def read_and_length(value):
        return((VarInt.read(value), VarInt.getLength(value)))