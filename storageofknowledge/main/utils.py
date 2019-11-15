from secrets import token_hex


def get_random_key(nbytes=16):
    return token_hex(nbytes)
