import lirc


class IR_LIRC:
    def __init__(self: any , keymap_file_name: str, keymap_folder_name: str,  gpio_pin: str) -> None:
        self.LIRC_CLIENT = lirc.Client()
        self.REMOTE_NAME = keymap_file_name[0 : (len(keymap_file_name)-5)]
        print(f'Remote: lirc: {keymap_file_name}')

        # gpio pin AND keymap file name are useless here. we are bound by the system configuration

    def send(self , data: str) -> None:
        try:
            self.LIRC_CLIENT.send_once(self.REMOTE_NAME, data)
        except lirc.exceptions.LircdCommandFailureError as error:
            print('Unable to send the power key!')
            print(error)  # Error has more info on what lircd sent back.
