class Combo_Direct:
    
    def __init__(self) -> None:
        pass

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
    
    def __init__(self) -> None:
        pass

    def get_keycode(self , speed_red: int , speed_blue: int) -> str:
        if speed_red not in self.SPEEDS or speed_blue not in self.SPEEDS:
            error = 'ERR_DIR_10: one of the speeds not in range' 
            raise Exception(error)
        keycode = self.SPEEDS[speed_red]+'_'+self.SPEEDS[speed_blue]
        return keycode

    def set_speed(self , color: str , speed: int) -> str:
        if speed == -99:
            self.state[color] = -99
            keycode = self.get_keycode(self.state['red'] , self.state['blue'])
            self.state[color] = 0
        elif abs(speed) == 7 or speed == 0:
            self.state[color] = speed
            keycode = self.get_keycode(self.state['red'] , self.state['blue'])
        else:
            error = f'ERR_DIR_20: Sorry, speed of {speed} is not allowed in Combo Direct mode'
            raise Exception(error)
        return keycode

    def action(self , color , action) -> str:
        if action == 'BRK':
            data = self.set_speed(color , -99)
        elif action == 'FWD':
            data = self.set_speed(color , +7)
        elif action == 'REV':
            data = self.set_speed(color , -7)
        elif action == 'FLT':
            data = self.set_speed(color , 0)
        else:
            error = f'ERR_DIR_30: Action {action} not recognized'
            raise Exception(error)
        return data