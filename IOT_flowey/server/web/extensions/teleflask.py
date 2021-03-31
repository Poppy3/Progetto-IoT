from ..config import TELEFLASK_API_KEY, TELEFLASK_HOSTNAME
from teleflask import Teleflask


bot = Teleflask(TELEFLASK_API_KEY, hostname=TELEFLASK_HOSTNAME, debug_routes=True)
