import evdev
from evdev import InputDevice, UInput, ecodes, InputEvent
import threading
import time
from createMap import KEYBOARD_REMAP, COMBINATIONS
from pynput.mouse import Button, Controller

mouse = Controller()

hold = {}
modifier_hold = {}

MODIFIERS = [
    ecodes.KEY_LEFTCTRL,
    ecodes.KEY_RIGHTCTRL,
    ecodes.KEY_LEFTSHIFT,
    ecodes.KEY_RIGHTSHIFT,
    ecodes.KEY_LEFTSHIFT,
    ecodes.KEY_RIGHTSHIFT,
    ecodes.KEY_LEFTALT,
    ecodes.KEY_RIGHTALT,
]

def list_keyboard_devices():
    # List all input device paths
    devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
    device_paths = []  
    # Filter and print information about devices that have "keyboard" in their name
    for device in devices:
        if 'keyboard' in device.name.lower():
            # print(f"Device name: {device.name}")
            # print(f"Device path: {device.path}")
            # print(f"Device phys: {device.phys}")
            # print(f"Device info: {device.info}")
            device_paths.append(device.path)
    return device_paths

def custom_event(code, type, val):
    return InputEvent(
        sec=time.time(),
        usec=time.time(),
        type=type,
        code=code,
        value=val
    )

def process_device(input_device_path):
    # Open the input device
    input_device = InputDevice(input_device_path)

    # Grab the input device to stop it from sending events to the system
    input_device.grab()

    # Create a virtual output device with the same capabilities as the input device
    capabilities = input_device.capabilities()
    del capabilities[0]

    output_device = UInput(capabilities, name="virtual_output_device")

    print(f"Listening for events from {input_device_path}...")

    # Dictionary to store the key press times
    store_keys = {}

    # Initialize the hold state and modifier state dictionaries
    hold = {}
    modifier_hold = {}
    threadhold = 0.185 ## in second
    alpha_press = 15 ## in pixel
    alpha_hold = 40  ## in pixel
    try:
        for event in input_device.read_loop():
            current_time = time.time()
            
            if event.type == ecodes.EV_KEY:
                if event.value == 1:  # Key press
                    outer_run = True
                    if event.code in MODIFIERS:
                        modifier_hold[KEYBOARD_REMAP[event.code][1]] = True
                        output_device.write_event(custom_event(KEYBOARD_REMAP[event.code][1],ecodes.EV_KEY,1))
                    for key, value in modifier_hold.items():
                        if value:
                            combination = (key, event.code)
                            if combination in COMBINATIONS:
                                outer_run = False
                                if 'mouse' in str(COMBINATIONS[combination]):
                                    action = COMBINATIONS[combination].split(' ')[1]
                                    try:
                                        if action == 'up':
                                            mouse.move(0, -alpha_press)
                                        elif action == 'down':
                                            mouse.move(0, alpha_press)
                                        elif action == 'left':
                                            mouse.move(-alpha_press, 0)
                                        elif action == 'right':
                                            mouse.move(alpha_press, 0)
                                        elif action == 'leftclick':
                                            mouse.click(Button.left)
                                        elif action == 'rightclick':
                                            mouse.click(Button.right)
                                        elif action == 'scrollup':
                                            mouse.scroll(0, -1)
                                        elif action == 'scrolldown':
                                            mouse.scroll(0, 1)
                                        elif action == 'scrollleft':
                                            mouse.scroll(-1, 0)
                                        elif action == 'scrollright':
                                            mouse.scroll(1, 0)
                                    except Exception as e:
                                        pass
                                else:
                                    output_device.write_event(custom_event(COMBINATIONS[combination],ecodes.EV_KEY,1))
                    if outer_run:
                        store_keys[event.code] = current_time
                        hold[event.code] = 0
                elif event.value == 2:
                    for key, value in modifier_hold.items():
                        if value:
                            combination = (key, event.code)
                            if combination in COMBINATIONS:
                                if 'mouse' in str(COMBINATIONS[combination]):
                                    action = COMBINATIONS[combination].split(' ')[1]
                                    alpha_hold = int(alpha_hold * 1.5)
                                    try:
                                        if action == 'up':
                                            mouse.move(0, -alpha_hold)
                                        elif action == 'down':
                                            mouse.move(0, alpha_hold)
                                        elif action == 'left':
                                            mouse.move(-alpha_hold, 0)
                                        elif action == 'right':
                                            mouse.move(alpha_hold, 0)
                                        elif action == 'leftclick':
                                            mouse.click(Button.left)
                                        elif action == 'rightclick':
                                            mouse.click(Button.right)
                                        elif action == 'scrollup':
                                            mouse.scroll(0, -1)
                                        elif action == 'scrolldown':
                                            mouse.scroll(0, 1)
                                        elif action == 'scrollleft':
                                            mouse.scroll(-1, 0)
                                        elif action == 'scrollright':
                                            mouse.scroll(1, 0)
                                    except Exception as e:
                                        pass
                elif event.value == 0:  # Key release
                    alpha_hold = 15
                    if event.code in MODIFIERS:
                        modifier_hold[KEYBOARD_REMAP[event.code][1]] = False
                        output_device.write_event(custom_event(KEYBOARD_REMAP[event.code][0],ecodes.EV_KEY,0))
                    for key, value in modifier_hold.items():
                        if value:
                            combination = (key, event.code)
                            if combination in COMBINATIONS:
                                if 'mouse' not in str(COMBINATIONS[combination]):
                                    output_device.write_event(custom_event(COMBINATIONS[combination],ecodes.EV_KEY,0))
                    
                    if event.code in store_keys:
                        press_duration = current_time - store_keys[event.code]
                        if press_duration < threadhold:
                            output_device.write_event(custom_event(KEYBOARD_REMAP[event.code][0], ecodes.EV_KEY, 1))
                            output_device.write_event(custom_event(KEYBOARD_REMAP[event.code][0], ecodes.EV_KEY, 0))
                        else:
                            output_device.write_event(custom_event(KEYBOARD_REMAP[event.code][1], ecodes.EV_KEY, 0))
                        del store_keys[event.code]
                output_device.syn()
                
            for key, press_time in store_keys.items():
                if current_time - press_time >= threadhold:
                    output_device.write_event(custom_event(KEYBOARD_REMAP[key][1], ecodes.EV_KEY, 1))
                
    except KeyboardInterrupt:
        print("Program interrupted by user.")
    finally:
        # Ensure all devices are properly released and closed
        input_device.ungrab()
        input_device.close()
        output_device.close()


if __name__ == '__main__':
    threads = []
    for path in list_keyboard_devices():
        thread = threading.Thread(target=process_device, args=(path,))
        thread.start()
        threads.append(thread)
    for thread in threads:
        thread.join()
        
        