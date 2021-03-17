################################################################################
# Collection of utility functions used in other scripts
################################################################################

# local
import config as cfg

# standard libraries
# -- NONE --


def debug(message, level=1):
    if cfg.DEBUG != 0 and level <= cfg.DEBUG:
        print(f'DEBUG - {message}')
