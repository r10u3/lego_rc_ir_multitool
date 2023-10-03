NAME = 'Single_Other'

COLORS = {
    'red': 'R',
    'blue': 'B'
}

# holds speeds
state = {
            'red'  : 0 , 
            'blue' : 0
        }

def get_keycode(color: str , action: str) -> str:
    global COLORS
    #print(f'color: {color}')
    #print(COLORS)
    #print (COLORS[color])
    keycode = COLORS[color] + '_' + action
    return keycode

def speed_change(color: str , increment: int) -> None:
    global state
    if (abs(state[color] + increment) <= 7):
        state[color] += increment
        #print (f'Color: {color} | State[{color}]: {state[color]} | increment: {increment}')

def set_speed(color: str , speed: int) -> None:
    global state
    if (speed == -99):
        state[color] = -99
        state[color] = 0
    else:
        state[color] = speed

def action(mapped_key) -> str:
    color = mapped_key[0]
    action= mapped_key[1]
    if action in ['INC_NUM','INC_PWM']:
        speed_change(color , +1)
    elif action in ['DEC_NUM','DEC_PWM']:
        speed_change(color , -1)
    elif action in ['FUL_FWD']:
        set_speed(color , +7)
    elif action in ['FUL_BCK']:
        set_speed(color , -7)
    elif action in ['TOG_DIR','TOG_0000','TOG_1000','TOG_1111','CLR_C1','SET_C1','TOG_C1','CLR_C2','SET_C2','TOG_C2']:
        set_speed(color , 0)
    else:
        error = f'Action {action} not recognized'
        raise Exception(error)
    data = get_keycode(color , action)
    return data

{





}