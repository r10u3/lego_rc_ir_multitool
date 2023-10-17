class ComboPWM:
    
    def __init__(self) -> None:
        pass


    NAME = 'ComboPWM'

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

    state = {
        'red'  : 0,
        'blue' : 0
        }

    def get_keycode(self, speed_red: int, speed_blue: int) -> str:
        if (speed_red not in self.SPEEDS
                or speed_blue not in self.SPEEDS):
            error = 'ERR_PWM_010: one of the speeds not in range'
            raise Exception (error)
        keycode = self.SPEEDS[speed_red]+'_'+self.SPEEDS[speed_blue]
        return keycode

    def speed_change(self, color: str, increment: int) -> str:
        if abs(self.state[color] + increment) <= 7:
            self.state[color] += increment
            #print (f'Color: {color} | State[{color}]: {state[color]} | increment: {increment}')
        keycode = self.get_keycode(self.state['red'], self.state['blue'])
        return keycode

    def set_speed(self, color: str, speed: int) -> str:
        if speed == -99:
            self.state[color] = -99
            keycode = self.get_keycode(self.state['red'], self.state['blue'])
            self.state[color] = 0
        else:
            self.state[color] = speed
            keycode = self.get_keycode(self.state['red'], self.state['blue'])
        return keycode

    def action(self, color: str, action: str) -> str:
        if action == 'BRK':
            data = self.set_speed(color, -99)
        elif action == 'INC':
            data = self.speed_change(color, +1)
        elif action == 'DEC':
            data = self.speed_change(color, -1)
        elif action == 'FLT':
            data = self.set_speed(color, 0)
        elif type(action) is int and abs(action)<= 7:
            data = self.set_speed(color, action)
        else:
            error = f'ERR_PWM_30: Action {action} not recognized'
            raise Exception(error)
        return data