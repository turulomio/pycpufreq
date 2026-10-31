"""CLI commands entrypoint for pycpufreq."""

import argparse
import sys
from time import sleep
from pycpufreq.i18n import _
from pycpufreq.version import __version__
from pycpufreq.core import (
    is_cpufreq_configured,
    sys_get_cpu_max_freq,
    sys_get_cpu_min_freq,
    sys_get_cpu_current_freq,
    sys_get_cpu_max_scaling_freq,
    sys_set_cpu_max_scaling_freq,
    sys_set_cpu_turbo,
)


def main(args: list[str] | None = None) -> int:
    """Main CLI entrypoint demonstrating cpufreq features and leaving final frequency."""
    parser = argparse.ArgumentParser(
        prog="pycpufreq",
        description=_("Manage and monitor CPU frequencies and turbo state."),
    )
    parser.add_argument(
        "-v", "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )
    parser.add_argument(
        "frequency",
        nargs="?",
        type=int,
        default=None,
        help=_("Target final CPU scaling frequency (in kHz). If omitted, maximum frequency is used."),
    )

    parsed = parser.parse_args(args)
    sleeptime = 2

    print(_("Is kernel cpufreq configured?:"), is_cpufreq_configured())

    if not is_cpufreq_configured():
        return 1

    max_freq = int(sys_get_cpu_max_freq())
    min_freq = int(sys_get_cpu_min_freq())

    # Validate target frequency if supplied
    target_freq = parsed.frequency
    if target_freq is not None:
        if target_freq < min_freq or target_freq > max_freq:
            print(
                _("Invalid frequency: {}. It must be between {} and {} kHz.").format(
                    target_freq, min_freq, max_freq
                ),
                file=sys.stderr,
            )
            return 2
    else:
        target_freq = max_freq

    print(_("Max cpu freq is {}").format(max_freq))
    print(_("Min cpu freq is {}").format(min_freq))
    print(_("Current cpu freq is {}").format(sys_get_cpu_current_freq()))

    print(_("Changing cpu to maximum scaling freq"))
    sys_set_cpu_max_scaling_freq(max_freq)
    sleep(sleeptime)
    print(_("Current cpu max scaling freq is {}").format(sys_get_cpu_max_scaling_freq()))

    print(_("Disabling turbo"))
    sys_set_cpu_turbo(False)
    sleep(sleeptime)
    print(_("Current cpu max scaling freq is {}").format(sys_get_cpu_max_scaling_freq()))

    print(_("Enabling turbo"))
    sys_set_cpu_turbo(True)
    sleep(sleeptime)
    print(_("Current cpu max scaling freq is {}").format(sys_get_cpu_max_scaling_freq()))

    print(_("Changing cpu to minimum scaling freq"))
    sys_set_cpu_max_scaling_freq(min_freq)
    sleep(sleeptime)
    print(_("Current cpu max scaling freq is {}").format(sys_get_cpu_max_scaling_freq()))

    # Leave the CPU configured with target frequency at the end
    print(_("Leaving CPU frequency at {}").format(target_freq))
    sys_set_cpu_max_scaling_freq(target_freq)
    sleep(sleeptime)
    print(_("Current cpu max scaling freq is {}").format(sys_get_cpu_max_scaling_freq()))

    return 0


if __name__ == "__main__":
    sys.exit(main())
