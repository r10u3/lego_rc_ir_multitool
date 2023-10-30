import power_functions_encoders.power_functions_super as pf

class Extended(pf.LegoPF):
    
    NAME = 'Extended'

    ACTIONS = [
        'BRK',       # Brake then float output A
        'INC',       # Increment speed on output A
        'DEC',       # Decrement speed on output A
        'NOT_USED',  # Not used
        'TOG',       # Toggle forward/float on output B
        'NOT_USED',  # Not used
        'ADD_TOG',   # Toggle Address bit
        'TOG_AGN',   # Align toggle bit (get in sync)
        'RSVD'       # Reserved
    ]

    def __init__(self, channel : int = 0) -> None:
        """Encodes input into Lego PF codes using Extended mode.

        This class subclasses LegoPF. The main differences are:
        - signature is different. Super class uses args for <escape>
            and <mode>. In Combo Direct those are fixed as 
            0 <self.nibble1 = 0x0> and 0 <self.nibble2 = 0x0>
            respectively.
        - get_nibble2() is implemented.
        - get_scancode() is implemented.
        - get_keycode() is implemented.

        Args:
            channel (int): the Lego PF channel to be used (0 to 3)
                Default = 0
        """
        self.nibble1 = 0x0 | channel
        self.nibble2 = 0x0

    def get_nibble2(self) -> int:
        """Assemble <nibble 2> for the Extended mode.
        
        Implements method from pr.LegoPF.
        Returns:
            nibble2 (int): the second nibble in the scancode
                for this PowerFunction mode.
        """
        return self.nibble2 | (self.address_bit  << 3)

    def get_scancode(self, output: str, action: str) -> int:
        """Assemble the <scancode> for output/action in Extended mode.
        
        Args:
            output: not used in this mode; left for consistency. 
                Keys mapped as [output, action] are included as
                ['', <action>]
            action: the 'action' to be encoded.
        Returns:
            scancode (int): the entire scancode for the given actions
                for this PowerFunction mode.
        """
        self.toggle_toggle_bit()
        nibble1 = self.get_nibble1()
        nibble2 = self.get_nibble2()
        nibble3 = self.get_data_nibble(action)
        nibble4 = self.get_nibble4(nibble1, nibble2, nibble3)
        return (nibble1 << 12) | (nibble2 << 8) | (nibble3 << 4) | (nibble4)

    def get_keycode(self, output: str, action: str) -> str:
        """Return <scancode> for output/action in Extended mode.
        
        Args:
            output: not used in this mode; left for consistency. 
                Keys mapped as [output, action] are included as
                ['', <action>]
            action: the 'action' to be encoded.
        Returns:
            scancode (int): the entire scancode for the given actions
                for this PowerFunction mode.
        """
        self.toggle_toggle_bit()
        keycode = action + '_' + str(self.toggle_bit) + str(self.address_bit)\
                if output == '' else\
                output + '_' + action + '_' + str(self.toggle_bit) + str(self.address_bit)
        return keycode