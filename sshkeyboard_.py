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


def get_config(config_file_name: str) -> {}:
    with open(config_file_name, 'r') as config_file:
        config = json.loads(config_file.read())
    return config


def get_maps_config(maps_config_file_name):
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
    error = f'ERR_Lego_10: No Remote Mode'
    raise Exception(error)


## Set up IR Tool
## Set up Remote TX Object
GPIO = CONFIG['GPIO']
SYSTEM_MODE = CONFIG['system_mode']
IR_TOOL = 'rpigpio' if SYSTEM_MODE == 'SCAN' else CONFIG['ir_tool']
if SYSTEM_MODE == 'SCAN':
    print(f'SCAN mode -> IR_TOOL set to {IR_TOOL}')
REMOTE_KEYMAP_FOLDER_NAME = MAPS_CONFIG['keymaps'][IR_TOOL]['folder']
REMOTE_KEYMAP_FILE_NAME = MAPS_CONFIG['keymaps'][CONFIG['ir_tool']][RC_MODES[RC_MODE]]

if IR_TOOL == 'piir':
    import ir_tools.piir as irt
    remote_tx = irt.IR_PiIR(GPIO, REMOTE_KEYMAP_FILE_NAME, REMOTE_KEYMAP_FOLDER_NAME)
elif IR_TOOL == 'rpigpio':
    import ir_tools.rpigpio as irt
    remote_tx = irt.RPiGPIO(GPIO, REMOTE_KEYMAP_FILE_NAME, REMOTE_KEYMAP_FOLDER_NAME)
elif IR_TOOL == 'lirc':
    import ir_tools.lirc as irt
    remote_tx = irt.IR_LIRC(GPIO, REMOTE_KEYMAP_FILE_NAME, REMOTE_KEYMAP_FOLDER_NAME)
elif IR_TOOL == 'ir_ctl':
    import ir_tools.ir_ctl as irt
    remote_tx = irt.IR_ir_ctl(GPIO, REMOTE_KEYMAP_FILE_NAME, REMOTE_KEYMAP_FOLDER_NAME)
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
            print(f'Raw code: {data}')
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
        print(f'keycode sent: {data}')
        return True
    else:
        print(f'Unknown Key: {key}')
        return True


def on_release(key: str) -> bool:
    print(f'Key {key} released')
    if key == 'q' or key == 'Key.esc':
        print('Good Bye')
        stop_listening()
        return False


def start_listen() -> None:
    listen_keyboard(
        on_press=on_press,
        on_release=on_release,
        sequential=True,
        debug=True,
        delay_second_char=0.75,
        delay_other_chars=0.05,
    )


# Main
start_listen()