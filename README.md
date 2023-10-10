# Lego:tm: Power Functions & Raspberry Pi
<em>Last updated: 10/9/2023</em>
## Introduction

This project is part of using a Raspberry Pi as a [Lego:tm: PowerFunctions](#legotm-protocol) controller. 
> **Note:** Technically, the app can use any remote. Except for the pigpio which is only coded for pulse distance encoding.

There are four IR tools that I found that work with Python and I use in this project:
* LIRC:
  - LIRC is a package that allows you to decode and send infra-red signals of many (but not all) commonly used remote controls.
  - Recent linux kernels makes it possible to use some IR remote controls as regular input devices. Sometimes this makes LIRC redundant. However, LIRC offers more flexibility and functionality and is still the right tool in a lot of scenarios.
  - The most important part of LIRC is the lircd daemon which decodes IR signals received by the device drivers and provides the information on a socket. It also accepts commands for IR signals to be sent if the hardware supports this.
  - [lirc.org](https://www.lirc.org/)
* <code>ir-ctl</code>
  - ir-ctl is a tool that allows one to list the features of a lirc device, set its options, receive raw IR, and send IR.
  - IR can be sent as the keycode of a keymap, or using a scancode, or using raw IR.
  - [<code>ir-ctl</code> - Man Page](https://www.mankier.com/1/ir-ctl)
* PiIR
   - PiIR is a client program for pigpio, a hardware-timed GPIO library. Some code are taken from its sample program irrp.py.
   - It records and plays IR remote control code.
   - It decodes and encodes NEC, Sony, RC5, RC6, AEHA, Mitsubishi, Sharp and Nokia formats.
   - It dumps decoded and prettified data to help you analyze your air conditioner's remote.
   - It provides both command-line and programmatic control.
   - [PiIR 0.2.5](https://pypi.org/project/PiIR/) by Takeshi Sone
* pigpio
   - "pigpio is a library for the Raspberry which allows control of the General Purpose Input Outputs (GPIO).  pigpio works on all versions of the Pi." [^1]
   - Among other things, it allows waveforms to generate GPIO level changes (time accurate to a few &mu;s)
   - I developed a custom object to handle the codes.
   - With almost direct access to the GPIO.
 
In comparing speeds roughly by eye, there is no noticeable difference between the tools. New keys are almost instantaneous, while repeated keys seem limited by sshkeyboard. This poses a limitation for increment/decrement where it takes multiple keystrokes of the same key to reach a particular speed.

## Setup
> **Notes:**
>
> You can find more detailed information on how to set up the project in the docs section. Relevant documents are:
> - setup.md: shows the initial steps
> - setup_lirc.md: shows how to set up LIRC and details on how it works
> - setup_ir-ctl.md: shows how to set up <code>ir-ctl</code> and details on how it works
> - setup_piir: shows how to set up PiIR and details on how it works
> - setup_pigpio: shows how to set up pigpio and details on how it works

The basic steps for the setup are:
### 1. Edit /boot/config.txt and reboot
```
# Uncomment this to enable infrared communication.
dtoverlay=pwm-ir-tx,gpio_pin=18
```
```
sudo reboot
```
### 2. Setup LIRC
#### a. Install LIRC
```
sudo apt-get install lirc
```
#### b. Edit <code>/etc/lirc/lirc_options.conf</code>
```
driver = default
device = /dev/lirc0
```
#### c. Start service and check
```
sudo systemctl start lircd.socket lircd.service
```
```
sudo systemctl status lirc.service
```
#### d. Install LIRC Python
```
sudo pip3 install lirc
```

### 3. Setup <code>ir-ctl</code>
#### a. Check if ir-ctl is installed by default.
```
ir-ctl -f
```
#### b. Install <code>v4l-utils</code> if <code>ir-ctl</code> is not installed
```
sudo apt-get install v4l-utils
```

### 4. Setup PiIR
#### a. Install pigpio
```
sudo apt-get install pigpio python-pigpio python3-pigpio
```

#### b. Start pigpio daemon and check status
```
sudo systemctl enable pigpiod
```
```
sudo systemctl start pigpiod
```
```
sudo systemctl status pigpiod
```

#### c. Install PiIR
```
sudo pip3 install PiIR
```

### 5. Setup RPiGPIO
This tool also uses pigpio, so you should have already performed these steps. If you pick and choose your tools, these steps would required to use RPiGPIO. But only if you didn't do it already.
#### a. Install pigpio
```
sudo apt-get install pigpio python-pigpio python3-pigpio
```

#### b. Start pigpio daemon and check status
```
sudo systemctl enable pigpiod
```
```
sudo systemctl start pigpiod
```
```
sudo systemctl status pigpiod
```

### 6. Reboot
```
sudo reboot
```

### 7. Install sshkeyboard
The app (lego.py) uses sshkeyboard for input capture over SSH. I am using a headless RPi over SSH. If you use a different configuration or create your own app, you can skip this step. You will need to install the appropriate capture tool for your platform configuration.

### 8. Copy/extract project
#### a. Download and extract
Use your favorite tool to do this

#### b. Copy LIRC Keymap Files to <code>/etc/lirc/lircd.conf.d/</code>
LIRC expects all files to be located at /etc/lirc/lircd.conf.d/. 

```
sudo cp -r [project folder]/maps/keymaps/lirc /etc/lirc/lircd.conf.d/
```
We also hide <code>devinput.lircd.conf</code>. This is not necessary, but reduces bloat by loading less remotes 
```
sudo mv /etc/lirc/lircd.conf.d/devinput.lircd.conf /etc/lirc/lircd.conf.d/devinput.lircd.conf.dist
```

### 9. Test
#### a. Test LIRC
List all the available remotes.
```
irsend LIST "" ""
```
List all the available codes for a particular remote
```
irsend LIST "combo_pwm_ch1_26ns" ""
```
Send a sample code
```
irsend SEND_ONCE combo_pwm_ch1_26ns FW2_FW2
```
#### b. Test ir-ctl
First, navigate to the project's directory. Then send key with ir-ctl
```
ir-ctl –-keymap=maps/keymaps/ir_ctl/combo_pwm_ch1_26ns.toml --keycode=FW2A_FW2B --verbose
```

#### c. Test PiIR
Send a sample code. Again, first navigate to the project's directory.
```
piir play --gpio 18 --file maps/keymaps/piir/combo_pwm_ch1_26ns.json FW2_FW2
```

#### c. Test rpigpio
Send a sample code. Again, first navigate to the project's directory.
```
python -c 'import ir_tools.rpigpio as irt; irt.test_send("maps/keymaps/rpigpio/combo_pwm_ch1_26ns.json" , 18 , "FW2_FW2")'
```

## IR Multitool Configuration

### 1. Config file
<code>config.json</code>
```
{
    "project_folder" : "/home/pi/Projects/lego_rc_0_0_2",
    "maps_config_file" : "maps/maps_config.json",
    "rc_mode" : "SGL",
    "ir_tool" : "rpigpio",
    "GPIO" : 18
}
```
#### a. <code>project_folder</code>
This is the absolute path to the project. It is not really used anywhere

#### b. <code>maps_config_file</code>
This is quite important. If you move the config file, make sure to modify here. I recommend you leave it where it is.

The <code>maps_config_file</code> file has links to keymaps and button maps. If you change the names of the keymaps or use different ones, make sure to update the <code>maps_config_file</code>.

#### c. <code>rc_mode</code>
The available modes are:
   - PWM: Combo PWM
   - DIR: Combo Direct
   - SGL: Single PWM
   - EXT: Extended
   - OTH: Single Clear/Set/Toggle/Inc/Dec (doesn't work)

#### d. <code>ir_tool</code>
The available tools are:
   - lirc
   - ir_ctl
   - piir
   - rpigpio (the 'r' prefix is there to distinguish it from the pigpio library when it's imported)

#### e. <code>gpio_pin</code>
PIN must be Hardware PWM. "The maximum [software] PWM output frequency is 8 KHz using writePWMFrequency(mypi, 12, 8000)."[^2] Lego uses 38KHz.

### 2. Button Maps
The keys are configured in the <code>maps/button_maps</code> folder. One file per rc mode. Each mode has its own set of key mappings. I only coded for the red output in most cases. Here are some comparative examples:

|  Key         |  Combo PWM   | Combo Direct |  Single PWM  |   Extended   |
| ------------ | ------------ | ------------ | ------------ | ------------ |
| &uarr;  | INC       | FWD | INC | INC |
| &darr;  | DEC       | REV | DEC | DEC |
| SPACE BAR | BRK     | BRK | BRK | BRK |
| 'l'     | FLT       | FLT | FLT | n/a |
| '1'     | FW1       | n/a | FW1 | n/a |
| '2'     | FW2       | n/a | FW2 | n/a |
| ...     | ...       | ... | ... | ... |
| '7'     | FW7       | n/a | FW7 | n/a |
| 'a'     | RV1       | n/a | RV1 | TOG_ADDR |
| 'b'     | RV2       | n/a | RV2 | TOG_B |
| ...     | ...       | ... | ... | ... |
| 'g'     | RV7       | n/a | RV7 | n/a |
| Noteworthy |<p>&bull; Both outputs simultaneously</p><p>&bull; Speeds -7&#184;&#184;+7</p><p>&bull; Only one second</p>|<p>&bull; Both outputs simultaneously</p><p>&bull; Speeds Full Forward, Full Backward, Float, Break only</p><p>&bull; Only one second</p> | <p>&bull; One output at a time</p><p>&bull; Speeds -7&#184;&#184;+7</p><p>&bull; Permanent state until new key changes it</p> | <p>&bull; One output at a time</p><p>&bull; Red speeds -7&#184;&#184;+7, blue speeds Full Forward/Float</p><p>&bull; Permanent state until new key changes it</p><p>&bull; Toggle address bit, but doesn't accept <em>extended</em> commands with <code>address bit = 1</code> |

One important difference between the Single PWM and both Combo modes is that with Single, the state is permanent. When you press a key, the motor starts and keeps going. With the combo modes, the motor moves only for about a second and stops. You need to keep sending keys to keep the motor going.

### 3. Keymaps
Every tool has its own different keymap format. They all have a header with basic protocol parameters followed by scancode-keycode pairs. But each has a different format:
* LIRC: lirc keymaps have a <code>[.conf](https://www.lirc.org/html/lircd.conf.html)</code> extension and follow the basic rules of configuration files. Example for [Combo PWM](maps/keymaps/lirc/combo_pwm_ch1_26ns.conf).
* ir-ctl: uses the <code>[toml](https://toml.io/en/)</code> format. Example for [Combo PWM](maps/keymaps/ir_ctl/combo_pwm_ch1_26ns.toml).
* PiIR: uses json files. Example for [Combo PWM](maps/keymaps/piir/combo_pwm_ch1_26ns.json).
* PiGPIO: uses json files. Example for [Combo PWM](maps/keymaps/rpigpio/combo_pwm_ch1_26ns.json).

The common parameters in the header include (the names and format might change from one format to another but the meaning and values remain):

| Parameter | Value[^3] | Unit | Cycles[^4] | Notes |
|-----------|-------|------|--------|-------|
| carrier | 38000 | Hz | n/a | |
| cycle length | 26 | &mu;s | 1 | 1/carrier<br />**Note:** Not included as parameter, just for information purposes. Used by rpigpio to design waves. |
| header_pulse | 158 | &mu;s | 6 | 6 x cycle length |
| header_space | 1026 | &mu;s | 39 | 39 x cycle length |
| bit_pulse | 158 | &mu;s | 6 | 6 x cycle length |
| bit_0_space | 263 | &mu;s | 10 | 10 x cycle length |
| bit_1_space | 553 | &mu;s | 21 | 21 x cycle length |
| trailer_pulse | 158 | &mu;s | 6 | 6 x cycle length |
| bits | 16 | n/a | | |
[^3]: Used by LIRC and <code>ir-ctl</code>
[^4]: Used by PiIR and RPiGPIO

You can find more detailed descriptions of each file format in each tool's setup file in the <code>docs</code> folder.

## Multitool API
If you want to use parts of this project as an API, you can do without the <code>lego.py</code> file and access the objects directly. Here is a description of each object and their methods

### 1. Keypad
#### a. Features
* The <code>keypad</code> maps buttons to actions.
* Note that the <code>keypad</code> does not match buttons to keycodes; the <code>power_functions</code> (or encoders) do that while keeping track of state. The reason is that we can have keys that don't map to codes. For example, in the Combo PWM <code>button_map</code> (where the mappings are configured) there is a button map for 'INC' (increment), but there is no such code in the Lego protocol for the Combo PWM mode. The <code>Combo_PWM</code> object creates the corresponding code by calculating the speed = current speed + 1.

#### b. Methods
##### &#x25B6; New Object: <code>Keypad(mapped_keys_file_name: str) -> Keypad</code>
The required parameters are:
* **<code>mapped_keys_file_name</code>:** from <code>maps/maps_config.json</code>.
```
import keypad

kb = keypad.Keypad(button_maps_file_name)
```

##### &#x25B6; <code>is_mapped_key(self , key: str) -> bool</code>
Checks whether a particular key (e.g., &uarr;) is in the button map. Return a boolean.

##### &#x25B6; <code>get_action(self , key: str) -> [str , str]</code>
Returns the action associated to a particular key. The action is an array with [color , action] pairs.


### 2. IR Tools
#### a. Features
* There are four types (classes):
  * LIRC
  * ir-ctl
  * PiIR
  * RPiGPIO

* All have the same methods and attributes with the same signatures
* Send code to tool to be transmitted

#### b. Methods
##### &#x25B6; New Object: <code>Tool(keymap_file_name: str, keymap_folder_name: str,  gpio_pin: str) -> Tool</code>
Require the following arguments:
* **keymap_file_name:** from <code>maps/maps_config.json</code>. Used by <code>ir-ctl</code> and PiIR to locate the keymap. <code>LIRC</code> uses remote names instead of keymap files. The remote name inside the keymap file should match the name of the keymap file minus the extension.
* **keymap_folder_name:** from <code>maps/maps_config.json</code>. Used by <code>ir-ctl</code> and PiIR to locate the keymap. <code>LIRC</code> keymaps are all located at <code>/etc/lirc/lircd.conf.d</code>
* **gpio_pin:** from <code>config.json</code>. Used by PiIR. <code>LIRC</code> and <code>ir-ctl</code> use the pin configured in the <code>/boot/config.txt</code> file.
The methods to create each type of object are:
```
import ir_tools.ir_ctl as irt
remote_tx = irt.IR_ir_ctl(REMOTE_KEYMAP_FILE_NAME , REMOTE_KEYMAP_FOLDER_NAME , GPIO_PIN)
```
```
import ir_tools.lirc as irt
remote_tx = irt.IR_LIRC(REMOTE_KEYMAP_FILE_NAME , REMOTE_KEYMAP_FOLDER_NAME , GPIO_PIN)
```
```
import ir_tools.piir as irt
remote_tx = irt.IR_PiIR(REMOTE_KEYMAP_FILE_NAME , REMOTE_KEYMAP_FOLDER_NAME , GPIO_PIN)
```
```
import ir_tools.rpigpio as irt
remote_tx = irt.RPiGPIO(REMOTE_KEYMAP_FILE_NAME , REMOTE_KEYMAP_FOLDER_NAME , GPIO)
```

##### &#x25B6; send(data: str) -> None:
It converts a keycode (e.g., 'FW2_FW2') to scancode (e.g., 0x422B) and sends it.
Arguments:
* **data:** this is the keycode. For example 'FW2_FW2'

##### &#x25B6; send_x(data_bytes: str) -> None:
This method is unique to PiIR and RPiGPIO. It takes a scancode in hexadecimal string format (e.g., '42 2B') and sends it.
> **Note:** PiIR reverses the bits in each byte, so you need to pre-process the data to be sent. This is not the case with RPiGPIO, which was custom coded for this application.
Arguments:
* **data_bytes:** the scancode as an hexadecimal string.

##### &#x25B6; send_scancode(data: int) -> None:
This method is unique to RPiGPIO. It takes a scancode in integer format (e.g., 16939 or 0x422B), and sends it. The code must be a valid code. The method does not check for validity. The code is sent anyway and the receiver will reject it without any error.
Arguments:
* **data_bytes:** the scancode as an integer.

### 3. Power Functions (Encoders)
#### a. Features
* There are four types (classes):
  * Combo_PWM
  * Combo_Direct
  * Single_PWM
  * Extended
  * Single_Other (doesn't work)
* All have the same methods and attributes with the same signatures
* Keep track of current speeds for red and blue outputs. Only red is functional though, except for <em>Extended</em> mode.
* Perform actions:
  * set speed
  * change speed in increments
  * in some cases toggle between full forward and float
* Provide keycode corresponding to self reported speeds

#### b. Methods
##### &#x25B6; New Object
Does not require any parameters. The methods to create each type of object are:
```
import power_functions.combo_pwm as pf
rc_encoder = pf.Combo_PWM()
```
```
import power_functions.combo_direct as pf
rc_encoder = pf.Combo_Direct()
```
```
import power_functions.single_pwm as pf
rc_encoder = pf.Single_PWM()
```
```
import power_functions.single_other as pf
rc_encoder = pf.Single_Other()
```

##### &#x25B6; <code>action(key: str) -> keycode: str</code>
Returns <code>keycode</code>. Key must exist in keymap.json. Actions programmed are:
* break then float=‘BRK’
* increment speed=‘INC’
* decrement speed= ‘DEC’
* float= ‘FLT’
* set speed (-7&#184;&#184;+7) except Combo Direct which does not support intermediate speeds.
```
rc_encoder.action(key)
```

##### &#x25B6; <code>speed_change(color: str , increment: int) -> keycode: str</code>
Change speed by increments. Returns <code>keycode</code>.
The range of speeds is -7&#184;&#184;+7. Float is 0. If <code>abs(state[color] + increment) > 7</code> it will not change speed and return the keycode for the current speed.
The Combo Direct mode only supports full forward and full backward. It does not support intermediate speeds.
```
rc_encoder.speed_change(color, increment)
```

##### &#x25B6; <code>set_speed(color: str , speed: int) -> keycode: str</code>
Sets speed. Returns <code>keycode</code>.
* The range of speeds is -7&#184;&#184;+7 (except Combo Direct)
* 0 is Float
* -99: break then float
```
rc_encoder.set_speed(color , speed)
```

##### &#x25B6; <code>get_keycode(speed_red: int , speed_blue: int) -> keycode: str</code>
Get keycode for red-blue combo speeds. Returns <code>keycode</code>
```
rc_encoder.get_keycode(speed_red , speed_blue)
```

[^1]: [The pigpio library](https://abyz.me.uk/rpi/pigpio/), joan@abyz.me.uk
[^2]: [Raspberry Pi PWM, MathWorks](https://www.mathworks.com/help/supportpkg/raspberrypiio/ug/the-raspberry-pi-pwm.html)
