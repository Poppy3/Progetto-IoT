################################################################################
# Collection of utility functions used in other scripts
################################################################################

# local
import config as cfg

# standard libraries
import datetime
import signal


def log(message, prefix, path=None):
    to_print = f'[{datetime_iso()}] - {prefix} - {message}'
    print(to_print)
    if path is not None:
        with path.open('a', buffering=1) as f:
            f.write(to_print)
            f.write('\n')


def debug(message, level=1, path=None):
    if cfg.LOGGING.DEBUG_LEVEL and level <= cfg.LOGGING.DEBUG_LEVEL:
        log(message, f'DEBUG({level})', path)


def error(message, path=None):
    log(message, f'ERROR', path)


def info(message, path=None):
    log(message, f'INFO', path)


def warning(message, path=None):
    log(message, f'WARNING', path)


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


# taken from https://stackoverflow.com/questions/1112343/how-do-i-capture-sigint-in-python
class GracefulInterruptHandler:
    def __init__(self, signals=(signal.SIGINT, signal.SIGTERM)):
        self.signals = signals
        self.original_handlers = {}
        self.interrupted = False
        self.released = False

    def __enter__(self):
        self.interrupted = False
        self.released = False

        for sig in self.signals:
            self.original_handlers[sig] = signal.getsignal(sig)
            signal.signal(sig, self.handler)

        return self

    def handler(self, signum, frame):
        self.release()
        self.interrupted = True

    def __exit__(self, exc_type, exc_value, traceback):
        self.release()

    def release(self):
        if self.released:
            return False

        for sig in self.signals:
            signal.signal(sig, self.original_handlers[sig])

        self.released = True
        return True
