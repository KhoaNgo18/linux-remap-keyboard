from evdev import InputDevice, UInput, ecodes, InputEvent

with open('keys.txt', 'w') as f:
    for x in sorted(ecodes.keys):
        f.write(f'{x}: {ecodes.keys[x]}\n')
        