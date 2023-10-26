import power_functions_encoders.power_functions_super as pf

class SinglePWM(pf.LegoPF):

    NAME = 'SinglePWM'

    ACTIONS = ['FLT', 'FW1', 'FW2', 'FW3', 'FW4', 'FW5', 'FW6', 'FW7',
               'BRK', 'RV7', 'RV6', 'RV5', 'RV4', 'RV3', 'RV2', 'RV1']

    def __init__(self, channel : int = 1) -> None:
        self.nibble1 = 0x0 | (channel - 1)
        self.nibble2 = 0x4

    def get_nibble2(self, output: int) -> int:
        output_bit = 0 if output == 'A' else 1
        return self.nibble2 | (self.address_bit  << 3) | output_bit     # adds output

    def get_scancode(self, output: str, action: str) -> int:
        self.toggle_toggle_bit()
        nibble1 = self.get_nibble1()
        nibble2 = self.get_nibble2(output)          # Output = A or B
        nibble3 = self.get_data_nibble(action)
        nibble4 = self.get_nibble4(nibble1, nibble2, nibble3)
        return (nibble1 << 12) | (nibble2 << 8) | (nibble3 << 4) | (nibble4)
    
    def get_keycode(self, output: str, action: str) -> str:
        self.toggle_toggle_bit()
        return output + '_' + action + '_' + str(self.toggle_bit)
