"""CLI commands entrypoint for pycpufreq."""

from time import sleep
from pycpufreq.i18n import _
from pycpufreq.core import (
    is_cpufreq_configured,
    sys_get_cpu_max_freq,
    sys_get_cpu_min_freq,
    sys_get_cpu_current_freq,
    sys_get_cpu_max_scaling_freq,
    sys_set_cpu_max_scaling_freq,
    sys_set_cpu_turbo,
)


def main() -> None:
    """Main CLI entrypoint demonstrating cpufreq features."""
    sleeptime = 2

    print(_("Is kernel cpufreq configured?:"), is_cpufreq_configured())

    if is_cpufreq_configured():
        print(_("Max cpu freq is {}").format(sys_get_cpu_max_freq()))
        print(_("Min cpu freq is {}").format(sys_get_cpu_min_freq()))
        print(_("Current cpu freq is {}").format(sys_get_cpu_current_freq()))

        print(_("Changing cpu to maximum scaling freq"))
        sys_set_cpu_max_scaling_freq(sys_get_cpu_max_freq())
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
        sys_set_cpu_max_scaling_freq(sys_get_cpu_min_freq())
        sleep(sleeptime)
        print(_("Current cpu max scaling freq is {}").format(sys_get_cpu_max_scaling_freq()))


if __name__ == "__main__":
    main()
