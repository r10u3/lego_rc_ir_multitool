# Lego:tm: Power Functions & Raspberry Pi
<em>Last updated: 9/29/2023</em>
## Introduction

This project is part of using a Raspberry Pi as a [Lego:tm: PowerFunctions](#legotm-protocol) controller. 

There are three IR tools that I found that work with Python and I use in this project:
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
   - PiIR is a client program for pigpio, the excellent hardware-timed GPIO library. Some code are taken from its sample program irrp.py.
   - It records and plays IR remote control code.
   - It decodes and encodes NEC, Sony, RC5, RC6, AEHA, Mitsubishi, Sharp and Nokia formats.
   - It dumps decoded and prettified data to help you analyze your air conditioner's remote.
   - It provides both command-line and programmatic control.
   - [PiIR 0.2.5](https://pypi.org/project/PiIR/) by Takeshi Sone

## Setup
> **Notes:**
>
> You can find more detailed information on how to set up the project in the docs section. Relevant documents are:
> - setup.md: shows the initial steps
> - setup_lirc.md: shows how to set up LIRC
> - setup_ir-ctl.md: shows how to set up <code>ir-ctl</code>
> - setup_piir: shows how to set up PiIR

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
#### a. Install PiIR
```
sudo pip3 install PiIR
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

### 5. Reboot
```
sudo reboot
```

### 6. Copy/extract project
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

### 7. Test
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
irsend SEND_ONCE combo_pwm_ch1_26ns FW2A_FW2B
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

## IR Multitool Configuration

### Config file
<code>config.json</code>
```
{
    "project_folder" : "/home/pi/Projects/lego_rc_0_0_2",
    "maps_config_file" : "maps/maps_config.json",
    "rc_mode" : "SGL",
    "ir_tool" : "ir_ctl",
    "gpio_pin" : 18
}
```
#### <code>project_folder</code>
This is the absolute path to the project. It is not really used anywhere

#### <code>maps_config_file</code>
This is quite important. If you move the config file, make sure to modify here. I recommend you leave it where it is.

The <code>maps_config_file</code> file has links to keymaps and button maps. If you change the names of the keymaps or use different ones, make sure to update the <code>maps_config_file</code>.

#### <code>rc_mode</code>
The available modes are:
   - PWM: Combo PWM
   - DIR: Combo Direct
   - SGL: Single PWM
   - OTH: Single Clear/Set/Toggle/Inc/Dec (doesn't work)
   - EXT: Extended (not implemented)

#### <code>ir_tool</code>
The available tools are:
   - lirc
   - ir_ctl
   - piir

#### <code>gpio_pin</code>
PIN must be Hardware PWM. "The maximum [software] PWM output frequency is 8 KHz using writePWMFrequency(mypi, 12, 8000)."[^1] Lego uses 38KHz.

### Button Maps
The keys are configured in the <code>maps/button_maps</code> folder. One file per rc mode. Each mode has its own set of key mappings. I only coded for the red output in most cases. Here are some comparative examples:

|  Key    | Combo PWM | Combo Direct | Single PWM |
| ------- | --------- | ------------ | ---------- |
| &uarr;  | INC       | FWD | INC |
| &darr;  | DEC       | REV | DEC |
| SPACE BAR | BRK     | BRK | BRK |
| 'l'     | FLT       | FLT | FLT |
| '1'     | FW1       | n/a | FW1 |
| '2'     | FW2       | n/a | FW2 |
| ...     | ...       | ... | ... |
| '7'     | FW7       | n/a | FW7 |
| 'a'     | RV1       | n/a | RV1 |
| 'b'     | RV2       | n/a | RV2 |
| ...     | ...       | ... | ... |
| 'g'     | RV7       | n/a | RV7 |
| Noteworthy |-Both outputs simultaneously<br />-Speeds -7..+7<br />-Only one second|-Both outputs simultaneously<br />-Speeds Full Forward, Full Backward, Float, Break only<br />-Only one second | -One output at a time<br />-Speeds -7..+7<br />-Permanent state until new key changes it |

One important difference between the Single PWM and both Combo modes is that with Single, the state is permanent. When you press a key, the motor starts and keeps going. With the combo modes, the motor moves only for about a second and stops. You need to keep sending keys to keep the motor going.

### Keymaps
Every tool has its own different keymap format. They all have a header with basic protocol parameters followed by scancode-keycode pairs. But each has a different format:
* LIRC: lirc keymaps have a .conf extension and follow the basic rules of configuration files
* ir-ctl: uses the [toml](https://toml.io/en/) format
* PiIR: uses json files

The common parameters in the header include (the names might change from one format to another but the meaning remains):
* header_pulse = 158
* header_space = 1026
* bit_pulse = 158
* bit_0_space = 263
* bit_1_space = 553
* trailer_pulse = 158
* bits = 16
* carrier = 38000

You can find more detailed descriptions of each file format in each tool's setup file.

## Multitool API
If you want to use parts of this project as an API, you can do without the <code>lego.py</code> file and access the objects directly. Here is a description of each object and their methods

### Power Functions (Encoders)
#### Features
* There are four types (classes):
  * Combo_PWM
  * Combo_Direct
  * Single_PWM
  * Single_Other
  * Extended is not coded yet
* All have the same methods and attributes with the same signatures
* Keep track of current speeds for red and blue outputs (only red is functional though)
* Perform actions:
  * set speed
  * change speed in increments
* Provide keycode corresponding to self reported speeds

#### Methods
##### New Object
Does not require any parameters. The methods to create each type of object are:
```
import power_functions.combo_pwm as pf
rc_encoder = pf.Combo_PWM()
```
or
```
import power_functions.combo_direct as pf
rc_encoder = pf.Combo_Direct()
```
or
```
import power_functions.single_pwm as pf
rc_encoder = pf.Single_PWM()
```
or
```
import power_functions.single_other as pf
rc_encoder = pf.Single_Other()
```

##### <code>action(key: str) -> keycode: str</code>
Returns <code>keycode</code>. Key must exist in keymap.json. Actions programmed are:
* break then float=‘BRK’
* increment speed=‘INC’
* decrement speed= ‘DEC’
* float= ‘FLT’
* set speed (-7..+7) except Combo Direct which does not support intermediate speeds.
```
rc_encoder.action(key)
```

##### <code>speed_change(color: str , increment: int) -> keycode: str</code>
Change speed by increments. Returns <code>keycode</code>.
The range of speeds is -7 - +7. Float is 0. If <code>abs(state[color] + increment) > 7</code> it will not change speed and return the keycode for the current speed.
The Combo Direct mode only supports full forward and full backward. It does not support intermediate speeds.
```
rc_encoder.speed_change(color, increment)
```

##### <code>set_speed(color: str , speed: int) -> keycode: str</code>
Sets speed. Returns <code>keycode</code>.
* The range of speeds is -7 to +7 (except Combo Direct)
* 0 is Float
* -99: break then float
```
rc_encoder.set_speed(color , speed)
```

#### Other functions

##### <code>get_keycode(speed_red: int , speed_blue: int) -> keycode: str</code>
Get keycode for red-blue combo speeds. Returns <code>keycode</code>
```
rc_encoder.get_keycode(speed_red , speed_blue)
```

[^1]: [Raspberry Pi PWM, MathWorks](https://www.mathworks.com/help/supportpkg/raspberrypiio/ug/the-raspberry-pi-pwm.html)
