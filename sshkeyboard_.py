"""Sends IR codes in response to keyboard inputs over SSH

This module demonstrates how to use the IR tools to send IR codes to 
a Lego(c) RC using Power Functions. It provides mechanisms to select
a tool and a Power Functions modes. Both are set in the config.json 
file.

Functions:
    def get_config(config_file_name: str) -> dict

    get_maps_config(maps_config_file_name: str) -> dict

    start_listen() -> None

    on_press(key: str) -> bool

    on_release(key: str) -> bool

Attributes:
    rc_encoder (ComboPWM, ComboDirect, Extended, SinglePWM,
        or SingleOther): object that encodes actions into keycodes
        and scancodes.
        
    remote_tx (IR_ir_ctl, IR_LIRC, IR_PiIR, or IR_RPiGPIO): Object that
        controls the IR tool, sends commands via IR.

    kb (Keyboard): Object that maps buttons to actions using
        buttonmaps.

    RC_MODES (dict): Maps PowerFunctions mode acronyms to their
        verbose equivalent (e.g., 'DIR' : 'combo_direct')

    CONFIG (dict): Dictionary where the config.json file is loaded.

    RC_MODE (str): Stores the PowerFunctions mode. 
        Acronym (DIR, PWM, EXT, SGL, OTH). Loaded from 'config.json'.

    GPIO (int): Stores GPIO pin number. Loaded from 'config.json'.

    SYSTEM_MODE (str): KEY, RAW, or HEX. The type of command sent.
        KEY: commands are in key form (e.g., 'FW2_RV1'). 
        RAW: commands are integer scancodes (e.g., 1234, 0x422B, 0b...)
            Only PiIR and RPiGPIO tools.
        HEX: commands are hexadecimal strings (e.g., '422B').
            Only PiIR and RPiGPIO tools.
        Loaded from 'config.json'.

    IR_TOOL (str): Lowercase (ir_ctl, lirc, piir, rpigpio).
        Loaded from 'config.json'.

    MAPS_CONFIG (dict): Dictionary where the maps_config.json file
        is loaded. The maps config includes configuration elements 
        to find the buttonmap and keymap files. 

    REMOTE_KEYMAP_FOLDER_NAME (str): Folder where keymap is located
        Loaded from 'config_maps.json'. 

    REMOTE_KEYMAP_FILE_NAME (str): Name of the keymap file
        Loaded from 'config_maps.json'.

    button_maps_file_name (str): Name of the file that contains the
        button mapping. Loaded from 'config_maps.json'.

Raises:
    Exception: ERR_SSHKeyboard010: No Remote Mode

    Exception: ERR_SSHKeyboard_020: No IR Tool

    Exception: ERR_SSHKeyboard_025: No SYSTEM MODE
"""

from sshkeyboard import listen_keyboard, stop_listening
import json

# SYSTEM MODES:
# * SCAN = scancodes
# * KEY  = keycodes

# IR TOOLS:
# * piir = PiIR
# * rpigpio = RPiGPIO
# * lirc = LIRC
# * ir_ctl = ir-ctl

RC_MODES = {
    'DIR' : 'combo_direct',
    'PWM' : 'combo_pwm',
    'SGL' : 'single_pwm',
    'OTH' : 'single_other',
    'EXT' : 'extended'
}



def get_config(config_file_name: str) -> dict:
    """Load and return config file as a directory"""
    with open(config_file_name, 'r') as config_file:
        config = json.loads(config_file.read())
    return config


def get_maps_config(maps_config_file_name: str) -> dict:
    """Load and return maps_config_file file as a directory"""
    with open(maps_config_file_name, 'r') as maps_config_file:
        maps_config = json.loads(maps_config_file.read())
    return maps_config


CONFIG = get_config('config.json')

MAPS_CONFIG = get_maps_config(CONFIG['maps_config_file'])

## Set up RC Mode
RC_MODE = CONFIG['rc_mode']
if CONFIG['rc_mode'] == 'PWM':
    import power_functions_encoders.combo_pwm as pf
    rc_encoder = pf.ComboPWM()
elif CONFIG['rc_mode'] == 'DIR':
    import power_functions_encoders.combo_direct as pf
    rc_encoder = pf.ComboDirect()
elif CONFIG['rc_mode'] == 'SGL':
    import power_functions_encoders.single_pwm as pf
    rc_encoder = pf.SinglePWM()
elif CONFIG['rc_mode'] == 'OTH':
    import power_functions_encoders.single_other as pf
    rc_encoder = pf.SingleOther()
