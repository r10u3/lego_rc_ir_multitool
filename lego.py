from sshkeyboard import listen_keyboard, stop_listening
import json

import keyboard as kb

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

## Set up KEYBOARD
rc_mode = RC_MODES[CONFIG['rc_mode']]
button_maps_file_name = MAPS_CONFIG['button_maps']['folder'] + '/' + MAPS_CONFIG['button_maps'][rc_mode]
kb.map_keys(button_maps_file_name, rc_mode)


## Set up RC Mode
RC_MODE = CONFIG['rc_mode']
if (CONFIG['rc_mode'] == 'PWM'):
    import power_functions.combo_pwm as pf
elif (CONFIG['rc_mode'] == 'DIR'):
    import power_functions.combo_direct as pf
elif (CONFIG['rc_mode'] == 'SGL'):
    import power_functions.single_pwm as pf
elif (CONFIG['rc_mode'] == 'OTH'):
    import power_functions.single_other as pf
else:
    raise Exception(f'No Remote Mode')


## Set up System Mode
ir_tool = CONFIG['ir_tool']
if (ir_tool == 'piir'):
    import ir_tools.piir as irt
elif (ir_tool == 'lirc'):
    import ir_tools.lirc as irt
elif (ir_tool == 'ir_ctl'):
    import ir_tools.ir_ctl as irt
else:
    raise Exception(f'No IR Tool')


## Set up Remote TX Object
# print(MAPS_CONFIG)
REMOTE_KEYMAP_FOLDER_NAME = MAPS_CONFIG['keymaps'][ir_tool]['folder']
REMOTE_KEYMAP_FILE_NAME = MAPS_CONFIG['keymaps'][CONFIG['ir_tool']][rc_mode]
REMOTE_TX = irt.IR_Transmitter(REMOTE_KEYMAP_FILE_NAME , REMOTE_KEYMAP_FOLDER_NAME , CONFIG['gpio_pin'])


def on_press(key: str) -> bool:
    global REMOTE_TX
    print(f'Key {key} pressed')
    if (key == 'q') or (key == 'Key.esc'):
        print('Good Bye')
        stop_listening()
        return False
    if kb.is_mapped_key(key):
        mapped_key = kb.get_action(key)
        print(f'Mapped Key: {mapped_key}')
        data = pf.action(mapped_key)
        REMOTE_TX.send(data)
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