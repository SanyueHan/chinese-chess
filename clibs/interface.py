from ctypes import CDLL, c_char_p, c_int


lib = CDLL("/usr/local/lib/is_valid.so")


is_valid = lib.is_valid
is_valid.argtypes = [c_char_p, c_int, c_int]
is_valid.restype = c_int
