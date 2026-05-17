from pathlib import Path

import environ

env = environ.Env()

BASE_DIR = Path(__file__).parent.parent.parent
ENV_PATH = BASE_DIR.parent.joinpath(".env")
environ.Env.read_env(ENV_PATH)

DEBUG = env.bool("DJANGO_DEBUG")

if DEBUG:
    from .local import *
else:
    from .prod import *

