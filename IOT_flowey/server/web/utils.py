import random


def human_readable_time(quotient):
    """quotient input is the time in seconds"""
    if quotient is None or quotient < 0:
        return None

    reminder = unit = unit_prev = 0
    dividers = [(60, 's', None),
                (60, 'm', 's'),
                (24, 'h', 'm'),
                (7, 'd', 'h'),
                (52, 'w', 'd'),
                (-1, 'y', 'w')]
    for divider, unit, unit_prev in dividers:
        if divider < 0 or quotient < divider:
            break
        quotient, reminder = divmod(quotient, divider)
    return f'{quotient}{unit}' + \
           (f'{reminder}{unit_prev}' if reminder > 0 else '')


def shrink_id(source_id: str, head_length: int = 3, tail_length: int = 6) -> str:
    """
    Returns a shorter version of the 'source_id' with only the first
    'head_length' characters, three dots '...', and the last 'tail_length' characters.
    """
    if len(source_id) <= head_length + tail_length:
        return source_id
    head = source_id[:head_length]
    tail = source_id[-tail_length:]
    return f'{head}...{tail}'


def randint(a, b):
    """
    Return random integer in range [a, b], including both end points.
    """
    return random.randint(a, b)


def get_random_color(alpha: bool = False) -> str:
    """
    Returns a random color string
    :param alpha: if True, a random rgba string will be returned instead of a hex-string
    """
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    if alpha:
        a = random.uniform(0, 1)
        return f'rgba({r}, {g}, {b}, {a})'
    return f'rgb({r}, {g}, {b})'
