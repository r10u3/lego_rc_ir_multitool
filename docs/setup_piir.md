# PiIR
## What is PiIR?
> IR remote control for Raspberry Pi.
>
> PiIR is a client program for pigpio, the excellent hardware-timed GPIO library. Some code are taken from its sample program irrp.py.
>
> **Features**
> * Records and plays IR remote control code.
> * Decodes and encodes NEC, Sony, RC5, RC6, AEHA, Mitsubishi, Sharp and Nokia formats.
> * Dumps decoded and prettified data to help you analyze your air conditioner's remote.
> * Both command-line and programmatic control.
>
> [PiIR 0.2.5](https://pypi.org/project/PiIR/) by Takeshi Sone

In our case, we will play IR remote control code.

## Setup <code>pigpio</code>
> **Note:**
>
> [PiIR project page](https://pypi.org/project/PiIR/))

### 1. Install PiIR
```
sudo pip3 install PiIR
```
### 2. Start pigpio daemon
```
sudo systemctl enable pigpiod
```
```
sudo systemctl start pigpiod
```

### 3. Reboot
```
sudo reboot
```

### 4. Stop, start and check status of pigpio
```
sudo systemctl stop pigpiod
```
```
sudo systemctl start pigpiod
```
```
sudo systemctl status pigpiod
```

## Test
### 1. Make sure service is running
```
sudo systemctl status pigpiod
```
### 2. Send a sample code
> **Note:** Assuming you are at the Project root directory
```
piir play --gpio 18 --file maps/keymaps/piir/combo_pwm_ch1_26ns.json FW2_FW2
```
## PiIR Keymap Format
After testing, PiIR seems to reverse bits on most and least significant bytes (per byte). As a result, we can either create keymap files that pre-reverse the bits or use the send_data() command and create the code on the fly programmatically. In either case we need to pre-reverse the data as follows:
Convert Lego Keycode to Scancode (Bytes in Hex)
Convert Bytes to bits
Reverse bits on each byte individually
Convert back to Bytes in Hex

Here is an example
| Keycode | Scancode | Scancode<br>in bits | Bits reversed | Bits Reversed<br /> to Bytes |
|---------|----------|----------|---------------|--------------|
|FW2A_FW2B | 42 2B | 0100 0010 - 0010 1011 | 0100 0010 - 1101 0100 | 42 D4 |

The protocol parameters seem to follow a multiplier format, with a timebase and all definitions as multiples of the base. In our case, we use 1/38,000Hz = 26 &nu;s. Then we can use the multipliers laid out in [LEGO_Power_Functions_RC_v120](docs/LEGO_Power_Functions_RC_v120.pdf).

Here is a sample of the keymap file:


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
## Python Usage
> **Notes:** For more info: [LIRC man pages](https://www.lirc.org/html/)

### 1. PiIR API: 
#### a. Sending IR keycode
```
import piir

remote_tx = piir.Remote('/etc/rc_keymaps/lego_26ns', 18)
remote_tx.send('FW2A_FW2B')
```
#### b. Sending arbritrary data
```
remote_tx.send_data('42 2B')
```
Or
```
remote_tx.send_data(bytes([0x422B]))
```
