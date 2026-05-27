"""多模态学习内容可视化生成器 - 文本/PDF → 知识图谱 → 交互式HTML"""

import os
import sys
from pathlib import Path

__version__ = "0.2.0"


def _get_env_path() -> Path:
    if getattr(sys, 'frozen', False):
        return Path(sys.executable).parent / ".env"
    return Path(__file__).parent.parent / ".env"


_env_path = _get_env_path()
if _env_path.exists():
    try:
        from dotenv import load_dotenv
        load_dotenv(_env_path)
    except ImportError:
        pass
