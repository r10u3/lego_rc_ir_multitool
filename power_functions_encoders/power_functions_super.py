class LegoPF:

    def __init__(self, extended : int = 0, channel : int = 0, mode : int = 0x4) -> None:
        self.nibble1 = (extended << 2) | channel
        self.nibble2 = mode

    address_bit = 0
    toggle_bit = 0

    def toggle_address_bit(self) -> None:
        self.address_bit = '1' if self.address_bit == '0' else '0'

    def toggle_toggle_bit(self) -> None:
        self.toggle_bit = 1 if self.toggle_bit == 0 else 0

    def get_nibble1(self) -> int:
        return self.nibble1 | (self.toggle_bit  << 3)

    def get_nibble2(self) -> int:
        pass

    def get_data_nibble(self, action: str) -> int:
        return self.ACTIONS.index(action)

    def get_nibble4(self, nibble1: int, nibble2: int, nibble3: int) -> int:
        return 0xf ^ nibble1 ^ nibble2 ^ nibble3

    def get_scancode(self, arg_1: str, arg_2: str) -> int:
        pass

    def get_keycode(self, arg_1: str, arg_2: str) -> str:
        pass
        
    def get_hexcode(self, arg_1: str, arg_2: str) -> int:
        return f'{self.get_scancode(arg_1, arg_2):04X}'
