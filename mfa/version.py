"""Version."""
from typing import Tuple

__version_info__: Tuple[int, ...] = (0, 1, 0)
__version__: str = ".".join(map(str, __version_info__))
