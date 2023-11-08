# Lego:tm: Protocol
You can find information on Lego:tm: Power Functions RC on [Philo's page on Power Functions](https://www.philohome.com/pf/pf.htm). The protocol itself is laid out in [LEGO:tm: Power Functions RC Version 1.2](LEGO_Power_Functions_RC_v120.pdf) (PDF, 370kb).
## Encoding
A code in the Lego:tm: protocol consists of (a) a start pulse/space, (b) sixteen –16– bits, and (c) a stop pulse/space. “Low bit consists of 6 cycles of IR and 10 “cycles” of pause, high bit of 6 cycles IR and 21 “cycles” of pause and start bit of 6 cycles IR and 39 “cycles” of pause.” 

A cycle is 1/carrier frequency = 1 / 38,000 Hz = 26&mu;s. 

All pulses are the same length in the Lego:tm: protocol (6 cycles). Start, stop, high and low bits are distinguished by the pause length.
The following table shows the timings for each of the intervals and their use in the remote configuration files for each tool:

| Element          | Value in Cycles   | Value in Units           | Parameter<br /> LIRC | Parameter<br /> ir-ctl | Parameter<br /> PiIR | Parameter<br /> RPiGPIO |
| ---------------- | ----------------- | ------------------------ | --------------- | --------------- | --------------- | --------------- |
| Frequency        |                   | 38,000 Hz                | 38000<br />&bull;frequency      | 38000<br />&bull;carrier        |    <sub>(uses timebase<br />instead of frequency)</sub>          | 38000<br />&bull;frequency       |
| Cycle            | 1                 | 1 / 38,000  =  26 &mu;s  |       n/a       |       n/a       |    26<br />&bull;timebase     |    n/a          |
| Pulse            | 6                 | 6 / 38,000  = 158 &mu;s  | 158<br />&bull;ptrail   | 158<br />&bull;header_pulse<br />&bull;bit_pulse<br />&bull;trailer_pulse | 158<br />&bull;postamble<br /><sub>see below for start, one and zero</sub> | 158<br />&bull;pulse |
| Start/Stop Space | 39                | 39 / 38,000 =1,026 &mu;s | 1026<br />&bull;gap | 1026<br />&bull;header_space<br />&bull;gap | <sub>see next table</sub>| 39<br />&bull;heading_space<br />&bull;trailing_space |
| Low Bit Space    | 10                | 10 / 38,000 = 263 &mu;s  | <sub>see next table</sub>| 263<br />&bull;bit_0_space | <sub>see next table</sub>| 10<br />&bull;zero_space |
| High Bit Space   | 21                | 21 / 38,000 = 553 &mu;s  | <sub>see next table</sub>| 553<br />&bull;bit_1_space | <sub>see next table</sub>| 21<br />&bull;one_space |

The resulting bits are then:
| Bit              | Pulse             | Space             | Total Duration    |Parameter<br /> LIRC | Parameter<br /> ir-ctl | Parameter<br /> PiIR | Parameter<br /> RPiGPIO |
| ---------------- | ----------------- | ----------------- | ----------------- |--------------------------- | --- | --------------------------- | --- |
| Start/Stop       | 158  &mu;s        | 1,026 &mu;s       | 1,184 &mu;s       | 158 1026<br />&bull;header | n/a | [6, 39]<br />&bull;preamble | n/a |
| Zero/Low Bit     | 158  &mu;s        | 263 &mu;s         | 421 &mu;s         | 158 263<br />&bull;zero    | n/a | [6, 10]<br />&bull;zero     | n/a |
| One/High Bit     | 158  &mu;s        | 553 &mu;s         | 711 &mu;s         | 158 553<br />&bull;one     | n/a | [6, 21]<br />&bull;one      | n/a |

The sixteen bits are grouped into four groups of four bits or <em>nibbles</em>. The first two nibbles are configuration, except for Combo PWM where the second nibble is data. The third nibble is data. And the fourth nibble is Longitudinal Redundancy Check (a !XOR of the respective bits of the first three nibbles).

As an example, the code we used for tests is <em>Combo PWM mode - Channel 1 - Forward Step 2 / Forward Step 2</em> with the hexadecimal code 422B (each digit is a nibble). The first nibble (4) indicates the mode and channel. The second (2) and third (2) nibbles are the speeds for red and blue outputs respectively. The fourth one (B) is the LRC. The following table shows the conversion from key to pulse timings. For the timings (in &mu;s), + is a pulse, while - is a space; the first row is the start bit, the next four rows are a nibble each, and the last one is the stop bit.

| Action |Scancode<br />(Hexadecimal) | Scancode<br />(Binary) | Scancode Timings |
| ------ | -------  | ---------------- | ----------------- |
| Mode: Combo PWM<br />Channel 1<br />Output A: Forward Step 2<br />Output B: Forward Step 2 | 42 2B | Start<br />0100 (4)<br />0010 (2)<br />0010 (2)<br />1011 (B)<br />Stop |  +158 -1026 <br />+158 -263 +158 -553 +158 -263 +158 -263 <br />+158 -263 +158 -263 +158 -553 +158 -263 <br />+158 -263 +158 -263 +158 -553 +158 -263 <br />+158 -553 +158 -263 +158 -553 +158 -553<br />+158 -1026|

> **Note:** Mode and channel are not included in the keycode files because we created configuration files unique to each mode and channel 1. I create different files for different mode/channel pairs. Otherwise each file would be too large.

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
      <th>Extended</th>
      <td>• One output at a time (determined by data)<br />• Red speeds -7··+7 (set by INC/DEC), blue speeds Full Forward/Float (set by TOGGLE)<br />• No timeout. Keeps going until new key changes it<br />• Toggle address bit, but doesn't accept extended commands with address bit = 1<br />• Toggle bit is verified on receiver</td>
    </tr>
    <tr>
      <th>Combo Direct</th>
      <td>• Both outputs simultaneously<br />• Speeds Full Forward/Full Backward/Float/Break<br />• Timeout for lost IR. Goes for one second and stops unless it keeps receiving IR<br />• Toggle bit is verified on receiver</td>
    </tr>
    <tr>
      <th>Single Output: PWM</th>
      <td>• One output at a time<br />• Speeds -7··+7<br />• This mode has no timeout for lost IR. Keeps going until new key changes it<br />• Toggle bit is verified on receiver.</td>
    </tr>
    <tr>
      <th>Single Output (Other):<br />Clear/Set/Toggle/<br />Inc/Dec</th>
      <td>• One output at a time<br />• Speeds -7··+7<br />• This mode has no timeout for lost IR. Keeps going until new key changes it. Except for "full forward" and "full backward"<br />• All speed in Increments/Decrements. Numerical PWM increases value, but keeps sign; no action for float<br />• C1 and C2 seem to drive motor in opposite directions<br />• Toggle bit is verified on receiver for increment/decrement/toggle</td>
    </tr>
    <tr>
      <th>Combo PWM</th>
      <td>• Both outputs simultaneously<br />• Speeds -7··+7<br />• Timeout for lost IR. Goes for one second and stops unless it keeps receiving IR<br />• Toggle bit is not verified on receiver</td>
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
      <th colspan=4>Nibble 2</th>
      <th colspan=4>Nibble 3</th>
      <th colspan=4>Nibble 4</th>
    </tr>
    <tr>
      <th><em>T</em></th>
      <th><em>E</em></th>
      <th colspan=2><em>Ch</em></th>
      <th><em>a</em></th>
      <th colspan=3><em>Mode</em></th>
      <th colspan=4><em>Data</em></th>
      <th colspan=4><em>LRC</em></th>
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
      <td>D<sub>A</sub></td>
      <td>D<sub>A</sub></td>
      <td>L</td>
      <td>L</td>
      <td>L</td>
      <td>L</td>
    </tr>
    <tr>
      <td>Reserved</td>
      <td>T</td>
      <td>0</td>
      <td>C</td>
      <td>C</td>
      <td>0</td>
      <td>0</td>
      <td>1</td>
      <td>x</td>
      <td>x</td>
      <td>x</td>
      <td>x</td>
      <td>x</td>
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
      <td>0<sub>A</sub><br />1<sub>B</sub></td>
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
      <td>0<sub>A</sub><br />1<sub>B</sub></td>
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
      <td>D<sub>A</sub></td>
      <td>D<sub>A</sub></td>
      <td>D<sub>A</sub></td>
      <td>D<sub>A</sub></td>
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
      <td rowspan=9>Extended (<em>DDDD</em>)<br /><br /><code>T0CC 0000 <b>DDDD</b> LLLL</code></td>
      <td>0000</td><td>Brake then float output A</td></tr>
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
      <td rowspan = 4>
        Combo Direct<br />
        (<em>D<sub>A</sub>D<sub>A</sub> or D<sub>B</sub>D<sub>B</sub></em>)<br /><br />
        <code>T0CC 0001 <b>D<sub>B</sub>D<sub>B</sub>D<sub>A</sub>D<sub>A</sub></b> LLLL</code>
      </td>
      <td>00</td><td>Float</td>
    </tr>
    <tr><td>01</td><td>Full Forward</td></tr>
    <tr><td>10</td><td>Full Backward</td></tr>
    <tr><td>11</td><td>Brake then float</td></tr>
    <tr>
      <td rowspan = 16>
        Single Output: PWM (<em>DDDD</em>)<br />
        <code>T0CC 010<b>0</b> <b>D<sub>A</sub>D<sub>A</sub>D<sub>A</sub>D<sub>A</sub></b> LLLL</code><br />
        <em>or</em><br />
        <code>T0CC 010<b>1</b> <b>D<sub>B</sub>D<sub>B</sub>D<sub>B</sub>D<sub>B</sub></b> LLLL</code><br /><br /><br />
        Combo PWM (D<sub>A</sub>D<sub>A</sub>D<sub>A</sub>D<sub>A</sub> or D<sub>B</sub>D<sub>B</sub>D<sub>B</sub>D<sub>B</sub>)<br />
        <code>01CC <b>D<sub>B</sub>D<sub>B</sub>D<sub>B</sub>D<sub>B</sub> D<sub>A</sub>D<sub>A</sub>D<sub>A</sub>D<sub>A</sub></b> LLLL</code>
      </td>
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
    <tr>
      <td rowspan = 16>
        Single Output:<br />
        Clear/Set/Toggle/Inc/Dec<br />
        (<em>DDDD</em>)<br /><br />
        <code>T0CC 011<b>0</b> <b>D<sub>A</sub>D<sub>A</sub>D<sub>A</sub>D<sub>A</sub></b> LLLL</code><br />
        <em>or</em><br />
        <code>T0CC 011<b>1</b> <b>D<sub>B</sub>D<sub>B</sub>D<sub>B</sub>D<sub>B</sub></b> LLLL</code><br /><br /><br />
      </td>
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
  </tbody>
</table>


###
