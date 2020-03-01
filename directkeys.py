# direct inputs
# source to this solution and code:
# http://stackoverflow.com/questions/14489013/simulate-python-keypresses-for-controlling-a-game
# http://www.gamespp.com/directx/directInputKeyboardScanCodes.html

import ctypes
import time
import pynput

SendInput = ctypes.windll.user32.SendInput

#keys
keyList = { '`' : 0x29,'1' : 0x02,'2' : 0x03,'3' : 0x04,'4' : 0x05,'5' : 0x06,'6' : 0x07,'7' : 0x08,'8' : 0x09,'9' : 0x0A,'0' : 0x0B,
            'q' : 0x10,'w' : 0x11,'e' : 0x12,'r' : 0x13,'t' : 0x14,'y' : 0x15,'u' : 0x16,'i' : 0x17,'o' : 0x18,'p' : 0x19,
            'a' : 0x1E,'s' : 0x1F,'d' : 0x20,'f' : 0x21,'g' : 0x22,'h' : 0x23,'j' : 0x24,'k' : 0x25,'l' : 0x26,
            'z' : 0x2C,'x' : 0x2D,'c' : 0x2E,'v' : 0x2F,'b' : 0x30,'n' : 0x31,'m' : 0x32,
            'space' : 0x39,'ctrl' : 0x1D,'control' : 0x1D,'shift' : 0x2A,'capslock' : 0x3A,'caps' : 0x3A,'tab' : 0x0F,'enter' : 0x1C,'backspace' : 0x0E,
            'right' : 0xCD,'up' : 0xC8,'down' : 0xD0,'left' : 0xCB,
            'f1' : 0x3B,'f2' : 0x3C,'f3' : 0x3D,'f4' : 0x3E,'f5' : 0x3F,'f6' : 0x40,'f7' : 0x41,'f8' : 0x42,'f9' : 0x43,'f10' : 0x44,'f11' : 0x57,'f12' : 0x58}

NP_2 = 0x50
NP_4 = 0x4B
NP_6 = 0x4D
NP_8 = 0x48

# C struct redefinitions 
PUL = ctypes.POINTER(ctypes.c_ulong)
class KeyBdInput(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort),
                ("wScan", ctypes.c_ushort),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class HardwareInput(ctypes.Structure):
    _fields_ = [("uMsg", ctypes.c_ulong),
                ("wParamL", ctypes.c_short),
                ("wParamH", ctypes.c_ushort)]

class MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time",ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput),
                 ("mi", MouseInput),
                 ("hi", HardwareInput)]

class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", Input_I)]

# Actuals Functions

def PressKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = pynput._util.win32.INPUT_union()
    ii_.ki = pynput._util.win32.KEYBDINPUT(0, hexKeyCode, 0x0008, 0, ctypes.cast(ctypes.pointer(extra), ctypes.c_void_p))
    x = pynput._util.win32.INPUT(ctypes.c_ulong(1), ii_)
    SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

def ReleaseKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = pynput._util.win32.INPUT_union()
    ii_.ki = pynput._util.win32.KEYBDINPUT(0, hexKeyCode, 0x0008 | 0x0002, 0, ctypes.cast(ctypes.pointer(extra), ctypes.c_void_p))
    x = pynput._util.win32.INPUT(ctypes.c_ulong(1), ii_)
    SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

if __name__ == '__main__':
    time.sleep(2)
    PressKey(0x11)
    time.sleep(1)
    ReleaseKey(0x11)
    time.sleep(1)