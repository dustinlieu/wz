# wz
Python library to parse Maplestory WZ img files

## Usage
```
import wz

key = wz.Key(wz.MAPLESTORY_GMS_IV, wz.MAPLESTORY_KEY_DEFAULT)
obj = wz.load_image_from_file("100000000.img", key)

# obj is a mapping
for k, v in obj.items():
	print(k, v)
```
