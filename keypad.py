import json

class Keypad:
    def __init__(self, mapped_keys_file_name: str) -> None:
        """The Keypad class maps buttons to actions.

        Args:
        mapped_keys_file_name (str): The name of the file with 
            the mapped keys.
        """
        with open(mapped_keys_file_name, 'r') as mapped_keys_file:
            self.MAPPED_KEYS = json.loads(mapped_keys_file.read())


    def is_mapped_key(self, key: str) -> bool:
        """Check whether a key (e.g., ↑) is in the button map or not.
            
        Args:
            key (str): The key to be considered (e.g., 'up' for ↑).

        Returns:
            bool: True if the key exists, False otherwise.
        """
        return key in self.MAPPED_KEYS


    def get_action(self, key: str) -> [str , str]:
        """Return the action corresponding to a key.
            
        Args:
            key (str): The key to be considered.

        Returns:
            str: The action corresponding to the key.
                The action is an array with pairs
                - [color , action] for the single output modes
                    (single PWM, single other and extended) 
                - [action A, action B] for the combo modes
                    (combo PWM and combo direct).
        """
        return self.MAPPED_KEYS[key]

