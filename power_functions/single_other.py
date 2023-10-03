class Single_Other:
    
    def __init__(self) -> None:
        pass

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

    def get_keycode(self , color: str , action: str) -> str:
        #print(f'color: {color}')
        #print(COLORS)
        #print (COLORS[color])
        keycode = self.COLORS[color] + '_' + action
        return keycode

    def speed_change(self , color: str , increment: int) -> None:
        if (abs(self.state[color] + increment) <= 7):
            self.state[color] += increment
            #print (f'Color: {color} | self.state[{color}]: {self.state[color]} | increment: {increment}')

    def set_speed(self , color: str , speed: int) -> None:
        if (speed == -99):
            self.state[color] = -99
            self.state[color] = 0
        else:
            self.state[color] = speed

    def action(self , mapped_key) -> str:
        color = mapped_key[0]
        action= mapped_key[1]
        if action in ['INC_NUM','INC_PWM']:
            self.speed_change(color , +1)
        elif action in ['DEC_NUM','DEC_PWM']:
            self.speed_change(color , -1)
        elif action in ['FUL_FWD']:
            self.set_speed(color , +7)
        elif action in ['FUL_BCK']:
            self.set_speed(color , -7)
        elif action in ['TOG_DIR','TOG_0000','TOG_1000','TOG_1111','CLR_C1','SET_C1','TOG_C1','CLR_C2','SET_C2','TOG_C2']:
            self.set_speed(color , 0)
        else:
            error = f'Action {action} not recognized'
            raise Exception(error)
        data = self.get_keycode(color , action)
        return data