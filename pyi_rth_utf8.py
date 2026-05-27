"""PyInstaller runtime hook: force UTF-8 encoding on Windows.

This hook runs before the main script, ensuring that Python uses UTF-8
for all I/O operations. Fixes 'ascii' codec errors on non-English Windows
installations (e.g., Chinese/Korean/Japanese usernames in file paths).
"""
import sys
import os

if sys.platform == 'win32':
    # Force Python to use UTF-8 for all implicit encoding
    sys._enablelegacywindowsfsencoding()  # Undo legacy 'mbcs' if set
    os.environ.setdefault('PYTHONUTF8', '1')
    os.environ.setdefault('PYTHONIOENCODING', 'utf-8')
    os.environ.setdefault('PYTHONLEGACYWINDOWSFSENCODING', '0')
