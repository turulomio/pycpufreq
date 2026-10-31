import gettext
from pathlib import Path

LOCALE_DIR = Path(__file__).resolve().parent / "locale"
translation = gettext.translation("pycpufreq", localedir=str(LOCALE_DIR), fallback=True)
_ = translation.gettext