elif CONFIG['rc_mode'] == 'EXT':
    import power_functions_encoders.extended as pf
    rc_encoder = pf.Extended()
else:
    error = f'ERR_SSHKeyboard010: No Remote Mode'
    raise Exception(error)


## Set up IR Tool
## Set up Remote TX Object
GPIO = CONFIG['GPIO']
SYSTEM_MODE = CONFIG['system_mode']
IR_TOOL = CONFIG['ir_tool']
REMOTE_KEYMAP_FOLDER_NAME = MAPS_CONFIG['keymaps'][IR_TOOL]['folder']
REMOTE_KEYMAP_FILE_NAME = \
    MAPS_CONFIG['keymaps'][IR_TOOL][RC_MODES[RC_MODE]]

if IR_TOOL == 'piir':
    import ir_tools.piir as irt
    remote_tx = irt.IR_PiIR(GPIO, REMOTE_KEYMAP_FILE_NAME,
                            REMOTE_KEYMAP_FOLDER_NAME)
elif IR_TOOL == 'rpigpio':
    import ir_tools.rpigpio as irt
    remote_tx = irt.RPiGPIO(GPIO, REMOTE_KEYMAP_FILE_NAME,
                            REMOTE_KEYMAP_FOLDER_NAME)
elif IR_TOOL == 'lirc':
    import ir_tools.lirc as irt
    remote_tx = irt.IR_LIRC(GPIO, REMOTE_KEYMAP_FILE_NAME,
                            REMOTE_KEYMAP_FOLDER_NAME)
elif IR_TOOL == 'ir_ctl':
    import ir_tools.ir_ctl as irt
    remote_tx = irt.IR_ir_ctl(GPIO, REMOTE_KEYMAP_FILE_NAME,
                              REMOTE_KEYMAP_FOLDER_NAME)
else:
    error = f'ERR_SSHKeyboard_020: No IR Tool'
    raise Exception(error)


## Set up KEYBOARD
import keypad
button_maps_file_name = (MAPS_CONFIG['button_maps']['folder'] 
                         + '/' 
                         + MAPS_CONFIG['button_maps'][RC_MODES[RC_MODE]])
kb = keypad.Keypad(button_maps_file_name)

def on_press(key: str) -> bool:
    """Send command in response to key pressed.
    
    Args:
        key (str): the key pressed in string form (e.g., 'up' or 'a')

    Returns
        continue (bool): True to keep listening for keys, 
            False otherwise.
    """
    print(f'--------------------\nKey {key} pressed')
    if key == 'q' or key == 'Key.esc':
        print('Good Bye')
        stop_listening()
        return False
    if kb.is_mapped_key(key):
        mapped_key = kb.get_action(key)
        print(f'Mapped Key: {mapped_key}')
        if SYSTEM_MODE == 'RAW':
            data = rc_encoder.get_scancode(*mapped_key)
            print(f'Raw code: {data:04X}')
            remote_tx.send_raw(data)
        elif SYSTEM_MODE == 'KEY':
            data = rc_encoder.get_keycode(*mapped_key)
            print(f'Key code: {data}')
            remote_tx.send(data)
        elif SYSTEM_MODE == 'HEX':
            data = rc_encoder.get_scancode(*mapped_key)
            print(f'Hex code: {data:04X}')
            remote_tx.send_hex(f'{data:04X}')
        else:
            error = f'ERR_SSHKeyboard_025: No SYSTEM MODE'
            raise Exception(error)
        return True
    else:
        print(f'Unknown Key: {key}')
        return True


def on_release(key: str) -> bool:
    """Check if key pressed is 'q', otherwise do nothing.
        
    Args:
        key (str): the key released in string form (e.g., 'up' or 'a')

    Returns
        continue (bool): True to keep listening for keys, 
            False otherwise.
    """
    print(f'Key {key} released')
    if key == 'q' or key == 'Key.esc':
        print('Good Bye')
        stop_listening()
        return False


def start_listen() -> None:
    """Start listening for keyboard strokes.
    
    When key is pressed call on_press(key).
    When key is released call on_release(key)
    """
    listen_keyboard(
        on_press=on_press,
        on_release=on_release,
        sequential=True,
        debug=True,
        delay_second_char=0.75,
        delay_other_chars=0.05,
    )


# Main
print(f'Tool: {IR_TOOL} | Tool Mode: {SYSTEM_MODE} | RC Mode: {RC_MODE}')
start_listen()