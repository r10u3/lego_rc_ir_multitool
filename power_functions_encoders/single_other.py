import math

class SingleOther:
    
    def __init__(self) -> None:
        self.nibble1 = 0x0
        self.nibble2 = 0x6

    NAME = 'SingleOther'

    COLORS = {
        'red': 'R',
        'blue': 'B'
    }

    state = {
        'red'  : 0, 
        'blue' : 0
    }

    toggle_bit = 0

    def toggle_toggle_bit(self) -> None:
        if self.toggle_bit == 0:
            self.toggle_bit = 1
        else:
            self.toggle_bit = 0


    def get_keycode(self, color: str, action: str) -> str:
        keycode = self.COLORS[color] + '_' + action + '_' + str(self.toggle_bit)
        return keycode

    def speed_change(self, color: str, increment: int) -> None:
        if abs(self.state[color] + increment) <= 7:
            self.state[color] += increment

    def set_speed(self, color: str, speed: int) -> None:
        if speed == -99:
            self.state[color] = -99
            self.state[color] = 0
        else:
            self.state[color] = speed

    def action(self, color: str, action: str) -> str:
        self.toggle_toggle_bit()
        if action == 'INC_PWM':
            #Increment PWM
            self.speed_change(color, +1)
        elif action == 'DEC_PWM':
            #Decrement PWM
            self.speed_change(color, -1)
        elif action == 'INC_NUM':
            #Increment numerical PWM
            if self.state[color] == 0:
                pass
            elif math.copysign(1 , self.state[color]) == +1:
                self.speed_change(color, +1)
            else:
                self.speed_change(color, -1)
        elif action == 'DEC_NUM':
            #Decrement numerical PWM
            if self.state[color] == 0:
                pass
            elif math.copysign(1 , self.state[color]) == +1:
                self.speed_change(color, -1)
            else:
                self.speed_change(color, +1)
        elif action == 'FUL_FWD':
            #Full forward (timeout)
            self.set_speed(color, +7)
        elif action == 'FUL_BCK':
            #Full backward (timeout)
            self.set_speed(color, -7)
        elif action == 'TOG_0000':
            #Toggle full forward (Stop → Fw, Fw → Stop, Bw → Fw)
            if (self.state[color] == 0
                    or self.state[color] == -7):
                self.set_speed(color, +7)
            elif self.state[color] == +7:
                self.set_speed(color, 0)
            else:
                self.set_speed(color, 0)
        elif action == 'TOG_0001':
            #Toggle direction
            self.set_speed(color, -self.state[color])
        elif action == 'TOG_1000':
            #Toggle full forward/backward (default forward)
            if self.state[color] == +7:
                self.set_speed(color, -7)
            else:
                self.set_speed(color, +7)
        elif action == 'TOG_1111':
            #Toggle full backward (Stop → Bw, Bw → Stop, Fwd → Bw)
            if (self.state[color] == 0
                    or self.state[color] == +7):
                self.set_speed(color, -7)
            elif self.state[color] == -7:
                self.set_speed(color, 0)
            else:
                self.set_speed(color, -7)
        elif action == 'CLR_C1':
            #Clear C1 (negative logic – C1 high)
            self.set_speed(color, 0)
        elif action == 'SET_C1':
            #Set C1 (negative logic – C1 low)
            self.set_speed(color, +7)
        elif action == 'TOG_C1':
            #Toggle C1
            if self.state[color] == -7:
                self.set_speed(color, +7)
            else:
                self.set_speed(color, +7)
        elif action == 'CLR_C2':
            #Clear C2 (negative logic – C2 high)
            self.set_speed(color, 0)
        elif action == 'SET_C2':
            #Set C2 (negative logic – C2 low)
            self.set_speed(color, -7)
        elif action == 'TOG_C2':
            #Toggle C2
            if self.state[color] == -7:
                self.set_speed(color, +7)
            else:
                self.set_speed(color, +7)
        else:
            error = f'OTH_010: Action {action} not recognized'
            raise Exception(error)
        data = self.get_keycode(color, action)
        return data


    DATACODES = {
        0b0000: "TOG_0000", #Toggle full forward (Stop → Fw, Fw → Stop, Bw → Fw)
        0b0001: "TOG_0001", #Toggle direction
        0b0010: "INC_NUM",  #Increment numerical PWM
        0b0011: "DEC_NUM",  #Decrement numerical PWM
        0b0100: "INC_PWM",  #Increment PWM
        0b0101: "DEC_PWM",  #Decrement PWM
        0b0110: "FUL_FWD",  #Full forward (timeout)
        0b0111: "FUL_REV",  #Full backward (timeout)
        0b1000: "TOG_1000", #Toggle full forward/backward (default forward)
        0b1001: "CLR_C1",   #Clear C1 (negative logic – C1 high)
        0b1010: "SET_C1",   #Set C1 (negative logic – C1 low)
        0b1011: "TOG_C1",   #Toggle C1
        0b1100: "CLR_C2",   #Clear C2 (negative logic – C2 high)
        0b1101: "SET_C2",   #Set C2 (negative logic – C2 low)
        0b1110: "TOG_C2",   #Toggle C2
        0b1111: "TOG_1111"  #Toggle full backward (Stop → Bw, Bw → Stop, Fwd → Bw)
    }

    def get_nibble1(self, channel: int = 0) -> int:
        print(f'nibble1: {type(self.nibble1)} | togglebit: {type(self.toggle_bit)}')
        return self.nibble1 | (self.toggle_bit * 8) | channel
    
    def get_nibble2(self, output: int = 0) -> int:
        return self.nibble2 | output
    
    def get_nibble3(self, action: str) -> int:
        idx_action = list(self.DATACODES.values()).index(action)
        return list(self.DATACODES.keys())[idx_action]

    def get_nibble4(self, nibble1: int, nibble2: int, nibble3: int) -> int:
        return 0xf ^ nibble1 ^ nibble2 ^ nibble3
    
    def get_scancode(self, nibble1: int, nibble2: int, nibble3: int, nibble4: int) -> int:
        return (nibble1 << 12) | (nibble2 << 8) | (nibble3 << 4) | (nibble4)
    
    def get_scancode(self, color: str, action: str) -> int:
        self.toggle_toggle_bit()
        if color == 'red':
            output = 0
        else:
            output = 1
        nibble1 = self.get_nibble1()
        nibble2 = self.get_nibble2(output)
        nibble3 = self.get_nibble3(action)
        nibble4 = self.get_nibble4(nibble1, nibble2, nibble3)
        return self.get_scancode(nibble1, nibble2, nibble3, nibble4)