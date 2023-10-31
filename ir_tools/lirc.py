import lirc

class IR_LIRC:
    def __init__(self,  
                 GPIO: int = '',
                 keymap_file_name: str = '',
                 keymap_folder_name: str = '') -> None:
        """Uses LIRC to send IR codes.

        Args:
            GPIO (int): not used. Left in for consistency 
                with other tools. LIRC uses the pin configured 
                in the /boot/config.txt file.
            keymap_file_name (str): not used. Left in for consistency 
                with other tools. LIRC uses keymaps stored in
                '/etc/lirc/lircd.conf.d'.
            keymap_folder_name (str):  not used. Left in for consistency 
                with other tools. LIRC uses keymaps stored in
                '/etc/lirc/lircd.conf.d'.
        """
        self.LIRC_CLIENT = lirc.Client()
        self.REMOTE_NAME = keymap_file_name[0 : (len(keymap_file_name)-5)]

        # gpio pin AND keymap file name are useless here. we are bound by the system configuration

    def send(self, keycode: str) -> None:
        """Send IR using LIRC.
        
        Args:
            keycode (str): the keycode to be sent.
        """
        try:
            self.LIRC_CLIENT.send_once(self.REMOTE_NAME, keycode)
        except lirc.exceptions.LircdCommandFailureError as e:
            print('Unable to send the power key!')
            print(e)  # Error has more info on what lircd sent back.
