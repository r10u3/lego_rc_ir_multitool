import power_functions_encoders.power_functions_super as pf

class ComboPWM(pf.LegoPF):
    
    NAME = 'ComboPWM'

    ACTIONS = ['FLT', 'FW1', 'FW2', 'FW3', 'FW4', 'FW5', 'FW6', 'FW7',
               'BRK', 'RV7', 'RV6', 'RV5', 'RV4', 'RV3', 'RV2', 'RV1']

    def __init__(self, channel : int = 0) -> None:
        self.nibble1 = 0x4 | channel

    def get_nibble1(self) -> int:
        return self.nibble1 | (self.address_bit << 3)       # address bit instead of toggle bit

    def get_scancode(self, action_A: str, action_B: str) -> int:
        self.toggle_toggle_bit()
        nibble1 = self.get_nibble1()
        nibble2 = self.get_data_nibble(action_B)
        nibble3 = self.get_data_nibble(action_A)
        nibble4 = self.get_nibble4(nibble1, nibble2, nibble3)
        return (nibble1 << 12) | (nibble2 << 8) | (nibble3 << 4) | (nibble4)

    def get_keycode(self, action_A: str, action_B: str) -> str:
        return action_A + '_' + action_B   # no toggle for combo_pwm
