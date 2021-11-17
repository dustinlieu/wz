import struct

class BinaryReader:
	def __init__(self, reader, key):
		self.reader = reader
		self.key = key

	def pos(self):
		return self.reader.tell()

	def seek(self, offset):
		self.reader.seek(offset, 0)

	def read_uint_8(self):
		return int.from_bytes(self.reader.read(1), byteorder="little", signed=False)

	def read_uint_16(self):
		return int.from_bytes(self.reader.read(2), byteorder="little", signed=False)

	def read_uint_32(self):
		return int.from_bytes(self.reader.read(4), byteorder="little", signed=False)

	def read_uint_64(self):
		return int.from_bytes(self.reader.read(8), byteorder="little", signed=False)

	def read_int_8(self):
		return int.from_bytes(self.reader.read(1), byteorder="little", signed=True)

	def read_int_16(self):
		return int.from_bytes(self.reader.read(2), byteorder="little", signed=True)

	def read_int_32(self):
		return int.from_bytes(self.reader.read(4), byteorder="little", signed=True)

	def read_int_64(self):
		return int.from_bytes(self.reader.read(8), byteorder="little", signed=True)

	def read_float_32(self):
		return struct.unpack("f", self.reader.read(4))[0]

	def read_float_64(self):
		return struct.unpack("d", self.reader.read(8))[0]

	def read_wz_int(self):
		sb = self.read_int_8()
		if sb == -128:
			return self.read_int_32()
		else:
			return sb

	def read_wz_float(self):
		flag = self.read_uint_8()
		if flag == 0x00:
			return 0
		if flag == 0x80:
			return self.read_float_32()

	def read_wz_long(self):
		sb = self.read_int_8()
		if sb == -128:
			return self.read_int_64()
		else:
			return sb

	def read_wz_string(self):
		length = self.read_int_8()
		if length == 0:
			return

		if length > 0:
			# Unicode
			if length == 127:
				length = self.read_int_32()

			if length <= 0:
				return None

			mask = 0xAAAA
			ret_str = ""

			for i in range(length):
				val = self.read_uint_16()
				val = val ^ (mask + i)
				val = (self.key.at(i * 2 + 1) << 8) + self.key.at(i * 2)
				ret_str += chr(val)

			return ret_str
		elif length < 0:
			# ASCII
			if length == -128:
				length = self.read_int_32()
			else:
				length = -length

			if length <= 0:
				return None

			mask = 0xAA
			ret_str = ""

			for i in range(0, length):
				b = self.read_uint_8()
				b = b ^ (mask + i)
				b = b ^ self.key.at(i)
				ret_str += chr(b)

			return ret_str

	def read_wz_uol(self):
		flag = self.read_uint_8()

		if flag == 0x00 or flag == 0x73:
			return self.read_wz_string()
		elif flag == 0x01 or flag == 0x1B:
			offset = self.read_uint_32()
			
			original_pos = self.pos()
			self.seek(original_pos + offset)
			ret_str = self.read_wz_string()
			self.seek(original_pos)
			return ret_str
		else:
			return ""
