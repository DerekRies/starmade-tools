"""
Modified version of the sample code provided by Zippoxer on stackoverflow
stackoverflow.com/questions/442188/readint-readbyte-readstring-etc-in-python/

Using Big-Endian because that's what the Java library uses.
"""

import utils

from struct import *


class BinaryStream:

    def __init__(self, base_stream):
        self.base_stream = base_stream

    def readByte(self):
        return self.base_stream.read(1)

    def readBytes(self, length):
        return self.base_stream.read(length)

    def readChar(self):
        return self.unpack('>b')

    def readUChar(self):
        return self.unpack('>B')

    def readBool(self):
        return self.unpack('>?')

    def readInt16(self):
        return self.unpack('>h', 2)

    def readUInt16(self):
        return self.unpack('>H', 2)

    def readInt32(self):
        return self.unpack('>i', 4)

    def readUInt32(self):
        return self.unpack('>I', 4)

    def readInt64(self):
        return self.unpack('>q', 8)

    def readUInt64(self):
        return self.unpack('>Q', 8)

    def readFloat(self):
        return self.unpack('>f', 4)

    def readDouble(self):
        return self.unpack('>d', 8)

    def readString(self):
        length = self.readUInt16()
        return self.unpack(str(length) + 's', length)

    def readNBytesAsBits(self, nbytes):
        bits = ''
        for i in xrange(nbytes):
            byte = self.readChar()
            byte_as_bits = utils.bits(byte, 8)
            bits += byte_as_bits
        return bits

    def readVec3F(self):
        return (self.readFloat(), self.readFloat(), self.readFloat())

    def readVec3UInt16(self):
        return (self.readUInt16(), self.readUInt16(), self.readUInt16())

    def readVec3Int16(self):
        return (self.readInt16(), self.readInt16(), self.readInt16())

    def readVec3UInt32(self):
        return (self.readUInt32(), self.readUInt32(), self.readUInt32())

    def readVec3Int32(self):
        return (self.readInt32(), self.readInt32(), self.readInt32())

    def writeBytes(self, value):
        self.base_stream.write(value)

    def writeChar(self, value):
        self.pack('>b', value)

    def writeUChar(self, value):
        self.pack('>B', value)

    def writeBool(self, value):
        self.pack('>?', value)

    def writeInt16(self, value):
        self.pack('>h', value)

    def writeUInt16(self, value):
        self.pack('>H', value)

    def writeInt32(self, value):
        self.pack('>i', value)

    def writeUInt32(self, value):
        self.pack('>I', value)

    def writeInt64(self, value):
        self.pack('>q', value)

    def writeUInt64(self, value):
        self.pack('>Q', value)

    def writeFloat(self, value):
        self.pack('>f', value)

    def writeDouble(self, value):
        self.pack('>d', value)

    def writeString(self, value):
        length = len(value)
        self.writeUInt16(length)
        self.pack(str(length) + 's', value)

    def writeVec3F(self, vec):
        self.writeFloat(vec[0])
        self.writeFloat(vec[1])
        self.writeFloat(vec[2])

    def writeVec3UInt16(self, vec):
        self.writeUInt16(vec[0])
        self.writeUInt16(vec[1])
        self.writeUInt16(vec[2])

    def writeVec3Int16(self, vec):
        self.writeInt16(vec[0])
        self.writeInt16(vec[1])
        self.writeInt16(vec[2])

    def writeVec3UInt32(self, vec):
        self.writeUInt32(vec[0])
        self.writeUInt32(vec[1])
        self.writeUInt32(vec[2])

    def writeVec3Int32(self, vec):
        self.writeInt32(vec[0])
        self.writeInt32(vec[1])
        self.writeInt32(vec[2])

    def pack(self, fmt, data):
        return self.writeBytes(pack(fmt, data))

    def unpack(self, fmt, length=1):
        return unpack(fmt, self.readBytes(length))[0]


class BitPacker:
    """
    Convenience for packing bits that can later be writen as bytes
    """
    def __init__(self):
        self.bits = ''

    def pack(self, value, bits):
        self.bits += utils.bits(value, bits)

    def get_bytes(n):
        return [int(bs, 2) for bs in utils.split_every_nchars(self.bits, 8)]

    def write(self, stream):
        for bit_string in utils.split_every_nchars(self.bits, 8):
            byte = int(bit_string, 2)
            stream.writeUChar(byte)
