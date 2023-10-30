# Lego:tm: Power Functions & Raspberry Pi
<em>Last updated: 10/23/2023</em>

## Important
**This project is not very practical.** It mostly shows the tools available and my own journey through these tools. You don't need all four tools. You only need one. But the tools are available for you to pick the tool and mode you prefer and import only those.

**This project is complete.** I will maintain it if bugs appear, but it has been tested successfully and is finished. I am open to ideas for new features, but do not guarantee them.

## Introduction

This project is part of using a Raspberry Pi as a [Lego:tm: PowerFunctions](docs/Lego_Protocol.md) controller. In my case, I use a headless Raspberry Pi 1 version 2, with Raspbian Bullseye. I also use a simple transmitter using an IR LED and a simple circuit (see [rc_transmitter](docs/rc_transmitter.md) for more details).
> **Note:** Technically, the app can use any remote configuration, not just Lego. Except for the IR_RPiGPIO which is coded for pulse distance encoding ([see pulse distance modulation](https://www.phidgets.com/docs/IR_Remote_Control_Guide)). Although it should be open to any pulse distance encoding. The IR_PiIR tool, on the other hand, is hardcoded for 16 bits for the RAW mode.

There are four IR tools that I found that work with Python and I use in this project (in the order I learnt them):
* LIRC:
  - LIRC is a package that allows you to decode and send infra-red signals of many (but not all) commonly used remote controls.
  - Recent linux kernels make it possible to use some IR remote controls as regular input devices. Sometimes this makes LIRC redundant. However, LIRC offers more flexibility and functionality and is still the right tool in a lot of scenarios.
  - LIRC accepts commands for IR signals to be sent if the hardware supports this.
  - Commands must match the keycode in the keymap file.
    - Keymaps are provided
    - Keymaps must be placed in /etc/lirc/lircd.conf.d/
  - [lirc.org](https://www.lirc.org/)
* <code>ir-ctl</code>
  - ir-ctl is a tool that allows one to list the features of a lirc device, set its options, receive raw IR, and send IR.
  - IR can be sent as the keycode of a keymap, using a scancode, or using a raw IR file.
    - In this app, we only coded for keycodes on keymaps.
    - Keymaps are provided.
  - [<code>ir-ctl</code> - Man Page](https://www.mankier.com/1/ir-ctl)
* PiIR
  - PiIR is a client program for pigpio, a hardware-timed GPIO library that records and plays IR remote control code.
  - PiIR provides both command-line and programmatic control.
    - We use python programmatic control.
  - IR can be sent as the keycode of a keymap, or using a scancode in hexadecimal format.
    - In this app, we coded for keycodes on keymaps and 16 bit scancodes.
    - Keymaps are provided.
  - [PiIR 0.2.5](https://pypi.org/project/PiIR/) by Takeshi Sone
* PiGPIO
  - "pigpio is a library for the Raspberry which allows control of the General Purpose Input Outputs (GPIO).  pigpio works on all versions of the Pi." [^1]
  - Among other things, it allows waveforms to generate GPIO level changes (time accurate to a few &mu;s)
  - I developed a custom object to handle the codes.
  - IR can be sent as the keycode of a keymap, or using a scancode in hexadecimal or integer (decimal, binary or hexadecimal) format.
    - Keymaps are provided.
 
In comparing speeds roughly by eye, there is no noticeable difference between the tools. New keys are almost instantaneous, while repeated keys seem limited by sshkeyboard. This poses a limitation for increment/decrement where it takes multiple keystrokes of the same key to reach a particular speed.

## Multitool API
> **Definitions:**
>
> **Mapping:** Keys are mapped to the code sent in the following progression: **button (or key) &rarr; keycode &rarr; scancode**
> 
> **Button:** The actual key pressed (or whatever the app receives as a key). Examples of buttons/keys are: 'space', '&rarr;', '&larr;', '&uarr;', 'a', '4'
>
> **Keycode:** The tool's interpretation of a key. It does not have to be a real key. Normally, remote apps link remote buttons to system keys that are used to create events. We are using a custom app and the keys are not system keys. Examples of keycodes are: 'FW2_RV3', 'A_FLT'
>
> **Scancode:** The actual code being sent. Could be an hexadecimal string  (e.g., 422B) or an integer in hexadecimal, binary or decimal form (e.g., 0x422B, 0b0100001000101011, or 16939). The keymap files, map keycodes to scancodes in hexadecimal format, each with its own syntax. The code is converted to binary by the ir tool.

If you want to use parts of this project as an API, you can do without the <code>sshkeyboard_.py</code> file and access the objects directly. Here is a description of each object and their Members

### 1. Keypad
#### a. Features
* The <code>keypad</code> maps buttons to actions.
* Note that the <code>keypad</code> does not match buttons to keycodes. The reason is that when creating scancodes for the **combo** modes, it is useful to have both outputs separate (e.g, ['FW2', 'RV3']), while a keycode combines them (e.g., 'FW2_RV3').

#### b. Members
##### &#x25B6; New Object: <code>Keypad(mapped_keys_file_name: str) -> Keypad</code>
```
import keypad

kb = keypad.Keypad(mapped_keys_file_name)
```
**Args:**

* **<code>mapped_keys_file_name</code>:** loaded from <code>maps/maps_config.json</code>.
<br /><br />

##### &#x25B6; <code>is_mapped_key(key: str) -> bool</code>
Checks whether a particular key (e.g., &uarr;) is in the button map.
```
is_mapped_key(key)
```
**Args:**
* **<code>key (str)</code>:** The key to be considered (e.g., 'up' for ↑).

**Returns:**
* **<code>bool:</code>** <code>True</code> if the key exists, <code>False</code> otherwise.
<br /><br />

##### &#x25B6; <code>get_action(key: str) -> [str , str]</code>
Returns the action associated to a particular key. 
```
get_action(key)
```

**Args:**
* **<code>key (str)</code>:** The key to be considered (e.g., 'up' for ↑).

**Returns:**
* **<code>[str, str]</code>:** A <code>[color , action]</code> array for the single output modes (single PWM, single other and extended) or <code>[action_A, action_B]</code> for the combo modes (combo PWM and combo direct).
<br /><br />

### 2. IR Tools
#### a. Features
* IR tools take keycodes or scancodes and send it to the respective tool
* There are four types (classes):
  * <code>IR_LIRC</code>: sends keycodes using LIRC's python API.
  * <code>IR_ir_ctl</code>: sends keycodes using ir-ctl via system calls.
  * <code>IR_PiIR</code>: sends keycodes and scancodes using PiIR's library.
  * <code>IR_RPiGPIO</code>: converts keycodes and scancodes to wave chains and sends them using pigpio's python API.
* All have the same basic functions and attributes (i.e., members) with the same signatures.
* They send codes to the respective IR tool to be transmitted.

#### b. Members
##### &#x25B6; New Object: <code>[Tool](GPIO: int, keymap_file_name: str, keymap_folder_name: str = '/maps/keymaps/[tool]') -> [Tool]</code>
**Args:**
* **<code>GPIO (int)</code>:**  The GPIO pin used to transmit IR. Used by PiIR and RPiGPIO only. <code>LIRC</code> and <code>ir-ctl</code> use the pin configured in the <code>/boot/config.txt</code> file.  Loaded from <code>config.json</code>. PIN must be Hardware PWM. "The maximum [software] PWM output frequency is 8 KHz using <code>writePWMFrequency(mypi, 12, 8000)</code>."[^2] Lego uses 38KHz.
* **<code>keymap_file_name (str)</code>:** The name of the file containing the keymap.  Loaded from <code>maps/maps_config.json</code>. Used by <code>ir-ctl</code>, PiIR, and RPiGPIO to locate the keymap. <code>LIRC</code> uses remote names instead of keymap files. The remote name is inside the keymap file. As a matter of practice, the remote name should match the name of the keymap file minus the extension, but is not required by LIRC.<br />
<code>Default = 'single_pwm.toml'</code>.
* **<code>keymap_folder_name (str)</code>:** The name of the folder where the keymap is. Loaded from <code>maps/maps_config.json</code>. Used by <code>ir-ctl</code>, PiIR and RPiGPIO to locate the keymap. <code>LIRC</code> keymaps are all located at <code>/etc/lirc/lircd.conf.d</code> (you copy these as part of the setup).<br />
<code>Default = 'maps/keymaps/ir_ctl'</code>.

The function calls to create each type of object are:
```
import ir_tools.ir_ctl as irt
remote_tx = irt.IR_ir_ctl(GPIO, REMOTE_KEYMAP_FILE_NAME, REMOTE_KEYMAP_FOLDER_NAME)
```
```
import ir_tools.lirc as irt
remote_tx = irt.IR_LIRC(GPIO, REMOTE_KEYMAP_FILE_NAME, REMOTE_KEYMAP_FOLDER_NAME)
```
```
import ir_tools.piir as irt
remote_tx = irt.IR_PiIR(GPIO, REMOTE_KEYMAP_FILE_NAME, REMOTE_KEYMAP_FOLDER_NAME)
```
```
import ir_tools.rpigpio as irt
remote_tx = irt.RPiGPIO(GPIO, REMOTE_KEYMAP_FILE_NAME, REMOTE_KEYMAP_FOLDER_NAME)
```

##### &#x25B6; send(keycode: str) -> None:
Send IR keycode (e.g., 'FW2_RV3') using system the respective underlying IR tool.
Args:
* **keycode:** The keycode to be sent. For example 'FW2_RV3'

##### &#x25B6; send_hex(data_bytes: str) -> None:
Takes a scancode in hexadecimal string format (e.g., '422B') and sends it. This function is unique to PiIR and RPiGPIO. The code must be a valid code. The function does not check for validity. The code is sent anyway and the receiver will reject it without any error.
> **Notes:**
> 
> PiIR reverses the bits in each byte, so the function pre-processes the data to be sent. This is not the case with RPiGPIO, which was custom coded for this application. This is done in the background without the user's awareness.
> RPiGPIO converts the string to pigpio wave and sends it.
Args:
* **data_bytes:** the scancode to be sent as an hexadecimal string.

##### &#x25B6; send_raw(data: int) -> None:
This function is unique to RPiGPIO. It takes a scancode in integer format (e.g., 16939 or 0x422B), and sends it. The code must be a valid code. The function does not check for validity. The code is sent anyway and the receiver will reject it without any error.
Arguments:
* **data:** the scancode as an integer. Could be binary (0b...), hexadecimal (0x...) or plain decimal. PiIR's tool is hardcoded for 2 bytes (16 bits).

### 3. Power Functions (Encoders)
#### a. Features
* There are five types (classes):
  * ComboPWM
  * ComboDirect
  * SinglePWM
  * Extended
  * SingleOther
* All have the same functions and variables (i.e., members) with the same signatures.
* Keep track of:
  * Toggle bit (changes with each request for keycode or scancode except for combo PWM)
  * Address bit (defaults to 0 and only changes in extended mode)
* Provide keycode corresponding to action codes
  * e.g., in single PWM '&uarr;' is mapped to ["B", "FW7"] by keyboard. ["B", "FW7"] is then mapped to the keycode B_FW7 by the encoder.
* Provide the scancode corresponding to button codes
  * e.g., in the previous case, the scancode is 0x057D with toggle 0 or 0x8575 with toggle 1


#### b. Members
##### &#x25B6; New Object: [encoder]&#40;&#41; -> [encoder]
Does not require any parameters. The function calls to create each type of object are:
```
import power_functions.combo_pwm as pf
rc_encoder = pf.ComboPWM()
```
```
import power_functions.combo_direct as pf
rc_encoder = pf.ComboDirect()
```
```
import power_functions.single_pwm as pf
rc_encoder = pf.SinglePWM()
```
```
import power_functions.single_other as pf
rc_encoder = pf.SingleOther()
```

##### &#x25B6; <code>get_keycode(str, str) -> keycode: str</code>
Get keycode for output/action or actions A/B pairs. Returns <code>keycode</code>
Actions programmed include:
* break then float='BRK'
* increment speed='INC'
* forward speeds='FW1' through 'FW7'
* decrement speed= 'DEC'
* reverse speeds ='RV1' through 'RV7'
* float= 'FLT'
* toggle bit= 'TOG'
* <em>et cetera</em>

<table>
  <thead>
    <tr>
      <th></th>
      <th>Single Modes</th>
      <th>Combo Modes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>Pairs</th>
      <td>[output, action]</td>
      <td>[action A, action B]</td>
    </tr>
    <tr>
      <th rowspan=2>Code</th>
      <td>
        <pre>rc_encoder.get_keycode(output , action)</pre>
        For example:
        <pre>rc_encoder.get_keycode("A" , "FW4")</pre>
      </td>
      <td>
        <pre>rc_encoder.action(action_A, action_B)</pre>
        For example:
        <pre>rc_encoder.get_keycode("RV3" , "FW4")</pre>
      </td>
    </tr>
    <tr>
      <td colspan=2><pre>rc_encoder.action(*key)</pre></td>
    </tr>
    <tr>
      <td></td>
      <td>Where:<br />key is a [output, action] pair<br />such as ["A" , "FW4"]</td>
      <td>Or:<br />key is a [action A, action B] pair<br />such as ["RV3" , "FW4"]</td>
    </tr>
  </tbody>
</table>

## IR Multitool Configuration

### 1. Config file
<code>config.json</code>
```
{
    "system_mode" : "KEY",
    "project_folder" : "/home/pi/Projects/lego_rc",
    "rc_mode" : "SGL",
    "maps_config_file" : "maps/maps_config.json",
    "ir_tool" : "rpigpio",
    "GPIO" : 18
}
```
#### A. <code>system_mode</code>
This determines the **send** command to be used. There are three possible modes:
* **'KEY':** sends keycode from keymap. Keycodes are preset in the keymaps. This is the easiest mode to use.
* **'RAW':** sends the scancode as **int**. Only available for PiIR and RPiGPIO. The scancode is produced from the [*key] pairs in the button maps.
* **'HEX':** sends the scancode as hexadecimal string. Only available for PiIR and RPiGPIO. The scancode is produced from the [*key] pairs in the button maps.

#### b. <code>project_folder</code>
This is the absolute path to the project. It is not really used anywhere

#### c. <code>maps_config_file</code>
This is quite important. If you move the config file, make sure to modify here. I recommend you leave it where it is.

The <code>maps_config_file</code> file has links to keymaps and button maps. If you change the names of the keymaps or use different ones, make sure to update the <code>maps_config_file</code>.

#### d. <code>rc_mode</code>
The available modes are:
   - PWM: Combo PWM
   - DIR: Combo Direct
   - SGL: Single PWM
   - EXT: Extended
   - OTH: Single Clear/Set/Toggle/Inc/Dec

#### e. <code>ir_tool</code>
The available tools (as used in the config files) are:
   - lirc
   - ir_ctl
   - piir
   - rpigpio (the 'r' prefix is there to distinguish it from the pigpio library when it's imported)

#### f. <code>gpio_pin</code>
PIN must be Hardware PWM. "The maximum [software] PWM output frequency is 8 KHz using writePWMFrequency(mypi, 12, 8000)."[^2] Lego uses 38KHz.

### 2. Button Maps
The keys are configured in the <code>maps/button_maps</code> folder. One file per rc mode. Each mode has its own set of key mappings. I only coded for the A output in most cases. Here are some **comparative examples**:

|  Key         |  Combo PWM   | Combo Direct |  Single PWM  |   Extended   | Single Other |
| ------------ | ------------ | ------------ | ------------ | ------------ | ------------ |
| &uarr;       | FW7_FW7      | FW7_FLT      | B_FW7        | A_INC        | A_INC_NUM    |
| &darr;       | RV7_FLT      | RV7_FLT      | B_RV7        | A_DEC        | A_DEC_NUM    |
| &rarr;       | FLT_FW7      | FLT_FW7      | B_FLT        | n/a          | A_DEC_PWM    |
| &larr;       | FLT_RV7      | FLT_RV7      | B_BRK        | n/a          | A_DEC_PWM    |
| SPACE        | BRK_BRK      | BRK_BRK      | A_BRK        | A_BRK        | A_TOG_DIR    |
| 'l'          | FLT_FLT      | n/a          | A_FLT        | n/a          | B_TOG_C2     |
| '1'          | FW1_FLT      | n/a          | A_FW1        | n/a          | CLR_C1       |
| '2'          | FW2_FLT      | n/a          | A_FW2        | n/a          | n/a          |
| ...          | ...          | ...          |  ...         | ...          | ...          |
| '7'          | FW7_FLT      | n/a          | A_FW7        | n/a          | TOG_C1       |
| 'a'          | RV1_FLT      | n/a          | A_RV1        | ADD_TOG      | TOG_FWD      |
| 'b'          | RV2_FLT      | n/a          | A_RV2        | B_TOG        | FUL_REV      |
| ...          | ...          | ...          |  ...         | ...          | ...          |
| 'g'          | RV7_FLT      | n/a          | A_RV7        | n/a          | n/a          |
| Noteworthy |<sub>&bull; Both outputs simultaneously<br />&bull; Speeds -7&#183;&#183;+7<br />&bull; Timeout with loss of IR (needs constant IR to keep going)</sub>|<sub>&bull; Both outputs simultaneously<br />&bull; Speeds Full Forward, Full Backward, Float, Break only<br />&bull; Timeout with loss of IR (needs constant IR to keep going)</sub> |<sub>&bull; One output at a time<br />&bull; Speeds -7&#183;&#183;+7<br />&bull; No timeout for IR loss; keeps going until new key changes it</sub> |<sub>&bull; One output at a time<br />&bull; A speeds -7&#183;&#183;+7, B speeds Full Forward/Float<br />&bull; No timeout for IR loss; keeps going until new key changes it<br />&bull; Toggle address bit, but doesn't accept <em>extended</em> commands with <code>address bit = 1</code></sub> |<sub>&bull; One output at a time<br /> &bull; Speeds -7&#183;&#183;+7<br />&bull; No timeout for IR loss; keeps going until new key changes it. Except full forward/backward<br />&bull; C1 & C2 work as opposite directions. I haven't tested actual voltages to assess differences |

One important difference between the combo (direct and PWM) and not combo modes (single PWM, extended and single other) is that with not combo modes, the state is permanent. When you press a key, the motor starts and keeps going. With the combo modes, the motor moves only for about a second and stops. You need to keep sending keycodes to keep the motor going.

### 3. Keymaps
Every tool has its own different keymap format. They all have a header with basic protocol parameters followed by keycode-scancode pairs. But each has a different format:
* LIRC: lirc keymaps have a <code>[.conf](https://www.lirc.org/html/lircd.conf.html)</code> extension and follow the basic rules of configuration files. Example for [Combo PWM](maps/keymaps/lirc/combo_pwm_ch1.conf).
* ir-ctl: uses the <code>[.toml](https://www.mankier.com/5/rc_keymap)</code> format. Example for [Combo PWM](maps/keymaps/ir_ctl/combo_pwm_ch1.toml).
* PiIR: uses json files. Example for [Combo PWM](maps/keymaps/piir/combo_pwm_ch1.json).
* PiGPIO: uses json files. Example for [Combo PWM](maps/keymaps/rpigpio/combo_pwm_ch1.json).

The common parameters in the header include (the names and format might change from one format to another but the meaning and values remain):

| Parameter | Value[^3] | Unit | Cycles[^4] | Notes |
|-----------|-------|------|--------|-------|
| frequency | 38000 | Hz | n/a | |
| cycle length | 26 | &mu;s | 1 | 1/carrier |
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

### 5. Setup PiGPIO
I created a custom object that uses PiGPIO directly. You should have already performed these steps. If you pick and choose your tools, these steps would required to use RPiGPIO (the object I created). But only if you didn't do it already.
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
The example app (sshkeyboard_.py) uses sshkeyboard for input capture over SSH. I am using a headless RPi over SSH. If you use a different configuration or create your own app, you can skip this step. You will need to install the appropriate capture tool for your platform configuration.

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
irsend LIST "combo_pwm_ch1" ""
```
Send a sample code
```
irsend SEND_ONCE combo_pwm_ch1 FW2_FW2
```
#### b. Test ir-ctl
First, navigate to the project's directory. Then send key with ir-ctl
```
ir-ctl –-keymap=maps/keymaps/ir_ctl/combo_pwm_ch1.toml --keycode=FW2A_FW2B --verbose
```

#### c. Test PiIR
Send a sample code. Again, first navigate to the project's directory.
```
piir play --gpio 18 --file maps/keymaps/piir/combo_pwm_ch1.json FW2_FW2
```

#### c. Test RPiGPIO
Send a sample code. Again, first navigate to the project's directory.
```
python -c 'import ir_tools.rpigpio as irt; irt.test_send("maps/keymaps/rpigpio/combo_pwm_ch1.json" , 18 , "FW2_FW2")'
```

[^1]: [The pigpio library](https://abyz.me.uk/rpi/pigpio/), joan@abyz.me.uk
[^2]: [Raspberry Pi PWM, MathWorks](https://www.mathworks.com/help/supportpkg/raspberrypiio/ug/the-raspberry-pi-pwm.html)
