import power_functions_encoders.power_functions_super as pf

class Extended(pf.LegoPF):
    
    NAME = 'Extended'

    ACTIONS = [
        'BRK',       # Brake then float output A
        'INC',       # Increment speed on output A
        'DEC',       # Decrement speed on output A
        'NOT_USED',  # Not used
        'TOG',       # Toggle forward/float on output B
        'NOT_USED',  # Not used
        'ADD_TOG',   # Toggle Address bit
        'TOG_AGN',   # Align toggle bit (get in sync)
        'RSVD'       # Reserved
    ]

    def __init__(self, channel : int = 0) -> None:
        self.nibble1 = 0x0 | channel
        self.nibble2 = 0x0

    def get_nibble2(self) -> int:
        return self.nibble2 | (self.address_bit  << 3)

    def get_scancode(self, output: str, action: str) -> int:
        self.toggle_toggle_bit()
        nibble1 = self.get_nibble1()
        nibble2 = self.get_nibble2()
        nibble3 = self.get_data_nibble(action)
        nibble4 = self.get_nibble4(nibble1, nibble2, nibble3)
        return (nibble1 << 12) | (nibble2 << 8) | (nibble3 << 4) | (nibble4)

    def get_keycode(self, output: str, action: str) -> str:
        self.toggle_toggle_bit()
        keycode = action + '_' + str(self.toggle_bit) + str(self.address_bit) \
            if output == '' \
                else output + '_' + action + '_' + str(self.toggle_bit) + str(self.address_bit)
        return keycode