import subprocess

class IR_ir_ctl:
    def __init__(self,  GPIO: int, keymap_file_name: str, 
                 keymap_folder_name: str = 'maps/keymaps/ir_ctl') -> None:
        """Uses ir-ctl system command to send IR codes

        Args:
            GPIO (int): not used. Left in for consistency 
                with other tools. ir-ctl uses the pin configured 
                in the /boot/config.txt file.
            keymap_file_name (str): the name of the file 
                containing the keymap.
            keymap_folder_name (str): the folder where the keymap is.
                Default = 'maps/keymaps/ir_ctl'.
        """
        self.keymap_file_name = (keymap_folder_name 
                                 + '/' 
                                 + keymap_file_name)
        # gpio pin is useless here. we are bound by the system configuration

    def send(self, data: str) -> None:
        params = []
        params.append('ir-ctl')
        params.append(f'--keymap={self.keymap_file_name}')
        params.append(f'--keycode={data}')
        params.append(f'--verbose')
        try: 
            subprocess.run(params)
        except subprocess.CalledProcessError as e:
            print('Unable to send the scancode!')
            print (e.output)


