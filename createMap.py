import os
from evdev import InputDevice, UInput, ecodes, InputEvent

keys = ecodes.keys

KEYBOARD_REMAP = {}

for key, value in keys.items():
    ##############[key] = [press, hold]
    KEYBOARD_REMAP[key] = [key, key]

def changeKey(key, press, hold=None):
    if hold is None:
        hold = press
    KEYBOARD_REMAP[key] = [press, hold]

### left-key
changeKey(ecodes.KEY_A, ecodes.KEY_A, ecodes.KEY_LEFTCTRL)
changeKey(ecodes.KEY_S, ecodes.KEY_S, ecodes.KEY_LEFTSHIFT)
changeKey(ecodes.KEY_D, ecodes.KEY_D, ecodes.KEY_LEFTALT)
changeKey(ecodes.KEY_F, ecodes.KEY_F, ecodes.KEY_LEFTMETA)

### right-key
changeKey(ecodes.KEY_SEMICOLON, ecodes.KEY_SEMICOLON, ecodes.KEY_RIGHTCTRL)
changeKey(ecodes.KEY_L, ecodes.KEY_L, ecodes.KEY_RIGHTSHIFT)
changeKey(ecodes.KEY_K, ecodes.KEY_K, ecodes.KEY_RIGHTALT)
changeKey(ecodes.KEY_J, ecodes.KEY_J, ecodes.KEY_LEFTMETA)

### left-modifiers
changeKey(ecodes.KEY_LEFTCTRL, ecodes.KEY_MACRO1, ecodes.KEY_MACRO1)
changeKey(ecodes.KEY_LEFTALT, ecodes.KEY_MACRO2, ecodes.KEY_MACRO2)
changeKey(ecodes.KEY_LEFTSHIFT, ecodes.KEY_MACRO3, ecodes.KEY_MACRO3) 

### right-modifiers
changeKey(ecodes.KEY_RIGHTCTRL, ecodes.KEY_MACRO4, ecodes.KEY_MACRO4)
changeKey(ecodes.KEY_RIGHTALT, ecodes.KEY_ESC, ecodes.KEY_ESC)
changeKey(ecodes.KEY_RIGHTSHIFT, ecodes.KEY_MACRO6, ecodes.KEY_MACRO6)



COMBINATIONS = {
    (ecodes.KEY_MACRO1, ecodes.KEY_J): ecodes.KEY_VOLUMEDOWN,
    (ecodes.KEY_MACRO1, ecodes.KEY_K): ecodes.KEY_VOLUMEUP,
    
    (ecodes.KEY_MACRO2, ecodes.KEY_SPACE): ecodes.KEY_BACKSPACE,
    (ecodes.KEY_MACRO2, ecodes.KEY_H): 'mouse left',
    (ecodes.KEY_MACRO2, ecodes.KEY_L): 'mouse right',
    (ecodes.KEY_MACRO2, ecodes.KEY_J): 'mouse down',
    (ecodes.KEY_MACRO2, ecodes.KEY_K): 'mouse up',
    (ecodes.KEY_MACRO2, ecodes.KEY_N): 'mouse leftclick',
    (ecodes.KEY_MACRO2, ecodes.KEY_M): 'mouse rightclick', 
    (ecodes.KEY_MACRO2, ecodes.KEY_I): 'mouse scrolldown',  
    (ecodes.KEY_MACRO2, ecodes.KEY_U): 'mouse scrollup', 
    (ecodes.KEY_MACRO2, ecodes.KEY_Y): 'mouse scrollleft',  
    (ecodes.KEY_MACRO2, ecodes.KEY_O): 'mouse scrollright', 
    
    (ecodes.KEY_MACRO3, ecodes.KEY_H): ecodes.KEY_LEFT,
    (ecodes.KEY_MACRO3, ecodes.KEY_L): ecodes.KEY_RIGHT,
    (ecodes.KEY_MACRO3, ecodes.KEY_J): ecodes.KEY_DOWN,
    (ecodes.KEY_MACRO3, ecodes.KEY_K): ecodes.KEY_UP,
    (ecodes.KEY_MACRO3, ecodes.KEY_SPACE): ecodes.KEY_DELETE,
    
}

