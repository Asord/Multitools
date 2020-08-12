from ctypes import Structure, c_ushort, c_ubyte, c_short, c_ulong

def struct_dict(struct):
    get_pair = lambda field_type: (
        field_type[0], getattr(struct, field_type[0]))
    return dict(list(map(get_pair, struct._fields_)))

def get_bit_values(number, size=32):
    res = list(gen_bit_values(number))
    res.reverse()
    # 0-pad the most significant bit
    res = [0] * (size - len(res)) + res
    return res

def gen_bit_values(number):
    number = int(number)
    while number:
        yield number & 0x1
        number >>= 1

class XINPUT_GAMEPAD(Structure):
    _fields_ = [
        ('buttons', c_ushort),  # wButtons
        ('left_trigger', c_ubyte),  # bLeftTrigger
        ('right_trigger', c_ubyte),  # bLeftTrigger
        ('l_thumb_x', c_short),  # sThumbLX
        ('l_thumb_y', c_short),  # sThumbLY
        ('r_thumb_x', c_short),  # sThumbRx
        ('r_thumb_y', c_short),  # sThumbRy
    ]

class XINPUT_STATE(Structure):
    _fields_ = [
        ('packet_number', c_ulong),  # dwPacketNumber
        ('gamepad', XINPUT_GAMEPAD),  # Gamepad
    ]

class XINPUT_VIBRATION(Structure):
    _fields_ = [("wLeftMotorSpeed", c_ushort),
                ("wRightMotorSpeed", c_ushort)]

class XINPUT_BATTERY_INFORMATION(Structure):
    _fields_ = [("BatteryType", c_ubyte),
                ("BatteryLevel", c_ubyte)]