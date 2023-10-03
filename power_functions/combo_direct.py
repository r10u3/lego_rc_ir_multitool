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
        if (speed_red not in self.SPEEDS or speed_blue not in self.SPEEDS):
            return 'ERROR: one of the speeds not in range'
        keycode = self.SPEEDS[speed_red]+'_'+self.SPEEDS[speed_blue]
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
        elif action == 'FWD':
            data = self.set_speed(color , +7)
        elif action == 'REV':
            data = self.set_speed(color , -7)
        elif action == 'FLT':
            data = self.set_speed(color , 0)
        else:
            error = f'Action {action} not recognized'
            raise Exception(error)
        return data