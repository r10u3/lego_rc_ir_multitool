NAME = 'Combo_Direct'

SPEEDS = {
    0 : 'FLT',
    7 : 'FWD',
    -99 : 'BRK',
    -7 : 'REV',
}

# holds speeds
state = {
            'red'  : 0 , 
            'blue' : 0
        }

def get_keycode(speed_red: int , speed_blue: int) -> str:
    global SPEEDS
    if (speed_red not in SPEEDS or speed_blue not in SPEEDS):
        return 'ERROR: one of the speeds not in range'
    keycode = SPEEDS[speed_red]+'_'+SPEEDS[speed_blue]
    return keycode

def set_speed(color: str , speed: int) -> str:
    global state
    if (speed == -99):
        state[color] = -99
        keycode = get_keycode(state['red'] , state['blue'])
        state[color] = 0
    else:
        state[color] = speed
        keycode = get_keycode(state['red'] , state['blue'])
    return keycode

def action(mapped_key) -> str:
    color = mapped_key[0]
    action= mapped_key[1]
    if action == 'BRK':
        data = set_speed(color , -99)
    elif action == 'FWD':
        data = set_speed(color , +7)
    elif action == 'REV':
        data = set_speed(color , -7)
    elif action == 'FLT':
        data = set_speed(color , 0)
    else:
        error = f'Action {action} not recognized'
        raise Exception(error)
    return data