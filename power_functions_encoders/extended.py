class Extended:
    
    def __init__(self) -> None:
        pass

    NAME = 'Extended'

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

    COLORS = {
        'red': 'R',
        'blue': 'B'
    }

    state = {
        'red'  : 0,
        'blue' : 0
    }
    
    toggle_bit = '1'
    addres_bit = '0'
    
    def __init__(self) -> None:
        pass

    def get_keycode(self, color: str, action: str) -> str:
        if color == '':
            keycode =  action + '_' + self.toggle_bit + self.addres_bit
        else:
            keycode =  action + '_' + self.COLORS[color] + '_' + self.toggle_bit + self.addres_bit            
        return keycode

    def toggle_address_bit(self):
        if self.addres_bit == '0':
            self.addres_bit = '1'
        else:
            self.addres_bit = '0'

    def toggle_toggle_bit(self):
        if self.toggle_bit == '0':
            self.toggle_bit = '1'
        else:
            self.toggle_bit = '0'

    def speed_change(self, color: str, increment: int) -> str:
        if abs(self.state[color] + increment) <= 7:
            self.state[color] += increment
        if increment == +1:
            keycode = 'INC_R' + '_' + self.toggle_bit + '0'
        elif increment == -1:
            keycode = 'DEC_R' + '_' + self.toggle_bit + '0'
        else:
            error = f'ERR_EXT_010: Sorry, there is a problem with the speed increment'
            raise Exception(error)
        return keycode

    def set_speed(self, color: str, speed: int) -> str:
        if speed == -99:
            if color != 'red':
                error = f'Sorry, color {color} is not valid or does not have BRK command'
                raise Exception(error)
            keycode = 'BRK_R_' + self.toggle_bit + '0'
            self.state[color] = 0
        elif color == 'blue' and speed == 0 and self.state['blue'] == +7:
            self.state[color] = 0
            keycode = 'TOG_B_' + self.toggle_bit + '0'
        elif color == 'blue' and speed == +7 and self.state['blue'] == 0:
            self.state[color] = 7
            keycode = 'TOG_B_' + self.toggle_bit + '0'
        else:
            error = f'ERR_EXT_020: Sorry, color: {color}-speed: {speed}- state: {self.state[color]} combination is not valid or does not have enough information'
            raise Exception(error)
        return keycode

    def action(self, color: str, action: str) -> str:
        if action == 'BRK':
            self.state[color] = 0
            data = 'BRK_R' + '_' + self.toggle_bit + '0'
        elif action == 'INC':
            data = self.speed_change('red', +1 )
        elif action == 'DEC':
            data = self.speed_change('red', -1 )
        elif action == 'TOG':
            if self.state['blue'] == 7:
                self.state['blue'] = 0
            elif self.state['blue'] == 0:
                self.state['blue'] = 7
            else:
                error = f'ERR_EXT_030: Sorry, there is a problem with the speed of the Blue output'
                raise Exception(error)
            data = 'TOG_B' + '_' + self.toggle_bit + '0'
        elif action == 'TOG_ADDR':
            self.toggle_address_bit()
            data = 'TOGG' + '_' + self.toggle_bit + self.addres_bit
        else:
            error = f'ERR_EXT_040: Action {action} not recognized'
            raise Exception(error)
        self.toggle_toggle_bit()
        return data