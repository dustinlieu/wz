from collections.abc import Mapping

def parse_object(reader, object_type=None):
	if object_type is None:
		object_type = reader.read_wz_string()

	if object_type == "Property":
		return Property(reader, reader.pos())
	elif object_type == "Canvas":
		# TODO
		return None
	elif object_type == "Shape2D#Vector2D":
		# TODO
		return None
	elif object_type == "Shape2D#Convex2D":
		# TODO
		return None
	elif object_type == "Sound_DX8":
		# TODO
		return None
	elif object_type == "UOL":
		return reader.read_wz_uol()
	else:
		return None

class Property(Mapping):
	def __init__(self, reader, pos):
		self._reader = reader
		self._pos = pos
		self._loaded = False

		self._children = {}

	def _load(self):
		self._reader.seek(self._pos + 2)

		entry_count = self._reader.read_wz_int()
		for i in range(entry_count):
			variant_name = self._reader.read_wz_uol()
			variant_type = self._reader.read_wz_int()

			if variant_type == 0x00:
				# Null
				self._children[variant_name] = None
			elif variant_type == 0x02 or variant_type == 0x0B:
				# Int 16
				self._children[variant_name] = self._reader.read_int_16()
			elif variant_type == 0x03 or variant_type == 0x13:
				# Wz int
				self._children[variant_name] = self._reader.read_wz_int()
			elif variant_type == 0x04:
				# Wz float 32
				self._children[variant_name] = self._reader.read_wz_float()
			elif variant_type == 0x05:
				# Float 64
				self._children[variant_name] = self._reader.read_float_64()
			elif variant_type == 0x14:
				# Wz Long
				self._children[variant_name] = self._reader.read_wz_long()
			elif variant_type == 0x08:
				# Wz UOL
				self._children[variant_name] = self._reader.read_wz_uol()
			elif variant_type == 0x09:
				# Object
				end_pos = self._reader.read_uint_32() + self._reader.pos()
				child_object_type = self._reader.read_uint_8()

				if child_object_type == 0x00 or child_object_type == 0x73:
					self._children[variant_name] = parse_object(self._reader)
				elif child_object_type == 0x01 or child_object_type == 0x1B:
					self._children[variant_name] = parse_object(self._reader, object_type=self._reader.read_wz_uol())

				self._reader.seek(end_pos)

	def _ensure_loaded(self):
		if self._loaded:
			return

		self._load()
		self._loaded = True

	def __getitem__(self, key):
		self._ensure_loaded()
		return self._children[key]

	def __iter__(self):
		self._ensure_loaded()
		return iter(self._children)

	def __len__(self):
		self._ensure_loaded()
		return len(self._children)
