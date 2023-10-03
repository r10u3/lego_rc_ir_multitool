import json

def map_keys(mapped_keys_file_name: str, rc_mode: str) -> None:
    global MAPPED_KEYS
    with open(mapped_keys_file_name, 'r') as mapped_keys_file:
        MAPPED_KEYS = json.loads(mapped_keys_file.read())
    # print(f'using {MAPPED_KEYS}')


def is_mapped_key(key):
    global MAPPED_KEYS
    return key in MAPPED_KEYS


def get_action(key):
    global MAPPED_KEYS
    return MAPPED_KEYS[key]

