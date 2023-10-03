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


### 1. Install LIRC if ir-ctl is not installed
```
$ sudo apt-get install lirc
```

### 2. Edit <code>/etc/lirc/lirc_options.conf</code>
```
$ sudo nano /etc/lirc/lirc_options.conf
```
```
driver = default
device = /dev/lirc0
```

### 3. Start service and check
```
$ sudo systemctl start lircd.socket lircd.service
```
```
$ sudo systemctl status lirc.service
```

### 4. Reboot
```
$ sudo reboot
```

### 5. Stop, start and check status of lircd
```
$ sudo systemctl stop lircd.service
```
```
$ sudo systemctl start lircd.service
```
```
$ sudo systemctl status lircd.service
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
