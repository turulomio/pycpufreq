from pathlib import Path
import subprocess
from pycpufreq.version import __version__
from pycpufreq.i18n import _

LANGUAGES = ["es", "fr", "ro", "ru", "zh", "hi"]
PACKAGE_DIR = Path(__file__).resolve().parent
LOCALE_DIR = PACKAGE_DIR / "locale"
POT_FILE = LOCALE_DIR / "pycpufreq.pot"


def translate() -> None:
    """Extract translatable strings, update PO catalogs, and compile MO binary files."""
    LOCALE_DIR.mkdir(parents=True, exist_ok=True)
    python_files = [str(p) for p in PACKAGE_DIR.glob("*.py") if p.name != "poethepoet.py"]

    subprocess.run(
        [
            "xgettext",
            "-L", "Python",
            "--no-wrap",
            "--no-location",
            "--from-code=UTF-8",
            "-o", str(POT_FILE),
            *python_files,
        ],
        check=True,
    )

    for lang in LANGUAGES:
        lang_dir = LOCALE_DIR / lang / "LC_MESSAGES"
        lang_dir.mkdir(parents=True, exist_ok=True)
        po_file = LOCALE_DIR / f"{lang}.po"

        if not po_file.exists():
            res = subprocess.run(
                ["msginit", "--no-translator", "-l", f"{lang}.UTF-8", "-i", str(POT_FILE), "-o", str(po_file)],
                capture_output=True,
            )
            if res.returncode != 0:
                po_file.write_bytes(POT_FILE.read_bytes())

        subprocess.run(
            ["msgmerge", "-N", "--no-wrap", "-U", str(po_file), str(POT_FILE)],
            check=True,
        )
        mo_file = lang_dir / "pycpufreq.mo"
        subprocess.run(
            ["msgfmt", "-cv", "-o", str(mo_file), str(po_file)],
            check=True,
        )


def release() -> None:
    """Print the step-by-step checklist for publishing a new release."""
    print(_("New Release:"))
    print(_("  * Change version and date in src/pycpufreq/version.py"))
    print(_("  * Change version in pyproject.toml"))
    print(_("  * Edit Changelog in README.md"))
    print("  * poe translate")
    print("  * mcedit src/pycpufreq/locale/es.po")
    print("  * poe translate")
    print("  * poe test")
    print(f"  * git commit -a -m 'pycpufreq-{__version__}'")
    print("  * git push")
    print(_("  * Make a new tag in github"))
    print("  * uv build")
    print("  * uv publish")
    print(_("  * Create a new gentoo ebuild with the new version"))
    print(_("  * Upload to portage repository"))
