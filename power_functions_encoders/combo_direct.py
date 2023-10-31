import power_functions_encoders.power_functions_super as pf

class ComboDirect(pf.LegoPF):

    NAME = 'ComboDirect'

    ACTIONS = ['FLT', 'FW7', 'RV7', 'BRK']

    def __init__(self, channel : int = 0) -> None:
        """Encodes input into Lego PF codes using Combo Direct mode.

        This class subclasses LegoPF. The main differences are:
        - signature is different. Super class uses args for <escape>
            and <mode>. In Combo Direct those are fixed as 
            0 <self.nibble1 = 0x0> and 1 <self.nibble2 = 0x1>
            respectively.
        - get_nibble2() is implemented.
        - get_nibble3() extends get_data_nibble() by combining data
            for output A and output B in one.
        - get_scancode() is implemented.
        - get_keycode() is implemented.

        Args:
            channel (int): the Lego PF channel to be used (0 to 3)
                Default = 0
        """
        self.nibble1 = 0x0 | channel
        self.nibble2 = 0x1

    def get_nibble2(self) -> int:
        """Assemble <nibble 2> for the Combo Direct mode.
        
        Implements method from pr.LegoPF.
        Returns:
            nibble2 (int): the second nibble in the scancode
                for this PowerFunction mode.
        """
        return self.nibble2 | (self.address_bit  << 3)

    def get_nibble3(self, action_A: str, action_B: str) -> int:
        """Assemble <data nibble> for combo action in Combo Direct mode.

        Extends the get_data_nibble() function by combining two data
        elements into one data nibble.
        
        Args:
            action_A: the 'action' on output A to be encoded.
            action_B: the 'action' on output B to be encoded.
        Returns:
            nibble3 (int): the third nibble in the scancode
                for this PowerFunction mode.
        """
        data_A = self.get_data_nibble(action_A)
        data_B = self.get_data_nibble(action_B)
        nibble3 = (data_B << 2) | data_A
        return nibble3

    def get_scancode(self, action_A: str, action_B: str) -> int:
        """Assemble the <scancode> for output/action in Combo Direct.
        
        Args:
            action_A: the 'action' on output A to be encoded.
            action_B: the 'action' on output B to be encoded.
        Returns:
            scancode (int): the entire scancode for the given actions
                for this PowerFunction mode.
        """
        self.toggle_toggle_bit()
        nibble1 = self.get_nibble1()
        nibble2 = self.get_nibble2()
        nibble3 = self.get_nibble3(action_A, action_B)
        nibble4 = self.get_nibble4(nibble1, nibble2, nibble3)
        return (nibble1 << 12) | (nibble2 << 8) | (nibble3 << 4) | (nibble4)

    def get_keycode(self, action_A: str, action_blue: str) -> str:
        """Assemble the <keycode> for output/action in Combo Direct.
        
        Args:
            action_A: the 'action' on output A to be encoded.
            action_B: the 'action' on output B to be encoded.
        Returns:
            keycode (str): the keycode for the actions given
                for this PowerFunction mode.
        """
        return action_A + '_' + action_blue + '_' + str(self.toggle_bit)