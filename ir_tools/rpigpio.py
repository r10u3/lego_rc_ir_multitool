import pigpio
import json

def test_send(config_file_name_and_path , GPIO , keycode):
    x = config_file_name_and_path.rfind('/')
    if (x == -1):
        config_file_folder = ''
        config_file_name = config_file_name_and_path
    else:
        config_file_folder = config_file_name_and_path[0:x]
        config_file_name = config_file_name_and_path[x+1:]

    my_pigpio = PiGPIO(config_file_name , config_file_folder , GPIO)
    my_pigpio.send(keycode)

class PiGPIO:

    def __init__(self: any , keymap_file_name: str, keymap_folder_name: str,  GPIO: str) -> None:
        with open(keymap_folder_name + '/' + keymap_file_name, 'r') as config_file:
            config = json.loads(config_file.read())

        frequency          = config['parameters']['frequency']
        pulse_length       = config['parameters']['pulse']
        start_space_length = config['parameters']['heading']
        zero_space_length  = config['parameters']['zero']
        one_space_length   = config['parameters']['one']
        stop_space_length  = config['parameters']['trailing']
        self.bits          = config['parameters']['bits']
        self.keymap        = config['keycodes']
        self.__config(GPIO , frequency , pulse_length , start_space_length , zero_space_length, one_space_length , stop_space_length)
        print(f'Remote: rpigpio: {keymap_file_name}')

    def __config(self , GPIO , frequency , pulse_length , start_space_length , zero_space_length, one_space_length , stop_space_length) -> None:
        self.pi = pigpio.pi()       # pi1 accesses the local Pi's GPIO
        self.pi.set_mode(GPIO, pigpio.OUTPUT)

        start_delay = int(1000000 / frequency * start_space_length)
        zero_delay  = int(1000000 / frequency * zero_space_length )
        one_delay   = int(1000000 / frequency * one_space_length  )
        stop_delay  = int(1000000 / frequency * stop_space_length  )

        #                            ON       OFF      DELAY
        START_SPACE = pigpio.pulse(   0   ,    0 ,   start_delay)
        ZERO_SPACE  = pigpio.pulse(   0   ,    0 ,   zero_delay )
        ONE_SPACE   = pigpio.pulse(   0   ,    0 ,   one_delay  )
        STOP_SPACE  = pigpio.pulse(   0   ,    0 ,   stop_delay )

        self.pi.wave_clear() # clear any existing waveforms

        start_wave_generic = self.append_pulse(GPIO , frequency , pulse_length)
        start_wave_generic.append(START_SPACE)
        zero_wave_generic = self.append_pulse(GPIO , frequency , pulse_length)
        zero_wave_generic.append(ZERO_SPACE)
        one_wave_generic = self.append_pulse(GPIO , frequency , pulse_length)
        one_wave_generic.append(ONE_SPACE)
        stop_wave_generic = self.append_pulse(GPIO , frequency , pulse_length)
        stop_wave_generic.append(STOP_SPACE)

        self.pi.wave_add_generic(start_wave_generic)
        self.start_wave = self.pi.wave_create() # create and save id
        self.pi.wave_add_generic(zero_wave_generic)
        self.zero_wave = self.pi.wave_create() # create and save id
        self.pi.wave_add_generic(one_wave_generic)
        self.one_wave = self.pi.wave_create() # create and save id
        self.pi.wave_add_generic(one_wave_generic)
        self.stop_wave = self.pi.wave_create() # create and save id

    def append_pulse(self , GPIO: int, carrier: int, cycles: int) -> pigpio.pulse:
        half_cycle = int(1000000  / carrier / 2)
        #                            ON       OFF      DELAY
        cycle_on    = pigpio.pulse(1<<GPIO,    0   , half_cycle )
        cycle_off   = pigpio.pulse(   0   , 1<<GPIO, half_cycle )
        pulse = []
        for i in range(cycles):
            pulse.append(cycle_on)
            pulse.append(cycle_off)
        return pulse

    def append_scancode(self , wave_chain , scancode : int):
        for bit in scancode:
            if bit == '0':
                wave_chain.append(self.zero_wave)
            elif bit == '1':
                wave_chain.append(self.one_wave)
            else:
                raise Exception(f'Sorry, character {bit} is not a bit')
        return wave_chain

    def send_scancode(self , data: int) -> pigpio.pi.wave_chain:
        bin_data = bin(data)[2:].zfill(self.bits)
        print(bin_data)
        wave_chain = []
        wave_chain.append(self.start_wave)
        wave_chain = self.append_scancode(wave_chain , bin_data)
        wave_chain.append(self.stop_wave)
        print(wave_chain)
        self.pi.wave_tx_stop()
        self.pi.wave_chain(wave_chain)
        return wave_chain
    
    def send_x(self , data: str) -> pigpio.pi.wave_chain:
        scancode = int(data , 16)
        self.send_scancode(scancode)


    def send(self , keycode: str) -> None:
        scancode_str = self.keymap[keycode]
        scancode = int(scancode_str , 16)
        self.send_scancode(scancode)