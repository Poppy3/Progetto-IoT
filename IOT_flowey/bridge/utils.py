################################################################################
# Collection of utility functions used in other scripts
################################################################################

# local
import config as cfg

# standard libraries
# -- NONE --


def debug(message, level=1):
    if cfg.DEBUG_LEVEL and level <= cfg.DEBUG_LEVEL:
        print(f'DEBUG - {message}')


def error(message):
    print(f'ERROR - {message}')


def info(message):
    print(f'INFO - {message}')


def warning(message):
    print(f'WARNING - {message}')


def compose_filename(filename, suffix):
    assert isinstance(filename, str), 'filename must be a string'
    assert isinstance(suffix, str) or suffix is None, 'suffix, when not None, must be a string'

    if suffix is not None:
        suffix = purge_filename(suffix)
        return '{0}-{2}.{1}'.format(*filename.rsplit('.', 1), suffix)
    return filename


def purge_filename(filename):
    assert isinstance(filename, str), 'filename must be a string'

    return filename.replace('/', '.').replace('\\', '.')
