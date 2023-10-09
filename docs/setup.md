# Initial Setup of IR on Raspberry Pi
These instructions are required regardless of the tool you use.

> **Note:**
> Some of this content was extracted from [Vaughan Harper' blog](https://vaughanharper.com/2020/08/12/configuring-an-infrared-remote-control-to-control-runeaudio-archlinux-without-needing-lirc/)

### 1. Edit /boot/config.txt
<pre><code>
$ sudo nano /boot/config.txt

# Comment this to disable audio.
# It shares pin 18. If you use other pins
# you might not need to comment this.
# Enable audio (loads and_bcm2835)
#dtparam=audio=on

# Uncomment this to enable infrared communication.
#dtoverlay=gpio-ir,gpio_pin=17
<b>dtoverlay=pwm-ir-tx,gpio_pin=18</b>
</code></pre>
### 2. Reboot
```
$ sudo reboot
```

### 3. Login back and confirm that the GPIO module has been loaded
```
> ssh pi@raspi.local

$ sudo lsmod | grep gpio
gpio_ir_tx              3607  0
```

### 4. See if GPIO 18 is PWM
> **Note:** I use a Raspberry Pi 1A v2. This model is limited to one hardware PWM pin (Pin 12 = GPIO18)
```
$ raspi-gpio get 18

GPIO 18: level=0 fsel=1 func=OUTPUT
```
