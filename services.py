
from typing import Optional
import logging
from config import ConfigService
from bg77 import BG77

logger: Optional[logging.Logger] = None
config: Optional[ConfigService]  = None
module: Optional[BG77] = None