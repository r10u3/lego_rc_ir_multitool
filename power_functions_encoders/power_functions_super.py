class LegoPF(object):

    def __init__(self, escape : int = 0,
                 channel : int = 1, mode : int = 0x4) -> None:
        """Encodes input into Lego PF codes.

        This class is subclassed by five classes, each using a different
            combo mode:
        - Extended
        - ComboDirect
        - SinglePWM
        - SingleOther
        - ComboPWM

        Functions:
            get_scancode(self, arg_1: str, arg_2: str) -> int
            get_keycode(self, arg_1: str, arg_2: str) -> str
            get_hexcode(self, arg_1: str, arg_2: str) -> str
            get_nibble1(self) -> int
            get_nibble2(self) -> int
            get_data_nibble(self, action: str) -> int
            get_nibble4(self, nibble1: int, nibble2: int, nibble3: int) -> int
            toggle_address_bit()
            toggle_toggle_bit(self) -> None
        
        Attributes:
            nibble1: the first nibble.
            nibble2: the second nibble. Except for ComboPWM
            toggle_bit: the toggle bit. Default 0.
            address_bit (int): the address bit. Default 0.


        Args:
            escape (int): determines whether to use ComboPWM or one
                of the other 4 modes (0: mode, 1: Combo PWM)
                Default = 0 (mode, not combo PWM).
            channel (int): the Lego PF channel to be used (0 to 3)
                Default = 0.
            mode: if <escape>=0, determines the mode to use
                (0: extended, 1: combo direct, 4: single output PWM,
                6: single output other)
                Default = 4 (Single PWM).
        """
        self.nibble1 = (escape << 2) | channel
        if escape == 0: 
            self.nibble2 = mode

    # Starting values
    address_bit = 0
    toggle_bit = 0

    def toggle_address_bit(self) -> None:
        """Toggle the address_bit from 0 to 1 or viceversa."""
        self.address_bit = '1' if self.address_bit == '0' else '0'

    def toggle_toggle_bit(self) -> None:
        """Toggle the toggle_bit from 0 to 1 or viceversa."""
        self.toggle_bit = 1 if self.toggle_bit == 0 else 0

    def get_nibble1(self) -> int:
        """Return nibble1 as stored in class variable by subclass."""
        return self.nibble1 | (self.toggle_bit  << 3)

    def get_nibble2(self) -> int:
        """Assemble nibble 2.
        
        Implemented by subclass.
        """
        pass

    def get_data_nibble(self, action: str) -> int:
        """Return <data_nibble> corresponding to <action>
        
        Args:
            action: the <action> to be encoded.
        """
        return self.ACTIONS.index(action)

    def get_nibble4(self, nibble1: int, nibble2: int, nibble3: int) -> int:
        "Calculate bitwise LRC for <nibble1, nibble2, nibble3>"
        return 0xf ^ nibble1 ^ nibble2 ^ nibble3

    def get_scancode(self, arg_1: str, arg_2: str) -> int:
        """Assemble the <scancode> for RC mode as integer.

        Implemented by subclasses. The arguments are different 
            for different classes.

        For Extended, Single PWM and Single Other:        
        Args:
            arg1: The <output> ('A' or 'B') to receive the action
            arg2: The <action> to be encoded.
        For Combo Direct and Combo PWM:
        Args:
            arg1: The <action_A> to be sent to output A.
            arg2: The <action_B> to be sent to output B.
        Returns:
            scancode (int): the entire scancode for the given actions
                and the pre-established class mode.
        """
        pass

    def get_keycode(self, arg_1: str, arg_2: str) -> str:
        """Assemble the <keycode> for RC mode.
        
        Implemented by subclasses. The arguments are different 
            for different classes.

        For Extended, Single PWM and Single Other:        
        Args:
            arg1: The <output> ('A' or 'B') to receive the action
            arg2: The <action> to be encoded.
        For Combo Direct and Combo PWM:
        Args:
            arg1: The <action_A> to be sent to output A.
            arg2: The <action_B> to be sent to output B.
        Returns:
            keycode (str): the keycode for the given actions and the 
                class mode.
        """
        pass
        
    def get_hexcode(self, arg_1: str, arg_2: str) -> str:
        """Return the <scancode> for RC mode as hexadecimal string.
        
        Extends get_scancode() by converting integer (0x) to 
            hexadecimal string. Used by PiIR and RPiGPIO tools only.
            The arguments are different for different classes.
        For Extended, Single PWM and Single Other:        
        Args:
            arg1: The <output> ('A' or 'B') to receive the action
            arg2: The <action> to be encoded.
        For Combo Direct and Combo PWM:
        Args:
            arg1: The <action_A> to be sent to output A.
            arg2: The <action_B> to be sent to output B.
        Returns:
            keycode (str): the entire keycode as hexadecimal string for
                the given actions and the pre-established class mode.
        """
        return f'{self.get_scancode(arg_1, arg_2):04X}'
