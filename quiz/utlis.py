import random
import string

def generate_random_string(length):
    """
    Generates a random string of specified length.

    Args:
        length (int): The desired length of the random string.

    Returns:
        str: A random string containing letters and digits.
    """
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))
