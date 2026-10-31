"""pycpufreq package."""

from pycpufreq.version import __version__, __version_date__, __version_datetime__
from pycpufreq.i18n import LOCALE_DIR, _, translation
from pycpufreq.core import (
    FAIL_FREQUENCY,
    is_cpufreq_configured,
    sys_get_cpu_max_freq,
    sys_get_cpu_min_freq,
    sys_get_cpu_current_freq,
    sys_get_cpu_max_scaling_freq,
    sys_set_cpu_max_scaling_freq,
    sys_set_cpu_turbo,
)

__all__ = [
    "__version__",
    "__version_date__",
    "__version_datetime__",
    "LOCALE_DIR",
    "_",
    "translation",
    "FAIL_FREQUENCY",
    "is_cpufreq_configured",
    "sys_get_cpu_max_freq",
    "sys_get_cpu_min_freq",
    "sys_get_cpu_current_freq",
    "sys_get_cpu_max_scaling_freq",
    "sys_set_cpu_max_scaling_freq",
    "sys_set_cpu_turbo",
]
