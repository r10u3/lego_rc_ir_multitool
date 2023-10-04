from sshkeyboard import listen_keyboard, stop_listening
import json

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
rc_mode = RC_MODES[CONFIG['rc_mode']]
RC_MODE = CONFIG['rc_mode']
if (CONFIG['rc_mode'] == 'PWM'):
    import power_functions.combo_pwm as pf
    rc_encoder = pf.Combo_PWM()
elif (CONFIG['rc_mode'] == 'DIR'):
    import power_functions.combo_direct as pf
    rc_encoder = pf.Combo_Direct()
elif (CONFIG['rc_mode'] == 'SGL'):
    import power_functions.single_pwm as pf
    rc_encoder = pf.Single_PWM()
elif (CONFIG['rc_mode'] == 'OTH'):
    import power_functions.single_other as pf
    rc_encoder = pf.Single_Other()
else:
    raise Exception(f'No Remote Mode')

## Set up System Mode
## Set up Remote TX Object
ir_tool = CONFIG['ir_tool']
REMOTE_KEYMAP_FOLDER_NAME = MAPS_CONFIG['keymaps'][ir_tool]['folder']
REMOTE_KEYMAP_FILE_NAME = MAPS_CONFIG['keymaps'][CONFIG['ir_tool']][rc_mode]
if (ir_tool == 'piir'):
    import ir_tools.piir as irt
    remote_tx = irt.IR_PiIR(REMOTE_KEYMAP_FILE_NAME , REMOTE_KEYMAP_FOLDER_NAME , CONFIG['gpio_pin'])
elif (ir_tool == 'lirc'):
    import ir_tools.lirc as irt
    remote_tx = irt.IR_LIRC(REMOTE_KEYMAP_FILE_NAME , REMOTE_KEYMAP_FOLDER_NAME , CONFIG['gpio_pin'])
elif (ir_tool == 'ir_ctl'):
    import ir_tools.ir_ctl as irt
    remote_tx = irt.IR_ir_ctl(REMOTE_KEYMAP_FILE_NAME , REMOTE_KEYMAP_FOLDER_NAME , CONFIG['gpio_pin'])
else:
    raise Exception(f'No IR Tool')


## Set up KEYBOARD
import keypad
button_maps_file_name = MAPS_CONFIG['button_maps']['folder'] + '/' + MAPS_CONFIG['button_maps'][rc_mode]
kb = keypad.Keypad(button_maps_file_name)

def on_press(key: str) -> bool:
    print(f'Key {key} pressed')
    if (key == 'q') or (key == 'Key.esc'):
        print('Good Bye')
        stop_listening()
        return False
    if kb.is_mapped_key(key):
        mapped_key = kb.get_action(key)
        print(f'Mapped Key: {mapped_key}')
        data = rc_encoder.action(mapped_key)
        remote_tx.send(data)
        print(f'keycode sent: {data}')
        return True
    else:
        print(f'Unknown Key: {key}')
        return True

def on_release(key: str) -> bool:
    print(f'Key {key} released')
    if (key == 'q') or (key == 'Key.esc'):
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