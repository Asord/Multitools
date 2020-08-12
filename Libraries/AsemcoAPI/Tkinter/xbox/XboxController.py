from ctypes import byref, c_uint, POINTER, sizeof

from operator import itemgetter
from itertools import count, starmap
from pyglet.event import EventDispatcher


class XboxController(EventDispatcher):
    max_devices = 4

    def __init__(self, device_number, normalize_axes=True):

        self.device_number = device_number
        self.normalize_axes = normalize_axes

        super(XboxController, self).__init__()

        self._last_state = self.get_state()
        self.received_packets = 0
        self.missed_packets = 0

        # Set the method that will be called to normalize
        #  the values for analog axis.
        choices = [self.translate_identity, self.translate_using_data_size]
        self.translate = choices[normalize_axes]

    @staticmethod
    def translate_using_data_size( value, data_size):
        # normalizes analog data to [0,1] for unsigned data
        #  and [-0.5,0.5] for signed data
        data_bits = 8 * data_size
        return float(value) / (2 ** data_bits - 1)

    @staticmethod
    def translate_identity( value, data_size=None):
        return value

    def get_state(self):

        state = XINPUT_STATE()
        res = xinput.XInputGetState(self.device_number, byref(state))
        if res == ERROR_SUCCESS:
            return state
        if res != ERROR_DEVICE_NOT_CONNECTED:
            raise RuntimeError(
                "Unknown error %d attempting to get state of device %d" % (res, self.device_number))
        # else return None (device is not connected)

    def is_connected(self):
        return self._last_state is not None

    @staticmethod
    def enumerate_devices():

        devices = list(
            map(XboxController, list(range(XboxController.max_devices))))
        return [d for d in devices if d.is_connected()]

    def set_vibration(self, left_motor, right_motor):

        # Set up function argument types and return type
        XInputSetState = xinput.XInputSetState
        XInputSetState.argtypes = [c_uint, POINTER(XINPUT_VIBRATION)]
        XInputSetState.restype = c_uint

        vibration = XINPUT_VIBRATION(
            int(left_motor * 65535), int(right_motor * 65535))
        XInputSetState(self.device_number, byref(vibration))

    def get_battery_information(self):

        BATTERY_DEVTYPE_GAMEPAD = 0x00
        BATTERY_DEVTYPE_HEADSET = 0x01

        XInputGetBatteryInformation = xinput.XInputGetBatteryInformation
        XInputGetBatteryInformation.argtypes = [c_uint, c_ubyte, POINTER(XINPUT_BATTERY_INFORMATION)]
        XInputGetBatteryInformation.restype = c_uint

        battery = XINPUT_BATTERY_INFORMATION(0,0)
        XInputGetBatteryInformation(self.device_number, BATTERY_DEVTYPE_GAMEPAD, byref(battery))

        batt_type = "Unknown" if battery.BatteryType == 0xFF else ["Disconnected", "Wired", "Alkaline","Nimh"][battery.BatteryType]
        level = ["Empty", "Low", "Medium", "Full"][battery.BatteryLevel]
        return batt_type, level

    def update_packet_count(self, state):

        self.received_packets += 1
        missed_packets = state.packet_number - \
                         self._last_state.packet_number - 1
        if missed_packets:
            self.dispatch_event('on_missed_packet', missed_packets)
        self.missed_packets += missed_packets

    def handle_changed_state(self, state):

        self.dispatch_event('on_state_changed', state)
        self.dispatch_axis_events(state)
        self.dispatch_button_events(state)

    def dispatch_events(self):
        state = self.get_state()
        if not state:
            raise RuntimeError(
                "Joystick %d is not connected" % self.device_number)
        if state.packet_number != self._last_state.packet_number:
            self.update_packet_count(state)
            self.handle_changed_state(state)

        self._last_state = state

    def dispatch_axis_events(self, state):
        # axis fields are everything but the buttons
        axis_fields = dict(XINPUT_GAMEPAD._fields_)
        axis_fields.pop('buttons')
        for axis, type in list(axis_fields.items()):
            old_val = getattr(self._last_state.gamepad, axis)
            new_val = getattr(state.gamepad, axis)
            data_size = sizeof(type)
            old_val = self.translate(old_val, data_size)
            new_val = self.translate(new_val, data_size)

            if (axis == 'right_trigger' or axis == 'left_trigger' or
                new_val > 0.08000000000000000 or new_val < -0.08000000000000000):
                self.dispatch_event('on_axis', axis, new_val)

    def dispatch_button_events(self, state):

        changed = state.gamepad.buttons ^ self._last_state.gamepad.buttons
        changed = get_bit_values(changed, 16)
        buttons_state = get_bit_values(state.gamepad.buttons, 16)
        changed.reverse()
        buttons_state.reverse()
        button_numbers = count(1)
        changed_buttons = list(
            filter(itemgetter(0), list(zip(changed, button_numbers, buttons_state))))
        tuple(starmap(self.dispatch_button_event, changed_buttons))

    def dispatch_button_event(self, changed, number, pressed):
        self.dispatch_event('on_button', number, pressed)

    def on_state_changed(self, state):
        pass

    def on_axis(self, axis, value):
        pass

    def on_button(self, button, pressed):
        pass

    def on_missed_packet(self, number):
        pass

list(map(XboxController.register_event_type, [
    'on_state_changed',
    'on_axis',
    'on_button',
    'on_missed_packet',
]))