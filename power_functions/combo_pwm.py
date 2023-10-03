
NAME = 'Combo_PWM'

SPEEDS = {
    0 : 'FLT',
    1 : 'FW1',
    2 : 'FW2',
    3 : 'FW3',
    4 : 'FW4',
    5 : 'FW5',
    6 : 'FW6',
    7 : 'FW7',
    -99 : 'BRK',
    -7 : 'RV7',
    -6 : 'RV6',
    -5 : 'RV5',
    -4 : 'RV4',
    -3 : 'RV3',
    -2 : 'RV2',
    -1 : 'RV1'
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

def speed_change(color: str , increment: int) -> str:
    global state
    if (abs(state[color] + increment) <= 7):
        state[color] += increment
        #print (f'Color: {color} | State[{color}]: {state[color]} | increment: {increment}')
    keycode = get_keycode(state['red'] , state['blue'])
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
    elif action == 'INC':
        data = speed_change(color , +1)
    elif action == 'DEC':
        data = speed_change(color , -1)
    elif action == 'FLT':
        data = set_speed(color , 0)
    elif (type(action) is int and abs(action)<= 7):
        data = set_speed(color , action)
    else:
        error = f'Action {action} not recognized'
        raise Exception(error)
    return data