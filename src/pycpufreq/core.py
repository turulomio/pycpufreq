"""Core functionality for CPU frequency management."""

from pathlib import Path
from pycpufreq.i18n import _

FAIL_FREQUENCY = 400000


def _resolve_path(base_path: str | Path) -> Path:
    """Helper to convert base_path to Path instance."""
    return Path(base_path)


def is_cpufreq_configured(base_path: str | Path = "/sys/devices/system/cpu") -> bool:
    """Check if cpufreq and intel_pstate sysfs nodes exist."""
    base = _resolve_path(base_path)
    return (
        (base / "cpu0" / "cpufreq").exists()
        and (base / "cpu0" / "cpufreq" / "cpuinfo_max_freq").exists()
        and (base / "cpu0" / "cpufreq" / "cpuinfo_min_freq").exists()
        and (base / "cpu0" / "cpufreq" / "scaling_cur_freq").exists()
        and (base / "cpu0" / "cpufreq" / "scaling_max_freq").exists()
        and (base / "intel_pstate" / "no_turbo").exists()
    )


def sys_get_cpu_max_freq(base_path: str | Path = "/sys/devices/system/cpu") -> str | int:
    """Get maximum cpu frequency supported by cpu0."""
    base = _resolve_path(base_path)
    if is_cpufreq_configured(base):
        try:
            return (base / "cpu0" / "cpufreq" / "cpuinfo_max_freq").read_text().strip()
        except OSError:
            return FAIL_FREQUENCY
    return FAIL_FREQUENCY


def sys_get_cpu_min_freq(base_path: str | Path = "/sys/devices/system/cpu") -> str | int:
    """Get minimum cpu frequency supported by cpu0."""
    base = _resolve_path(base_path)
    if is_cpufreq_configured(base):
        try:
            return (base / "cpu0" / "cpufreq" / "cpuinfo_min_freq").read_text().strip()
        except OSError:
            return FAIL_FREQUENCY
    return FAIL_FREQUENCY


def sys_get_cpu_current_freq(base_path: str | Path = "/sys/devices/system/cpu") -> str | int:
    """Get current operating cpu frequency of cpu0."""
    base = _resolve_path(base_path)
    if is_cpufreq_configured(base):
        try:
            return (base / "cpu0" / "cpufreq" / "scaling_cur_freq").read_text().strip()
        except OSError:
            return FAIL_FREQUENCY
    return FAIL_FREQUENCY


def sys_get_cpu_max_scaling_freq(base_path: str | Path = "/sys/devices/system/cpu") -> str | int:
    """Get maximum scaling frequency of cpu0."""
    base = _resolve_path(base_path)
    if is_cpufreq_configured(base):
        try:
            return (base / "cpu0" / "cpufreq" / "scaling_max_freq").read_text().strip()
        except OSError:
            return FAIL_FREQUENCY
    return FAIL_FREQUENCY


def sys_set_cpu_max_scaling_freq(freq: str | int, base_path: str | Path = "/sys/devices/system/cpu") -> bool:
    """Set maximum scaling frequency for all available CPUs."""
    base = _resolve_path(base_path)
    # Security validation: Ensure freq is numeric to avoid invalid writes
    try:
        val = int(freq)
        if val <= 0:
            raise ValueError()
        str_val = str(val)
    except (ValueError, TypeError):
        print(_("Error setting sys_set_cpu_max_scaling_freq"))
        return False

    if is_cpufreq_configured(base):
        i = 0
        written_any = False
        try:
            while True:
                freq_path = base / f"cpu{i}" / "cpufreq" / "scaling_max_freq"
                if freq_path.exists():
                    freq_path.write_text(str_val)
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


def sys_set_cpu_turbo(boolean: bool, base_path: str | Path = "/sys/devices/system/cpu") -> bool:
    """Enable or disable CPU turbo via intel_pstate."""
    base = _resolve_path(base_path)
    if is_cpufreq_configured(base):
        s = "0" if boolean else "1"
        target_path = base / "intel_pstate" / "no_turbo"
        try:
            target_path.write_text(s)
            return True
        except OSError:
            print(_("Error setting sys_set_cpu_turbo"))
            return False
    else:
        print(_("Error setting sys_set_cpu_turbo"))
        return False
