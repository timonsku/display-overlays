import board
import busio
import time
from adafruit_bus_device.i2c_device import I2CDevice
from adafruit_extended_bus import ExtendedI2C as I2C
import adafruit_24lc32

i2c = I2C(6)

# EEPROM I2C address and start offset
eeprom_address = 0x50

ICN6211_OFFSET = 0x400  # start ICN config at 0x400 (1K)
ICN6211_CONFIG = bytes([
  0x00, 0xc1,
  0x01, 0x62,
  0x02, 0x11,
  0x03, 0xff,
  0x08, 0x00,
  0x09, 0x10,
  0x10, 0x30,
  0x11, 0x88,
  0x14, 0x83,
  0x20, 0xd0,
  0x21, 0xd0,
  0x22, 0x22,
  0x23, 0x2e,
  0x24, 0x2c,
  0x25, 0x02,
  0x26, 0x00,
  0x27, 0x10,
  0x28, 0x02,
  0x29, 0x12,
  0x2a, 0x01,
  0x31, 0x78,
  0x32, 0x04,
  0x33, 0xff,
  0x34, 0x80,
  0x35, 0x08,
  0x36, 0x2e,
  0x51, 0x20,
  0x56, 0x92,
  0x63, 0xff,
  0x64, 0x00,
  0x65, 0x00,
  0x66, 0x00,
  0x67, 0x00,
  0x68, 0x00,
  0x69, 0x03,
  0x6a, 0x00,
  0x6b, 0x31,
  0x7a, 0x3e,
  0x7b, 0xff,
  0x7c, 0xf1,
  0x7d, 0x01,
  0x80, 0x00,
  0x81, 0x00,
  0x84, 0x01,
  0x85, 0x00,
  0x86, 0x28,
  0x87, 0x00,
  0x90, 0x05,
  0x91, 0x0a,
  0x92, 0x18,
  0x94, 0x0d,
  0x95, 0x04,
  0x96, 0x64,
  0x97, 0x00,
  0x99, 0x05,
  0x9a, 0x96,
  0xb5, 0xa0,
  0xb6, 0x20,
  0xFF, 0xFF # end
])

eeprom = adafruit_24lc32.EEPROM_I2C(i2c)

print("Found EEPROM of size: {}".format(len(eeprom)))
#print("Erasing...")
#for i in range(len(eeprom)):
#    eeprom[i] = 0xFF
#print("Done!")

def write_and_verify(offset, data_to_write):
  data_length = len(data_to_write)
  for i in range(0, data_length):
    eeprom[offset + i] = data_to_write[i]
  print("Done!")

  for i in range(0, data_length):
    if eeprom[offset + i][0] != data_to_write[i]:
        raise RuntimeError(f"Mismatch at address {offset + i}: {eeprom[offset + i][0]} != {data_to_write[i]}")

def pretty_print_eeprom(eeprom):
    previous_all_ff = False
    for i in range(0, len(eeprom), 16):
        line_data = eeprom[i:i+16]
        current_all_ff = all(byte == 0xFF for byte in line_data)

        # Only print the line if it's not all FFs or the previous line was not all FFs
        if not current_all_ff or not previous_all_ff or (i + 16 >= len(eeprom)):
            if previous_all_ff or (i + 16 >= len(eeprom)): print("...")
            hex_values = ' '.join(f'{byte:02X}' for byte in line_data)
            print(f'{i:04X}: {hex_values}')
        previous_all_ff = current_all_ff

print("Writing ICN6211 config data...")
write_and_verify(ICN6211_OFFSET, ICN6211_CONFIG)
print("Data verified successfully!")

# Call the pretty print function
pretty_print_eeprom(eeprom)
