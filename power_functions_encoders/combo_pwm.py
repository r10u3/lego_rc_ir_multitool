import power_functions_encoders.power_functions_super as pf

class ComboPWM(pf.LegoPF):
    
    NAME = 'ComboPWM'

    ACTIONS = ['FLT', 'FW1', 'FW2', 'FW3', 'FW4', 'FW5', 'FW6', 'FW7',
               'BRK', 'RV7', 'RV6', 'RV5', 'RV4', 'RV3', 'RV2', 'RV1']

    def __init__(self, channel : int = 1) -> None:
        """Encodes input into Lego PF codes using Combo PWM mode.

        This class subclasses LegoPF. The main differences are:
        - signature is different. Super class uses args for <escape>
            and <mode>. In Combo PWM those are fixed as 
            <escape> = 0 <self.nibble1 = 0x4> and <mode> is not used.
        - get_nibble1() is overriden to account for the address 
            instead of toggle bit.
        - get_nibble2() is not implemented. Nibble 2 is a data nibble
            in Combo PWM.
        - get_scancode() is implemented.
        - get_keycode() is implemented.
        Args:
            channel (int): the Lego PF channel to be used (0 to 3)
                Default = 0
        """
        self.nibble1 = 0x4 | channel

    def get_nibble1(self) -> int:
        """Assemble nibble 1 for the Combo PWM mode.
        
        Overrides method from pr.LegoPF to replace <address_bit> 
            for <toggle_bit>
        Returns:
            nibble2 (int): the second nibble in the scancode
                for this PowerFunction mode.
        """
        return self.nibble1 | (self.address_bit << 3)       # address bit instead of toggle bit

    def get_scancode(self, action_A: str, action_B: str) -> int:
        """Assemble the <scancode> for action combo in Combo PWM mode.
        
        Args:
            action_A: the 'action' on output A to be encoded.
            action_B: the 'action' on output B to be encoded.
        Returns:
            scancode (int): the entire scancode for the given actions
                for this PowerFunction mode.
        """
        self.toggle_toggle_bit()
        nibble1 = self.get_nibble1()
        nibble2 = self.get_data_nibble(action_B)
        nibble3 = self.get_data_nibble(action_A)
        nibble4 = self.get_nibble4(nibble1, nibble2, nibble3)
        return (nibble1 << 12) | (nibble2 << 8) | (nibble3 << 4) | (nibble4)

    def get_keycode(self, action_A: str, action_B: str) -> str:
        """Assemble the <keycode> for action combo in Combo PWM mode.
        
        Args:
            action_A: the 'action' on output A to be encoded.
            action_B: the 'action' on output B to be encoded.
        Returns:
            keycode (str): the keycode for the actions given
                for this PowerFunction mode.
        """
        return action_A + '_' + action_B   # no toggle for combo_pwm
