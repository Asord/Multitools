from ctypes import windll

JOY_UP = 1
JOY_DOWN = 2
JOY_LEFT = 3
JOY_RIGHT = 4

JOY_START = 5
JOY_BACK = 6

JOY_LT = 7
JOY_RT = 8
JOY_LB = 9
JOY_RB = 10

JOY_A = 13
JOY_B = 14
JOY_X = 15
JOY_Y = 16

JOY_LEFT_TRIGER = "left_trigger"
JOY_RIGHT_TRIGER = "right_trigger"
JOY_LEFT_THUMB_Y = "l_thumb_y"
JOY_LEFT_THUMB_X = "l_thumb_x"
JOY_RIGHT_THUMB_Y = "r_thumb_y"
JOY_RIGHT_THUMB_X = "r_thumb_x"

ERROR_DEVICE_NOT_CONNECTED = 1167
ERROR_SUCCESS = 0

xinput = windll.xinput1_4