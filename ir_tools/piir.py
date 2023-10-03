import piir

class IR_Transmitter:
    def __init__(self: any , keymap_file_name: str, keymap_folder_name: str,  gpio_pin: str) -> None:
        keymap_file_with_path = keymap_folder_name + '/' + keymap_file_name
        self.REMOTE_TX = piir.Remote(keymap_file_with_path, gpio_pin)
        print(f'Remote: piir: {keymap_file_name}')

    def send(self , data: str) -> None:
        self.REMOTE_TX.send(data)

    def send_x(self , data_bytes: hex) -> None:
        self.REMOTE_TX.send_data(data_bytes)

