import json

class Keypad:

    def __init__(self , mapped_keys_file_name: str) -> None:
        with open(mapped_keys_file_name, 'r') as mapped_keys_file:
            self.MAPPED_KEYS = json.loads(mapped_keys_file.read())
        # print(f'using {MAPPED_KEYS}')


    def is_mapped_key(self , key):
        return key in self.MAPPED_KEYS


    def get_action(self , key):
        return self.MAPPED_KEYS[key]

