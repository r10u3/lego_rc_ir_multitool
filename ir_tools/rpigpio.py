import pigpio
import json

def test_send(config_file_name_and_path, GPIO, keycode):
    x = config_file_name_and_path.rfind('/')
    if x == -1:
        config_file_folder = ''
        config_file_name = config_file_name_and_path
    else:
        config_file_folder = config_file_name_and_path[0:x]
        config_file_name = config_file_name_and_path[x+1:]

    my_pigpio = RPiGPIO(config_file_name, config_file_folder, GPIO)
    my_pigpio.send(keycode)

class RPiGPIO:

    def __init__(self,  GPIO: int = 18, keymap_file_name: str = 'single_pwm.json',
                 keymap_folder_name: str = 'maps/keymaps/rpigpio') -> None:
        """Uses pigpio library to format and send IR codes.

        Args:
            GPIO (int): PIN must be Hardware PWM.
                Default = 18.
            keymap_file_name (str): the name of the file 
                containing the keymap.
                Default = 'single_pwm.json'.
            keymap_folder_name (str): the name of the file 
                containing the keymap. Can be absolute or relative.
                Default = 'maps/keymaps/rpigpio'.
        """
        keymap_file = keymap_folder_name + '/' + keymap_file_name
        with open(keymap_file, 'r') as config_file:
            config = json.loads(config_file.read())

        frequency          = config['parameters']['frequency']
        pulse_length       = config['parameters']['pulse']
        start_space_length = config['parameters']['heading_space']
        zero_space_length  = config['parameters']['zero_space']
        one_space_length   = config['parameters']['one_space']
        stop_space_length  = config['parameters']['trailing_space']
        self.bits          = config['parameters']['bits']
        self.keymap        = config['keycodes']

        start_delay = int(1000000 / frequency * start_space_length)
        zero_delay  = int(1000000 / frequency * zero_space_length )
        one_delay   = int(1000000 / frequency * one_space_length  )
        stop_delay  = int(1000000 / frequency * stop_space_length  )

        self.pi = pigpio.pi()
        self.pi.set_mode(GPIO, pigpio.OUTPUT)
        #                          ON  OFF    DELAY
        START_SPACE = pigpio.pulse( 0, 0, start_delay)
        ZERO_SPACE  = pigpio.pulse( 0, 0, zero_delay )
        ONE_SPACE   = pigpio.pulse( 0, 0, one_delay  )
        STOP_SPACE  = pigpio.pulse( 0, 0, stop_delay )

        self.pi.wave_clear() # clear any existing waveforms

        start_wave_generic = self._append_pulse(GPIO, frequency, pulse_length)
        start_wave_generic.append(START_SPACE)
        zero_wave_generic = self._append_pulse(GPIO, frequency, pulse_length)
        zero_wave_generic.append(ZERO_SPACE)
        one_wave_generic = self._append_pulse(GPIO, frequency, pulse_length)
        one_wave_generic.append(ONE_SPACE)
        stop_wave_generic = self._append_pulse(GPIO, frequency, pulse_length)
        stop_wave_generic.append(STOP_SPACE)

        self.pi.wave_add_generic(start_wave_generic)
        self.start_wave = self.pi.wave_create()
        self.pi.wave_add_generic(zero_wave_generic)
        self.zero_wave = self.pi.wave_create()
        self.pi.wave_add_generic(one_wave_generic)
        self.one_wave = self.pi.wave_create()
        self.pi.wave_add_generic(one_wave_generic)
        self.stop_wave = self.pi.wave_create()
    
    def _append_pulse(self, 
                      GPIO: int,
                      carrier: int,
                      cycles: int) -> [pigpio.pulse]:
        half_cycle = int(1000000  / carrier / 2)
        #                            ON      OFF      DELAY
        cycle_on    = pigpio.pulse(1<<GPIO,   0  , half_cycle )
        cycle_off   = pigpio.pulse(   0 , 1<<GPIO, half_cycle )
        pulse = []
        for i in range(cycles):
            pulse.append(cycle_on)
            pulse.append(cycle_off)
        return pulse

    def _append_scancode(self, wave_chain, scancode: str):
        for bit in scancode:
            if bit == '0':
                wave_chain.append(self.zero_wave)
            elif bit == '1':
                wave_chain.append(self.one_wave)
            else:
                error = f'Sorry, character {bit} is not a bit'
                raise Exception(error)
        return wave_chain

    def send_raw(self, data: int) -> None:
        """Send IR using pigpio.
        
        Args:
            data_int (int): the scancode to be sent in int format.
                Can be int, hexadecimal (0x) or binary (0b).
        """
        self.pi.wave_tx_stop()
        bin_data = bin(data)[2:].zfill(self.bits)
        wave_chain = []
        wave_chain.append(self.start_wave)
        wave_chain = self._append_scancode(wave_chain, bin_data)
        wave_chain.append(self.stop_wave)
        self.pi.wave_chain(wave_chain)
    
    def send_hex(self, data: str) -> None:
        """Send IR using pigpio.
        
        Args:
            data_bytes (str): the scancode to be sent 
                in hexadecimal string format.
        """
        scancode = int(data, 16)
        self.send_raw(scancode)

    def send(self, keycode: str) -> None:
        """Send IR using pigpio.
        
        Args:
            keycode (str): the keycode to be sent.
        """
        scancode_str = self.keymap[keycode]
        scancode = int(scancode_str, 16)
        self.send_raw(scancode)
