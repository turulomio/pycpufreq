"""Core functionality for CPU frequency management."""

from os import path
from pycpufreq.i18n import _

FAIL_FREQUENCY = 400000


def is_cpufreq_configured(base_path: str = "/sys/devices/system/cpu") -> bool:
    """Check if cpufreq and intel_pstate sysfs nodes exist."""
    return (
        path.exists(path.join(base_path, "cpu0/cpufreq"))
        and path.exists(path.join(base_path, "cpu0/cpufreq/cpuinfo_max_freq"))
        and path.exists(path.join(base_path, "cpu0/cpufreq/cpuinfo_min_freq"))
        and path.exists(path.join(base_path, "cpu0/cpufreq/scaling_cur_freq"))
        and path.exists(path.join(base_path, "cpu0/cpufreq/scaling_max_freq"))
        and path.exists(path.join(base_path, "intel_pstate/no_turbo"))
    )


def sys_get_cpu_max_freq(base_path: str = "/sys/devices/system/cpu") -> str | int:
    """Get maximum cpu frequency supported by cpu0."""
    if is_cpufreq_configured(base_path):
        with open(path.join(base_path, "cpu0/cpufreq/cpuinfo_max_freq")) as f:
            data = f.read()
            return data.strip()
    return FAIL_FREQUENCY


def sys_get_cpu_min_freq(base_path: str = "/sys/devices/system/cpu") -> str | int:
    """Get minimum cpu frequency supported by cpu0."""
    if is_cpufreq_configured(base_path):
        with open(path.join(base_path, "cpu0/cpufreq/cpuinfo_min_freq")) as f:
            data = f.read()
            return data.strip()
    return FAIL_FREQUENCY


def sys_get_cpu_current_freq(base_path: str = "/sys/devices/system/cpu") -> str | int:
    """Get current operating cpu frequency of cpu0."""
    if is_cpufreq_configured(base_path):
        with open(path.join(base_path, "cpu0/cpufreq/scaling_cur_freq")) as f:
            data = f.read()
            return data.strip()
    return FAIL_FREQUENCY


def sys_get_cpu_max_scaling_freq(base_path: str = "/sys/devices/system/cpu") -> str | int:
    """Get maximum scaling frequency of cpu0."""
    if is_cpufreq_configured(base_path):
        with open(path.join(base_path, "cpu0/cpufreq/scaling_max_freq")) as f:
            data = f.read()
            return data.strip()
    return FAIL_FREQUENCY


def sys_set_cpu_max_scaling_freq(freq: str | int, base_path: str = "/sys/devices/system/cpu") -> bool:
    """Set maximum scaling frequency for all available CPUs."""
    if is_cpufreq_configured(base_path):
        i = 0
        written_any = False
        try:
            while True:
                filename = path.join(base_path, f"cpu{i}/cpufreq/scaling_max_freq")
                if path.exists(filename):
                    with open(filename, "w") as f:
                        f.write(str(freq))
                    written_any = True
                    i += 1
                else:
                    break
            return written_any
        except OSError:
            print(_("Error setting sys_set_cpu_max_scaling_freq"))
            return False
    else:
        print(_("Error setting sys_set_cpu_max_scaling_freq"))
        return False


def sys_set_cpu_turbo(boolean: bool, base_path: str = "/sys/devices/system/cpu") -> bool:
    """Enable or disable CPU turbo via intel_pstate."""
    if is_cpufreq_configured(base_path):
        s = "0" if boolean else "1"
        filename = path.join(base_path, "intel_pstate/no_turbo")
        try:
            with open(filename, "w") as f:
                f.write(s)
            return True
        except OSError:
            print(_("Error setting sys_set_cpu_turbo"))
            return False
    else:
        print(_("Error setting sys_set_cpu_turbo"))
        return False
