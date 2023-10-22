import power_functions_encoders.power_functions_super as pf

class ComboDirect(pf.LegoPF):

    NAME = 'ComboDirect'

    ACTIONS = ['FLT', 'FW7', 'RV7', 'BRK']

    def __init__(self, channel : int = 0) -> None:
        self.nibble1 = 0x0 | channel
        self.nibble2 = 0x1

    def get_nibble2(self) -> int:
        return self.nibble2 | (self.address_bit  << 3)

    def get_nibble3(self, action_A: str, action_B: str):
        data_A = self.get_data_nibble(action_A)
        data_B = self.get_data_nibble(action_B)
        nibble3 = (data_B << 2) | data_A
        return nibble3

    def get_scancode(self, action_A: str, action_B: str) -> int:
        self.toggle_toggle_bit()
        nibble1 = self.get_nibble1()
        nibble2 = self.get_nibble2()
        nibble3 = self.get_nibble3(action_A, action_B)
        nibble4 = self.get_nibble4(nibble1, nibble2, nibble3)
        return (nibble1 << 12) | (nibble2 << 8) | (nibble3 << 4) | (nibble4)

    def get_keycode(self, action_A: str, action_blue: str) -> str:
        return action_A + '_' + action_blue + '_' + str(self.toggle_bit)