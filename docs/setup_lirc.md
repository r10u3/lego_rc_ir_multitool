# LIRC
## What is LIRC?
>LIRC is a package that allows you to decode and send infra-red signals of many (but not all) commonly used remote controls.
>
>Recent linux kernels makes it possible to use some IR remote controls as regular input devices. Sometimes this makes LIRC redundant. However, LIRC offers more flexibility and functionality and is still the right tool in a lot of scenarios.
>
>The most important part of LIRC is the lircd daemon which decodes IR signals received by the device drivers and provides the information on a socket. It also accepts commands for IR signals to be sent if the hardware supports this.
>
> [lirc.org](https://www.lirc.org/)

In our case, we use LIRC to send commands via a PWM GPIO pin and custom hardware (see [rc_emitter.md](rc_emitter.md))

## Setup LIRC
> **Notes:**
>
> [LIRC man pages](https://www.lirc.org/html/)
>
> [Rich101101's Easy Setup IR Remote Control Using LIRC for the Raspberry PI (RPi)](https://www.instructables.com/Setup-IR-Remote-Control-Using-LIRC-for-the-Raspber/)


### 1. Install LIRC if it is not installed
```
sudo apt-get install lirc
```

### 2. Edit <code>/etc/lirc/lirc_options.conf</code>
```
sudo nano /etc/lirc/lirc_options.conf
```
```
driver = default
device = /dev/lirc0
```

### 3. Start service and check
```
sudo systemctl start lircd.socket lircd.service
```
```
sudo systemctl status lirc.service
```

### 4. Reboot
```
sudo reboot
```

### 5. Stop, start and check status of lircd
```
sudo systemctl stop lircd.service
```
```
sudo systemctl start lircd.service
```
```
sudo systemctl status lircd.service
```

### 6. Create bash to keep irw alive

> “It takes some time to set up (50 ms or so) so when no clients are connected to lircd the first transmission will have some higher latency. A workaround for this is to keep irw running with a bash script like this:” (https://www.lirc.org/html/audio.html)
```
#!/bin/sh
while [ true ]; do
irw || true
sleep 1
done
```

### 7. Copy LIRC Keymap Files to <code>/etc/lirc/lircd.conf.d/</code>
LIRC expects all files to be located at /etc/lirc/lircd.conf.d/. 

> **Notes:**
>
> Of course, you need to have the keymaps locally already. So perform this step after all files are copied or extracted on the Raspberry Pi.
>
> I use the default user <code>pi</code> and you need to change the <code>[project folder]</code> to its actual name.
```
sudo cp -r [project folder]/maps/keymaps/lirc /etc/lirc/lircd.conf.d/
```
We also hide <code>devinput.lircd.conf</code>. This is not necessary, but reduces bloat by loading less remotes 
```
sudo mv /etc/lirc/lircd.conf.d/devinput.lircd.conf /etc/lirc/lircd.conf.d/devinput.lircd.conf.dist
```
## Test
### 1. Make sure lircd service is running
```
sudo systemctl status lirc.service
```
### 2. List all the available remotes.
```
irsend LIST "" ""
```
### 3. List all the available codes for a particular remote
```
irsend LIST "cmb_pwm_ch1" ""
```
### 4. Send a sample code
```
irsend SEND_ONCE cmb_pwm_ch1 FW2A_FW2B
```
## LIRC Keymap Format
This file contains a sample of codes. For example, the code <code>FW2A_FW2B</code> is not included. The complete file is included in the <code>maps/keymaps/lirc</code> directory.
```
begin remote

  name  combo_pwm_ch1_26ns
  bits           16
  flags SPACE_ENC
  eps            30
  aeps          100

  header       158  1026
  one           158  553
  zero          158  263
  ptrail        158
  gap          1026
  frequency    38000

      begin codes
          FLT_FLT 0x400B
          FW1_FLT 0x401A
          FW2_FLT 0x4029
          FW3_FLT 0x4038
          FW4_FLT 0x404F
          FW5_FLT 0x405E
          FW6_FLT 0x406D
          FW7_FLT 0x407C
          BRK_FLT 0x4083
          RV7_FLT 0x4092
          RV6_FLT 0x40A1
          RV5_FLT 0x40B0
          RV4_FLT 0x40C7
          RV3_FLT 0x40D6
          RV2_FLT 0x40E5
          RV1_FLT 0x40F4
          FLT_FW1 0x410A
          FW1_FW1 0x411B
          FW2_FW1 0x4128
          FW1_FW7 0x471D
          FW2_FW7 0x472E
          FW3_FW7 0x473F
          FW4_FW7 0x4748
          FW5_FW7 0x4759
          FW6_FW7 0x476A
          FW7_FW7 0x477B
          BRK_FW7 0x4784
          RV7_FW7 0x4795
          RV6_FW7 0x47A6
          RV5_FW7 0x47B7
          RV4_FW7 0x47C0
          RV3_FW7 0x47D1
          RV2_FW7 0x47E2
          RV1_FW7 0x47F3
    end codes
end remote
```
## Python Usage
> **Notes:** For more info: [LIRC man pages](https://www.lirc.org/html/)

### 1. Install LIRC for python
```
sudo pip3 install lirc
```
### 2. LIRC API: Sending IR
```
import lirc

client = lirc.Client()
client.send_once("cmb_pwm_ch1" , "FW2A_FW2B")
```
### 3. LIRC API: Handling Errors
```
import lirc

client = lirc.Client()
remote_name = cmb_pwm_ch1
key = 'FW2A_FW2B'
try:
    client.send_once(remote_name , key)
except lirc.exceptions.LircdCommandFailureError as error:
    print(f'Unable to send the {key}!')
    print(error)  # Error has more info on what lircd sent back.
```
