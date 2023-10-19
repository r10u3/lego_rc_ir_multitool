class SinglePWM:
    
    def __init__(self) -> None:
        pass
    NAME = 'SinglePWM'

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

    def get_keycode(self, color: str, speed: int) -> str:
        if speed not in self.SPEEDS:
            return 'ERROR: Speed not in range'
        keycode = self.COLORS[color] + "_" + self.SPEEDS[speed]
        return keycode

    def speed_change(self, color: str, increment: int) -> str:
        if abs(self.state[color] + increment) <= 7:
            self.state[color] += increment
        keycode = self.get_keycode(color, self.state[color])
        return keycode

    def set_speed(self, color: str, speed: int) -> str:
        if speed == -99:
            self.state[color] = -99
            keycode = self.get_keycode(color, self.state[color])
            self.state[color] = 0
        else:
            self.state[color] = speed
            keycode = self.get_keycode(color, self.state[color])
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
            error = f'Action {action} not recognized'
            raise Exception(error)
        return data