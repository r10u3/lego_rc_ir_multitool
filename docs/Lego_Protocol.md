
## Lego:tm: Protocol

You can find information on Lego:tm: Power Functions RC on [Philo's page on Power Functions](https://www.philohome.com/pf/pf.htm). The protocol itself is laid out in [LEGO:tm: Power Functions RC Version 1.2](LEGO_Power_Functions_RC_v120.pdf) (PDF, 370kb).

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
