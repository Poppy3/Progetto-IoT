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
