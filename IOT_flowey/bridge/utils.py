################################################################################
# Collection of utility functions used in other scripts
################################################################################

# local
import config as cfg

# standard libraries


def debug(message):
    if cfg.DEBUG:
        print(f'DEBUG - {message}')
