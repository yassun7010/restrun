from .black_config import V1BlackConfig
from .isort_config import V1IsortConfig


V1FormatConfig = V1IsortConfig | V1BlackConfig
