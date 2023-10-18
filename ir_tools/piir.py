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

    def send_x(self, data_bytes: hex) -> None:
        self.REMOTE_TX.send_data(data_bytes)

