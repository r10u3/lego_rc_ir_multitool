import subprocess

class IR_ir_ctl:
    def __init__(self,  GPIO: int, keymap_file_name: str, 
                 keymap_folder_name: str = '/maps/keymaps/ir_ctl') -> None:
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


