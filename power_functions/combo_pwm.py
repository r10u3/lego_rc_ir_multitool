class Combo_PWM:
    
    def __init__(self) -> None:
        pass


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

    def get_keycode(self , speed_red: int , speed_blue: int) -> str:
        if (speed_red not in self.SPEEDS or speed_blue not in self.SPEEDS):
            return 'ERROR: one of the speeds not in range'
        keycode = self.SPEEDS[speed_red]+'_'+self.SPEEDS[speed_blue]
        return keycode

    def speed_change(self , color: str , increment: int) -> str:
        if (abs(self.state[color] + increment) <= 7):
            self.state[color] += increment
            #print (f'Color: {color} | State[{color}]: {state[color]} | increment: {increment}')
        keycode = self.get_keycode(self.state['red'] , self.state['blue'])
        return keycode

    def set_speed(self , color: str , speed: int) -> str:
        if (speed == -99):
            self.state[color] = -99
            keycode = self.get_keycode(self.state['red'] , self.state['blue'])
            self.state[color] = 0
        else:
            self.state[color] = speed
            keycode = self.get_keycode(self.state['red'] , self.state['blue'])
        return keycode

    def action(self , mapped_key) -> str:
        color = mapped_key[0]
        action= mapped_key[1]
        if action == 'BRK':
            data = self.set_speed(color , -99)
        elif action == 'INC':
            data = self.speed_change(color , +1)
        elif action == 'DEC':
            data = self.speed_change(color , -1)
        elif action == 'FLT':
            data = self.set_speed(color , 0)
        elif (type(action) is int and abs(action)<= 7):
            data = self.set_speed(color , action)
        else:
            error = f'Action {action} not recognized'
            raise Exception(error)
        return data