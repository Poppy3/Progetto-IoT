################################################################################
# Collection of utility functions used in other scripts
################################################################################

# local
import config as cfg

# standard libraries
import datetime


def log(message, prefix):
    print(f'[{datetime_iso()}] - {prefix} - {message}')


def debug(message, level=1):
    if cfg.DEBUG_LEVEL and level <= cfg.DEBUG_LEVEL:
        log(message, f'DEBUG({level})')


def error(message):
    log(message, f'ERROR')


def info(message):
    log(message, f'INFO')


def warning(message):
    log(message, f'WARNING')


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


def datetime_iso(datetime_=None):
    if datetime_:
        return datetime_.isoformat()
    return datetime.datetime.now().isoformat()
