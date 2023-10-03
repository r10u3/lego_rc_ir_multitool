# Lego:tm: Power Functions & Raspberry Pi
<em>Last updated: 9/29/2023</em>
## Introduction

This project is part of using a Raspberry Pi as a [Lego:tm: PowerFunctions](#legotm-protocol) controller. There are many tutorials that do something similar. Most use LIRC. Some are outdated.

In this tutorial we use <a href="https://pypi.org/project/PiIR/">PiIR</a>.  PiIR is a remote control for Raspberry Pi. It is a client program for pigpio, a hardware-timed GPIO library.

## Preparation

#### Install sshkeyboard
> **Note:** Installation of Python packages take a while, so be patient.

```
sudo pip3 install sshkeyboard
```

#### Unload and decompress
The file <code>Lego_RC_PiIR_0_0_1_beta.tar.gz</code> has all the packages included in this project. Unzip it to any folder and run
```
python app.py
```

#### Setup <code>/boot/conifig.txt</code>
I have previously set up pin 18 as <code>pwm-ir-tx</code> in <code>/boot/config.txt</code>. I am not aware if this is necessary, I did it before I started with PiIR.
```
sudo nano /boot/config.txt
``` 
```
# Uncomment this to enable infrared communication.
#dtoverlay=gpio-ir,gpio_pin=17
dtoverlay=pwm-ir-tx,gpio_pin=18
```

## Simple Lego_PiIR API

### Setup
We include a very simple app that uses <code>sshkeyboard</code> to capture keyboard strokes. The keys are configured in the <code>maps/button_maps</code> folder. One file per rc mode. Each mode has its own set of key mappings. I only coded for the red output in most cases. Here are some comparative examples:

|  Key    | Combo PWM | Combo Direct | Single PWM |
| ------- | --------- | ------------ | ---------- |
| &uarr;  | INC       | | |
| &darr;  | DEC       | | |
| SPACE BAR | BRK     | | |
| 'l'     | FLT       | | |


#### App Imports
Use this code if you are building your own app and using the Power Functions modules. 

> **Note:** Make sure that your module matches the module **mode** in the config file.

```
import power_functions.config as cfg
config_file = 'config.json'
cfg.config(config_file)

# comment this if you are bypassing lego_piir_remote_simple
import lego_piir_remote_simple as rc_lego

# uncomment this if bypassing rc_lego.start_listen_pynput() 
# and accessing the power functions module directly.
# if (cfg.CONFIG['remote_mode'] == 'PWM'):
#     import power_functions.combo_pwm as pf
# elif (cfg.CONFIG['remote_mode'] == 'DIR'):
#     import power_functions.combo_direct as pf
# elif (cfg.CONFIG['remote_mode'] == 'SGL'):
#     import power_functions.single_pwm as pf
# elif (cfg.CONFIG['remote_mode'] == 'OTH'):
#     import power_functions.single_other as pf

```
With this (uncommenting the bottom block) you can access the functions defined in the module combo_pwm directly using the prefix <code>pf.</code>

#### Config file format.
> **Notes:**
> * PIN must be Hardware PWM. "The maximum [software] PWM output frequency is 8 KHz using writePWMFrequency(mypi, 12, 8000)."[^1] Lego uses 38KHz.
> * Only one channel (Channel 1) is included in the PiIR format file (<code>combo_pwm_ch1_26ns.json</code>)

The available modes are:
   - PWM: Combo PWM
   - DIR: Combo Direct
   - SGL: Single PWM
   - OTH: Single Clear/Set/Toggle/Inc/Dec (doesn't work)
   - EXT: Extended (not implemented)

<code>config.json</code>
```
{
    "gpio_pin" : 18,
    "remote_mode" : "PWM",
    "piir_maps_folder" : "/etc/lego/maps/piir_keymaps",
    "button_maps_folder" : "/etc/lego/maps/button_maps",
    "piir_format_file" : "combo_pwm_ch1_26ns.json",
    "button_map_file" : "button_map_combo.json"
}
```

#### Button Map File
I included only keys for the **red** output. Feel free to change this at your convenience. There are two button maps: a general one, and one specific to the Single Clear/Set/Toggle/Inc/Dec mode. This last one is almost like a keymap.
<code>maps/button_maps/button_map_cmb_pwm.json</code>
```
{
    "Key.space" : ["red" , "BRK"],
    "Key.up"    : ["red" , "INC"],
    "Key.down"  : ["red" , "DEC"],
    "L"         : ["red" , "FLT"],
    "0"   : ["red" , 0],
    "1"   : ["red" , 1],
    "2"   : ["red" , 2],
    "3"   : ["red" , 3],
    "4"   : ["red" , 4],
    "5"   : ["red" , 5],
    "6"   : ["red" , 6],
    "7"   : ["red" , 7],
    "A"   : ["red" , -1],
    "B"   : ["red" , -2],
    "C"   : ["red" , -3],
    "D"   : ["red" , -4],
    "E"   : ["red" , -5],
    "F"   : ["red" , -6],
    "G"   : ["red" , -7]
}
```

### Functions

#### Start keyboard capture
##### <code>rc_lego.start_listen_pynput() -> None</code>
```
rc_lego.start_listen_pynput()
```

#### Perform actions
##### <code>pf.action(key: str) -> keycode: str</code>
Returns <code>keycode</code>. Key must exist in keymap.json. Actions programmed are:
* break then float=‘BRK’
* increment speed=‘INC’
* decrement speed= ‘DEC’
* float= ‘FLT’.
```
pf.action(key)
```

#### Change/Set Speeds -> <code>keycode</code>

##### <code>pf.speed_change(color: str , increment: int) -> keycode: str</code>
Change speed by increments. Returns <code>keycode</code>.
The range of speeds is -7 - +7. Float is 0. If <code>abs(state[color] + increment) > 7</code> it will not change speed and return the keycode for the current speed.
```
pf.speed_change(color, increment)
```

##### <code>pf.set_speed(color: str , speed: int) -> keycode: str</code>
Sets speed. Returns <code>keycode</code>.
* The range of speeds is -7 to +7
* 0 is Float
* -99: break then float
```
pf.set_speed(color , speed)
```

#### Other functions

##### <code>pf.get_keycode(speed_red: int , speed_blue: int) -> keycode: str</code>
Get keycode for red-blue combo speeds. Returns <code>keycode</code>
```
pf.get_keycode(speed_red , speed_blue)
```


## PiIR
> **Note:** See [PiIR project homepage](https://pypi.org/project/PiIR/) for more information

### Installing PiIR

Install PiIR:

```
sudo pip3 install PiIR
```

Start pigpio daemon:

```
sudo systemctl enable pigpiod
```
```
sudo systemctl start pigpiod
```

### Command line usage
Send IR signal for FW2A_FW2B from cmb_pwm_ch1.json on GPIO 18.
```
piir play --gpio 18 --file /etc/lego/maps/piir_keymaps/combo_pwm_ch1_26ns.json FW2A_FW2B
```
### PiIR API
#### Instantiate the PiIR remote
> **Notes:**
> * We use GPIO 18 (pin 12), but you can use any **hardware** PWM pin. Make sure to be consistent across the project. You will need to change the config files and the <code>/boot/conf.txt</code>
> * The 26ns refers to the length of a cycle = 1/38,000 Hz
```
import piir
remote_tx = piir.Remote(CONFIG['piir_maps_folder'] + '/' + CONFIG['piir_format_file'], CONFIG['gpio_pin'])
```

#### To send the same IR signal from a python script:
```
remote_tx.send('FW2A_FW2B')
```

> **Note:** There are test files with sample keycodes and a plain format file <code>piir_26ns.json</code> which has no keycodes. It only has the basic transmission parameters for the Lego:tm: protocol. Since in our code we send keycodes, we use the complete version with keycodes.

#### You can send arbitrary data like this:
```
remote_tx.send_data('42 2B')
```
or this:
```
remote_tx.send_data(bytes([0x422B]))
```
### PiIR File Format

PiIR File Format has two main parts: a <code>format</code> section and a <code>"keys"</code> section. The protocol, in the format section, seems to follow a multiplier format, with a timebase and all definitions as multiples of the base. The keys section consists of keycode name-Hex code pairs. The following example has a format consistent with the Lego:tm: protocol followed by a sample of keys (the whole file would be too long), <em>pre-reversed</em>, for the Combo PWM mode. The whole format file is at <code>maps/piir_keymaps/combo_pwm_ch1_26ns.json</code>

```
{
  "format": {
    "preamble": [ 6, 39 ],
    "coding": "ppm",
    "zero": [ 6, 10 ],
    "one": [ 6, 21 ],
    "postamble": [ 6 ],
    "timebase": 26,
    "gap": 1026
  },
  "keys": {
    "FLTA_FLTB" : "02 D0",
    "FW1A_FLTB" : "02 58",
    "FW2A_FLTB" : "02 94",
    "FW3A_FLTB" : "02 1C",
    "FW4A_FLTB" : "02 F2",
    "FW5A_FLTB" : "02 7A",
    "FW6A_FLTB" : "02 B6",
    "FW7A_FLTB" : "02 3E"
  }
}
```

After some testing, it seems that piir converts the output of <code>FW2A_FW2B = 42 2B</code> into <code>42 D4</code>. PiIR seems to reverse bits plus reverse most and least significant bytes. As a result, we can either create keymap files that pre-reverse the bits or create the code on the fly programmatically. In this 'simple' project we go with the first option. In either case we need to pre-reverse the data as follows:
1. Convert Keycode to Bytes in Hex
1. Convert to Binary
1. Reverse Bits
1. Convert back to Bytes in Hex
1. Reverse Bytes

For example:
| Keycode | Scancode | Scancode in bits | Bits reversed | Bits Reversed in Bytes | Bytes Reversed<br />(LSB first) |
| ------- | -------- | ---------------- | ---------------- | ------- | -------- |
| FW2A_FW2B | 42 2B | 0100 0010 0010 1011 | 1101 0100 0100 0010 | D4 42 | 42 D4 |

## Lego:tm: Protocol

You can find information on Lego:tm: Power Functions RC on [Philo's page on Power Functions](https://www.philohome.com/pf/pf.htm). The protocol itself is laid out in [LEGO:tm: Power Functions RC Version 1.2](docs/LEGO_Power_Functions_RC_v120.pdf) (PDF, 370kb).

A code in the Lego:tm: protocol consists of (a) a start pulse/space, (b) sixteen –16– bits, and (c) a stop pulse/space. “Low bit consists of 6 cycles of IR and 10 “cycles” of pause, high bit of 6 cycles IR and 21 “cycles” of pause and start bit of 6 cycles IR and 39 “cycles” of pause.” All pulses are the same length in the Lego:tm: protocol. Start, stop, high and low bits are distinguished by the pause length.
The following table shows the timings for each of the intervals.

| Element          | Cycles @ 38000 Hz | Duration                 | PiIR Parameter  |
| ---------------- | ----------------- | ------------------------ | --------------- |
| Cycle            | 1 cycle           | 1 / 38,000  =  26 &mu;s  | "timebase" = 26 |
| Pulse            | 6 cycles          | 6 / 38,000  = 158 &mu;s  |  |
| Start/Stop Space | 39 cycles         | 39 / 38,000 =1,026 &mu;s | "preamble" = [6 , 39] <br /> "postamble" = [6] <br /> "gap" = 1026 |
| Low Bit Space    | 10 cycles         | 10 / 38,000 = 263 &mu;s  | "zero" = [6 , 10] |
| High Bit Space   | 21 cycles         | 21 / 38,000 = 553 &mu;s  | "one" = [6 , 21] |

The sixteen bits are grouped into four groups of four bits each called <em>nibbles</em>. The first two nibbles are configuration, except for Combo PWM where the second nibble is data. The third nibble is data. And the fourth nibble is Longitudinal Redundancy Check (a !XOR of the respective bits of the first three nibbles).

For the test we will send the code for Combo PWM mode - Channel 1 - Forward Step 2 / Forward Step 2. This way we ensure we have movement in both outputs. The first nibble (4) indicates the mode and channel. The second (2) and third (2) nibbles are the speeds for red and blue outputs respectively. The fourth one (B) is the LRC. The following table shows the conversion from key to pulse timings (+ is a pulse, while - is a space).
> **Note:**  Pulse timings are as they should be sent. With PiIR we pre-process the hexadecimal code so the timings are correct; but timings are not affected.

| Action | Keycode | Scancode<br />(Hexadecimal) | Scancode<br />(Hexadecimal)<br />Pre-Reversed | Scancode Timings |
| ------ | ------- | ---------- | ---------- | ---------------------------------- |
| Mode: Combo PWM<br />Channel 1<br />Output A: Forward Step 2<br />Output B: Forward Step 2 | FW2A_FW2B | 42 2B | 42 D4 | +158 -1026 <br />+158 -263 +158 -553 +158 -263 +158 -263 <br />+158 -263 +158 -263 +158 -553 +158 -263 <br />+158 -263 +158 -263 +158 -553 +158 -263 <br />+158 -553 +158 -263 +158 -553 +158 -553<br />+158 |

> **Note:** Mode and channel are not included in the keycode because all keycodes in the file are Combo PWM / Channel 1. I create different files for different mode/channel pairs. Otherwise each file would be too large.

[^1]: [Raspberry Pi PWM, MathWorks](https://www.mathworks.com/help/supportpkg/raspberrypiio/ug/the-raspberry-pi-pwm.html)
