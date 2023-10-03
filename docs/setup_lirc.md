# Setup LIRC
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
