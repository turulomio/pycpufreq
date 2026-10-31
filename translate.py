import os
from os import makedirs, system
from pathlib import Path

LANGUAGES = ["es", "fr", "ro", "ru", "zh", "hi"]
PACKAGE_DIR = Path(__file__).resolve().parent / "src" / "pycpufreq"
LOCALE_DIR = PACKAGE_DIR / "locale"
POT_FILE = LOCALE_DIR / "pycpufreq.pot"


def translate() -> None:
    """Extract translatable strings, update PO catalogs, and compile MO binary files."""
    makedirs(LOCALE_DIR, exist_ok=True)
    python_files = " ".join(f'"{p}"' for p in PACKAGE_DIR.glob("*.py"))
    system(
        f"xgettext -L Python --no-wrap --no-location --from-code='UTF-8' "
        f"-o \"{POT_FILE}\" {python_files}"
    )

    for lang in LANGUAGES:
        lang_dir = LOCALE_DIR / lang / "LC_MESSAGES"
        makedirs(lang_dir, exist_ok=True)
        po_file = LOCALE_DIR / f"{lang}.po"

        if not po_file.exists():
            # Create po file with msginit or empty header
            system(f"msginit --no-translator -l {lang}.UTF-8 -i \"{POT_FILE}\" -o \"{po_file}\" 2>/dev/null || cp \"{POT_FILE}\" \"{po_file}\"")

        system(f"msgmerge -N --no-wrap -U \"{po_file}\" \"{POT_FILE}\"")
        mo_file = lang_dir / "pycpufreq.mo"
        system(f"msgfmt -cv -o \"{mo_file}\" \"{po_file}\"")


if __name__ == "__main__":
    translate()
