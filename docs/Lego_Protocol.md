# Lego:tm: Protocol
You can find information on Lego:tm: Power Functions RC on [Philo's page on Power Functions](https://www.philohome.com/pf/pf.htm). The protocol itself is laid out in [LEGO:tm: Power Functions RC Version 1.2](LEGO_Power_Functions_RC_v120.pdf) (PDF, 370kb).
## Encoding
A code in the Lego:tm: protocol consists of (a) a start pulse/space, (b) sixteen –16– bits, and (c) a stop pulse/space. “Low bit consists of 6 cycles of IR and 10 “cycles” of pause, high bit of 6 cycles IR and 21 “cycles” of pause and start bit of 6 cycles IR and 39 “cycles” of pause.” All pulses are the same length in the Lego:tm: protocol. Start, stop, high and low bits are distinguished by the pause length.
The following table shows the timings for each of the intervals.

| Element          | Cycles @ 38000 Hz | Duration                 | PiIR Parameter  |
| ---------------- | ----------------- | ------------------------ | --------------- |
| Cycle            | 1 cycle           | 1 / 38,000  =  26 &mu;s  | "timebase" = 26 |
| Pulse            | 6 cycles          | 6 / 38,000  = 158 &mu;s  |  |
| Start/Stop Space | 39 cycles         | 39 / 38,000 =1,026 &mu;s | "preamble" = [6 , 39] <br /> "postamble" = [6] <br /> "gap" = 1026 |
| Low Bit Space    | 10 cycles         | 10 / 38,000 = 263 &mu;s  | "zero" = [6 , 10] |
| High Bit Space   | 21 cycles         | 21 / 38,000 = 553 &mu;s  | "one" = [6 , 21] |

The sixteen bits are grouped into four groups of four bits or <em>nibbles</em>. The first two nibbles are configuration, except for Combo PWM where the second nibble is data. The third nibble is data. And the fourth nibble is Longitudinal Redundancy Check (a !XOR of the respective bits of the first three nibbles).

For the test we will send the code for Combo PWM mode - Channel 1 - Forward Step 2 / Forward Step 2. This way we ensure we have movement in both outputs. The first nibble (4) indicates the mode and channel. The second (2) and third (2) nibbles are the speeds for red and blue outputs respectively. The fourth one (B) is the LRC. The following table shows the conversion from key to pulse timings (+ is a pulse, while - is a space).
> **Note:**  Pulse timings are as they should be sent. With PiIR we pre-process the hexadecimal code so the timings are correct; but timings are not affected.

| Action | Keycode | Scancode<br />(Hexadecimal) | Scancode Timings |
| ------ | ------- | ---------- | ---------------------------------- |
| Mode: Combo PWM<br />Channel 1<br />Output A: Forward Step 2<br />Output B: Forward Step 2 | FW2A_FW2B | 42 2B | +158 -1026 <br />+158 -263 +158 -553 +158 -263 +158 -263 <br />+158 -263 +158 -263 +158 -553 +158 -263 <br />+158 -263 +158 -263 +158 -553 +158 -263 <br />+158 -553 +158 -263 +158 -553 +158 -553<br />+158 |

> **Note:** Mode and channel are not included in the keycode because all keycodes in the file are Combo PWM / Channel 1. I create different files for different mode/channel pairs. Otherwise each file would be too large.

## RC Modes
The protocol allows for different modes of operation:

**Single vs. Combo:**
The Lego:tm: receiver has two outputs (Red and Blue). Some of the modes control one output at a time while others (very originally called combo) control both outputs at the same time. Here is a comparison of the main features of the different modes.

<table>
  <thead>
    <tr>
      <th>RC Mode</th>
      <th>Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Extended</td>
      <td>• One output at a time (determined by data)<br />• Red speeds -7··+7 (set by INC/DEC), blue speeds Full Forward/Float (set by TOGGLE)<br />• Permanent state until new key changes it<br />• Toggle address bit, but doesn't accept extended commands with address bit = 1</td>
    </tr>
    <tr>
      <td>Combo Direct</td>
      <td>• Both outputs simultaneously<br />• Speeds Full Forward, Full Backward,<br />Float, Break only<br />• Only one second</td>
    </tr>
    <tr>
      <td>Single Output: PWM</td>
      <td>• One output at a time<br />• Speeds -7··+7<br />• Permanent state until new key changes it</td>
    </tr>
    <tr>
      <td>Single Output:<br />Clear/Set/Toggle/<br />Inc/Dec</td>
      <td>• Couldn't make it work</td>
    </tr>
    <tr>
      <td>Combo PWM</td>
      <td>• Both outputs simultaneously<br />• Speeds -7··+7<br />• Only one second</td>
    </tr>
  </tbody>
</table>

### Bits
* Toggle (T): Toggling for every new command to distinguish new command from repeated code (protocol allows up to 5 repetitions of a command)
* Escape (E): Allows for selection of mode in conjunction with the mode bits. In this case 1=Combo PWM, 0=anything else.
* Channels (Ch) There are four possible channels to control 4 x 2 devices. Channels are numbered 1 (00) through 4 (11)
* Address (a): Allows for an extra address space not used. All modes work with address=0
* Mode (MMM): Allows for selection of mode in conjunction with the escape bit.
* Data (DDDD) 16 different possible values (0-F)
* Longitudinal Redundancy Check (L) = 0xF xor Nibble1 xor Nibble2 xor Nibble 3

<table>
  <thead>
    <tr>
      <th rowspan=2>RC Mode</th>
      <th colspan=4>Nibble 1</th>
      <th colspan=4>Nibble 1</th>
      <th colspan=4>Nibble 1</th>
      <th colspan=4>Nibble 1</th>
    </tr>
    <tr>
      <th><sub>T</sub></th>
      <th><sub>E</sub></th>
      <th colspan=2><sub>Ch</sub></th>
      <th><sub>a</sub></th>
      <th colspan=3><sub>Mode</sub></th>
      <th colspan=4><sub>Data</sub></th>
      <th colspan=4><sub>LRC</sub></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Extended</td>
      <td>T</td>
      <td>0</td>
      <td>C</td>
      <td>C</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>D</td>
      <td>D</td>
      <td>D</td>
      <td>D</td>
      <td>L</td>
      <td>L</td>
      <td>L</td>
      <td>L</td>
    </tr>
    <tr>
      <td>Combo Direct</td>
      <td>T</td>
      <td>0</td>
      <td>C</td>
      <td>C</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>1</td>
      <td>D<sub>B</sub></td>
      <td>D<sub>B</sub></td>
      <td>D<sub>R</sub></td>
      <td>D<sub>R</sub></td>
      <td>L</td>
      <td>L</td>
      <td>L</td>
      <td>L</td>
    </tr>
    <tr>
      <td>Single Output: PWM</td>
      <td>T</td>
      <td>0</td>
      <td>C</td>
      <td>C</td>
      <td>0</td>
      <td>1</td>
      <td>0</td>
      <td>0<sub>R</sub><br />1<sub>B</sub></td>
      <td>D</td>
      <td>D</td>
      <td>D</td>
      <td>D</td>
      <td>L</td>
      <td>L</td>
      <td>L</td>
      <td>L</td>
    </tr>
    <tr>
      <td>Single Output:<br />Clear/Set/Toggle/<br />Inc/Dec</td>
      <td>T</td>
      <td>0</td>
      <td>C</td>
      <td>C</td>
      <td>0</td>
      <td>1</td>
      <td>1</td>
      <td>0<sub>R</sub><br />1<sub>B</sub></td>
      <td>D</td>
      <td>D</td>
      <td>D</td>
      <td>D</td>
      <td>L</td>
      <td>L</td>
      <td>L</td>
      <td>L</td>
    </tr>
    <tr>
      <td>Combo PWM</td>
      <td>a=0</td>
      <td>1</td>
      <td>C</td>
      <td>C</td>
      <td>D<sub>B</sub></td>
      <td>D<sub>B</sub></td>
      <td>D<sub>B</sub></td>
      <td>D<sub>B</sub></td>
      <td>D<sub>R</sub></td>
      <td>D<sub>R</sub></td>
      <td>D<sub>R</sub></td>
      <td>D<sub>R</sub></td>
      <td>L</td>
      <td>L</td>
      <td>L</td>
      <td>L</td>
    </tr>
  </tbody>
</table>

### Data

<table>
  <thead>
    <tr>
      <th>RC Mode</th>
      <th colspan=2>Data</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td rowspan=9>Extended<br /><em>DDDD</em></td>
      <td>0000</td><td>Brake then float output A</td>
    </tr>
    <tr><td>0001</td><td>Increment speed on output A</td></tr>
    <tr><td>0010</td><td>Decrement speed on output A</td></tr>
    <tr><td>0011</td><td>Not used</td></tr>
    <tr><td>0100</td><td>Toggle forward/float on output B</td></tr>
    <tr><td>0101</td><td>Not used</td></tr>
    <tr><td>0110</td><td>Toggle Address bit</td></tr>
    <tr><td>0111</td><td>Align toggle bit (get in sync)</td></tr>
    <tr><td>1000</td><td>Reserved</td>
    </tr>
    <tr>
      <td rowspan = 4>Combo Direct<br /><em>D<sub>R</sub>D<sub>R</sub> or D<sub>B</sub>D<sub>B</sub></em></td>
      <td>00</td><td>Float output B</td>
    </tr>
    <tr><td>01</td><td>Forward on output B</td></tr>
    <tr><td>10</td><td>Backward on output B</td></tr>
    <tr><td>11</td><td>Brake then float output B</td></tr>
    <tr>
      <td rowspan = 16>Single Output: PWM<br /><em>DDDD</em></td>
    </tr>
    <tr><td>0001</td><td>PWM forward step 1</td></tr>
    <tr><td>0010</td><td>PWM forward step 2</td></tr>
    <tr><td>0011</td><td>PWM forward step 3</td></tr>
    <tr><td>0100</td><td>PWM forward step 4</td></tr>
    <tr><td>0101</td><td>PWM forward step 5</td></tr>
    <tr><td>0110</td><td>PWM forward step 6</td></tr>
    <tr><td>0111</td><td>PWM forward step 7</td></tr>
    <tr><td>1000</td><td>Brake then float</td></tr>
    <tr><td>1001</td><td>PWM backward step 7</td></tr>
    <tr><td>1010</td><td>PWM backward step 6</td></tr>
    <tr><td>1011</td><td>PWM backward step 5</td></tr>
    <tr><td>1100</td><td>PWM backward step 4</td></tr>
    <tr><td>1101</td><td>PWM backward step 3</td></tr>
    <tr><td>1110</td><td>PWM backward step 2</td></tr>
    <tr><td>1111</td><td>PWM backward step 1</td></tr>
    <tr>
      <td rowspan = 16>Single Output:<br />Clear/Set/Toggle/<br />Inc/Dec<br /><em>DDDD</em></td>
      <td>0000</td><td>Toggle full forward (Stop → Fw, Fw → Stop, Bw → Fw)</td></tr>
    <tr><td>0001</td><td>Toggle direction</td></tr>
    <tr><td>0010</td><td>Increment numerical PWM</td></tr>
    <tr><td>0011</td><td>Decrement numerical PWM</td></tr>
    <tr><td>0100</td><td>Increment PWM</td></tr>
    <tr><td>0101</td><td>Decrement PWM</td></tr>
    <tr><td>0110</td><td>Full forward (timeout)</td></tr>
    <tr><td>0111</td><td>Full backward (timeout)</td></tr>
    <tr><td>1000</td><td>Toggle full forward/backward (default forward)</td></tr>
    <tr><td>1001</td><td>Clear C1 (negative logic – C1 high)</td></tr>
    <tr><td>1010</td><td>Set C1 (negative logic – C1 low)</td></tr>
    <tr><td>1011</td><td>Toggle C1</td></tr>
    <tr><td>1100</td><td>Clear C2 (negative logic – C2 high)</td></tr>
    <tr><td>1101</td><td>Set C2 (negative logic – C2 low)</td></tr>
    <tr><td>1110</td><td>Toggle C2</td></tr>
    <tr><td>1111</td><td>Toggle full backward (Stop → Bw, Bw → Stop, Fwd → Bw)</td></tr>
    <tr>
      <td rowspan = 16>Combo PWM<br /><em>D<sub>R</sub>D<sub>R</sub>D<sub>R</sub>D<sub>R</sub> or D<sub>B</sub>D<sub>B</sub>D<sub>B</sub>D<sub>B</sub></em></td>
      <td>0000</td><td>Float</td>
    </tr>
    <tr><td>0001</td><td>PWM forward step 1</td></tr>
    <tr><td>0010</td><td>PWM forward step 2</td></tr>
    <tr><td>0011</td><td>PWM forward step 3</td></tr>
    <tr><td>0100</td><td>PWM forward step 4</td></tr>
    <tr><td>0101</td><td>PWM forward step 5</td></tr>
    <tr><td>0110</td><td>PWM forward step 6</td></tr>
    <tr><td>0111</td><td>PWM forward step 7</td></tr>
    <tr><td>1000</td><td>Brake then float</td></tr>
    <tr><td>1001</td><td>PWM backward step 7</td></tr>
    <tr><td>1010</td><td>PWM backward step 6</td></tr>
    <tr><td>1011</td><td>PWM backward step 5</td></tr>
    <tr><td>1100</td><td>PWM backward step 4</td></tr>
    <tr><td>1101</td><td>PWM backward step 3</td></tr>
    <tr><td>1110</td><td>PWM backward step 2</td></tr>
    <tr><td>1111</td><td>PWM backward step 1</td></tr>
  </tbody>
</table>


###
