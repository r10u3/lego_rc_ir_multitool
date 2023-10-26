import piir

class IR_PiIR:
    def __init__(self,  GPIO: int = 18, keymap_file_name: str = 'single_pwm.json',
                 keymap_folder_name: str = 'maps/keymaps/piir') -> None:
        """Uses PiIR library to send IR codes. PiIR uses pigpio library.

        Args:
            GPIO (int): PIN must be Hardware PWM.
                Default = 18.
            keymap_file_name (str): the name of the file 
                containing the keymap.
                Default = 'single_pwm.json'.
            keymap_folder_name (str): the name of the file 
                containing the keymap. Can be absolute or relative.
                Default = 'maps/keymaps/piir'.
        """
        keymap_file_with_path = (keymap_folder_name 
                                 + '/' 
                                 + keymap_file_name)
        self.REMOTE_TX = piir.Remote(keymap_file_with_path, GPIO)

    def send_raw(self, data_int: int) -> None:
        """Send IR using PiIR.
        
        Args:
            data_int (int): the scancode to be sent in int format.
                Can be int, hexadecimal (0x) or binary (0b).
        """
        self.REMOTE_TX.send_data(self._hex_pre_processor(f'{data_int:04X}'))

    def _hex_pre_processor(self, input: str) -> str:
        raw_chars = [input[i:i+2] for i in range(0, len(input), 2)]
        reversed_bytes = [f'{int(f"{int(char, 16):08b}"[::-1], 2):02X}'
                          for char in raw_chars]
        return ' '.join(reversed_bytes)

    def send_hex(self, data_bytes: str) -> None:
        """Send IR using PiIR.
        
        Args:
            data_bytes (str): the scancode to be sent 
                in hexadecimal string format.
        """
        self.REMOTE_TX.send_data(self._hex_pre_processor(data_bytes))

    def send(self, keycode: str) -> None:
        """Send IR using PiIR.
        
        Args:
            keycode (str): the keycode to be sent.
        """
        self.REMOTE_TX.send(keycode)

