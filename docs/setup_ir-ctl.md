# <code>ir-ctl</code>
## What is <code>ir-ctl</code>
> ir-ctl is a tool that allows one to list the features of a lirc device, set its options, receive raw IR, and send IR.
>
> IR can be sent as the keycode of a keymap, or using a scancode, or using raw IR.
> 
> [<code>ir-ctl</code> - Man Page](https://www.mankier.com/1/ir-ctl)

## Setup
> **Notes:**
>
> Ir-ctl man page: https://www.mankier.com/1/ir-ctl
> 
> RPi troubleshooting discussion on <code>ir-keymaps</code> (a cousin of <code>ir-ctl</code>: https://forums.raspberrypi.com/viewtopic.php?t=261471

### 1. Check if ir-ctl is installed by default.
This command also lists all capabilities of the default device (most likely /dev/lirc0)
```
ir-ctl -f
```
<code>
Receive features /dev/lirc0:
 - Device cannot receive
Send features /dev/lirc0:
 - Device can send raw IR
 - IR scancode encoder
 - Set carrier
 - Set duty cycle
</code>

### 2. Install <code>v4l-utils</code> if <code>ir-ctl</code> is not installed
```
sudo apt-get install v4l-utils
```

## Test
### Send key with ir-ctl
```
ir-ctl –-keymap=maps/keymaps/ir_ctl/combo_pwm_ch1_26ns.toml --keycode=FW2A_FW2B --verbose
```
<code>
Sending: +158 -1026 +158 -263 +158 -553 +158 -263 +158 -263 +158 -263 +158 -263 +158 -553 +158 -263 +158 -263 +158 -263 +158 -263 +158 -263 +158 -553 +158 -263 +158 -263 +158 -553 +158
Successfully sent
</code>

## Keymap
The name of the file should correspond to the protocol name with extension <code>.toml</code>. In our example case it would be combo_pwm_ch1_26ns.toml. The file consists of a header with protocol parameters such as length of pulse and space, followed by a list of scancode=keycode pairs. Any option such as carrier not included in the file, can be included in the command. Scancodes are hexadecimal. 

If the keymap is used for receiving commands, then keycodes should be valid linux keycodes. If the keymap is only used for sending IR, then the key (right side) does not have to be a valid linux keycode; it can be any string without whitespace. We only send codes!

```
[[protocols]]
name = "combo_pwm_ch1_26ns"
protocol = "pulse_distance"
margin = 200
header_pulse = 158
header_space = 1026
bit_pulse = 158
bit_0_space = 263
bit_1_space = 553
trailer_pulse = 158
bits = 16

[protocols.scancodes]
0x400B = "FLT_FLT"
0x401A = "FW1_FLT"
0x4029 = "FW2_FLT"
0x4038 = "FW3_FLT"
0x404F = "FW4_FLT"
0x405E = "FW5_FLT"
0x406D = "FW6_FLT"
0x407C = "FW7_FLT"
0x4083 = "BRK_FLT"
0x4092 = "RV7_FLT"
0x40A1 = "RV6_FLT"
0x40B0 = "RV5_FLT"
0x40C7 = "RV4_FLT"
0x40D6 = "RV3_FLT"
0x40E5 = "RV2_FLT"
0x40F4 = "RV1_FLT"
0x410A = "FLT_FW1"
0x411B = "FW1_FW1"
0x4128 = "FW2_FW1"
0x4139 = "FW3_FW1"
0x414E = "FW4_FW1"
0x415F = "FW5_FW1"
0x416C = "FW6_FW1"
0x417D = "FW7_FW1"
0x4182 = "BRK_FW1"
0x4193 = "RV7_FW1"
0x41A0 = "RV6_FW1"
0x41B1 = "RV5_FW1"
0x41C6 = "RV4_FW1"
0x41D7 = "RV3_FW1"
0x41E4 = "RV2_FW1"
0x41F5 = "RV1_FW1"
0x4209 = "FLT_FW2"
0x4218 = "FW1_FW2"
0x422B = "FW2_FW2"
0x423A = "FW3_FW2"
0x424D = "FW4_FW2"
0x425C = "FW5_FW2"
0x426F = "FW6_FW2"
0x427E = "FW7_FW2"
0x4281 = "BRK_FW2"
0x4290 = "RV7_FW2"
0x42A3 = "RV6_FW2"
0x42B2 = "RV5_FW2"
0x42C5 = "RV4_FW2"
0x42D4 = "RV3_FW2"
0x42E7 = "RV2_FW2"
0x42F6 = "RV1_FW2"
```

## Python Usage
There isn't a python library available for <code>ir-ctl</code>, so we use system commands.
```
import subprocess

param_keymap = f'--keymap=combo_pwm_ch1_26ns'
param_keycode = f'--keycode=FW2A_FW2B'
param_other = f'--verbose'
try: 
    subprocess.run(['ir-ctl' , param_keymap , param_keycode , param_other])
except subprocess.CalledProcessError as e:
    print('Unable to send the scancode!')
    print (e.output)
```
