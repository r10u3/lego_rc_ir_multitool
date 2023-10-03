import subprocess

class IR_ir_ctl:
    def __init__(self: any , keymap_file_name: str, keymap_folder_name: str,  gpio_pin: str) -> None:
        self.keymap_file_name = keymap_folder_name + '/' + keymap_file_name
        print(f'IR_Transmitter: ir-ctl: {self.keymap_file_name}')
        # gpio pin is useless here. we are bound by the system configuration

    def send(self , data: str) -> None:
        param_keymap = f'--keymap={self.keymap_file_name}'
        param_keycode = f'--keycode={data}'
        param_other = f'--verbose'
        try: 
            subprocess.run(['ir-ctl' , param_keymap , param_keycode , param_other])
        except subprocess.CalledProcessError as e:
            print('Unable to send the scancode!')
            print (e.output)


