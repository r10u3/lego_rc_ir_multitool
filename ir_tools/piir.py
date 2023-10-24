import piir

class IR_PiIR:
    def __init__(self,  GPIO: int, keymap_file_name: str, keymap_folder_name: str = '/maps/keymaps/piir') -> None:
        keymap_file_with_path = (keymap_folder_name 
                                 + '/' 
                                 + keymap_file_name)
        self.REMOTE_TX = piir.Remote(keymap_file_with_path, GPIO)
        print(f'Remote: piir: {keymap_file_name}')

    def send(self, data: str) -> None:
        self.REMOTE_TX.send(data)

    def send_hex(self, data_bytes: str) -> None:
        data = self.pre_process_bit_string(data_bytes)
        self.REMOTE_TX.send_data(data)

    def send_raw(self, data: int) -> None:
        modified_data = self.hex_pre_processor(f'{data:04X}')
        self.REMOTE_TX.send_data([modified_data])

    def hex_pre_processor(self, input: str) -> str:
        print(f'Pre processed data: {input}')
        raw_chars = [input[i:i+2] for i in range(0, len(input), 2)]
        reversed_bytes = [f'{int(f"{int(char, 16):08b}"[::-1], 2):02X}' for char in raw_chars]
        print(f'Post processed data: {" ".join(reversed_bytes)}')
        return ' '.join(reversed_bytes)



