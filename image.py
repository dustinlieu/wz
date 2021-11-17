from .binary_reader import BinaryReader
from .property import Property, parse_object

def load_image_from_file(path, key):
	file = open(path, mode="rb")
	reader = BinaryReader(file, key)

	img_type = reader.read_uint_8()
	if img_type == 0x01:
		# TODO
		return None
	elif img_type == 0x73:
		return parse_object(reader)