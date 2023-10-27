import power_functions_encoders.power_functions_super as pf

class SingleOther(pf.LegoPF):
    
    NAME = 'SingleOther'

    ACTIONS = [
        'TOG_0000', # Toggle full forward (Stop → Fw, Fw → Stop, Bw → Fw)
        'TOG_0001', # Toggle direction
        'INC_NUM',  # Increment numerical PWM
        'DEC_NUM',  # Decrement numerical PWM
        'INC_PWM',  # Increment PWM
        'DEC_PWM',  # Decrement PWM
        'FUL_FWD',  # Full forward (timeout)
        'FUL_REV',  # Full backward (timeout)
        'TOG_1000', # Toggle full forward/backward (default forward)
        'CLR_C1',   # Clear C1 (negative logic – C1 high)
        'SET_C1',   # Set C1 (negative logic – C1 low)
        'TOG_C1',   # Toggle C1
        'CLR_C2',   # Clear C2 (negative logic – C2 high)
        'SET_C2',   # Set C2 (negative logic – C2 low)
        'TOG_C2',   # Toggle C2
        'TOG_1111'  # Toggle full backward (Stop → Bw, Bw → Stop, Fwd → Bw)
    ]

    def __init__(self, channel : int = 1) -> None:
        """Encodes input into Lego PF codes using Single Other mode.

        This class subclasses LegoPF. The main differences are:
        - signature is different. Super class uses args for <escape>
            and <mode>. In Combo Direct those are fixed as 
            0 <self.nibble1 = 0x0> and 6 <self.nibble2 = 0x6>
            respectively.
        - get_nibble2() is implemented.
        - get_scancode() is implemented.
        - get_keycode() is implemented.

        Args:
            channel (int): the Lego PF channel to be used (0 to 3)
                Default = 0
        """
        self.nibble1 = 0x0 | channel
        self.nibble2 = 0x6

    def get_nibble2(self, output: int) -> int:
        """Assemble <nibble 2> for the Single Other mode.
        
        Implements method from LegoPF.
        Returns:
            nibble2 (int): the second nibble in the scancode
                for this PowerFunction mode.
        """
        output_bit = 0 if output == 'A' else 1
        return self.nibble2 | (self.address_bit  << 3) | output_bit     # includes output

    def get_scancode(self, output: str, action: str) -> int:
        """Assemble the <scancode> for output/action in Single Other.
        
        Args:
            output: the output ('A' or 'B') to receive the action,
            action: the 'action' to be encoded.
        Returns:
            scancode (int): the entire scancode for the given actions
                for this PowerFunction mode.
        """
        self.toggle_toggle_bit()
        nibble1 = self.get_nibble1()
        nibble2 = self.get_nibble2(output)                              # 'A' or 'B'
        nibble3 = self.get_data_nibble(action)
        nibble4 = self.get_nibble4(nibble1, nibble2, nibble3)
        return (nibble1 << 12) | (nibble2 << 8) | (nibble3 << 4) | (nibble4)

    def get_keycode(self, output: str, action: str) -> str:
        """Assemble the <keycode> for output/action in Single Other.
        
        Args:
            output: the output ('A' or 'B') to receive the action,
            action: the 'action' to be encoded.
        Returns:
            keycode (int): the entire scancode for the given actions
                for this PowerFunction mode.
        """
        self.toggle_toggle_bit()
        return output + '_' + action + '_' + str(self.toggle_bit)
