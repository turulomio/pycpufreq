from pathlib import Path
import pytest
from pycpufreq import (
    is_cpufreq_configured,
    sys_get_cpu_max_freq,
    sys_get_cpu_min_freq,
    sys_get_cpu_current_freq,
    sys_get_cpu_max_scaling_freq,
    sys_set_cpu_max_scaling_freq,
    sys_set_cpu_turbo,
    FAIL_FREQUENCY,
)


@pytest.fixture
def fake_sysfs(tmp_path: Path) -> Path:
    """Create a mock sysfs structure for CPU frequency and intel_pstate."""
    cpu0_cpufreq = tmp_path / "cpu0" / "cpufreq"
    cpu0_cpufreq.mkdir(parents=True)
    (cpu0_cpufreq / "cpuinfo_max_freq").write_text("3200000\n")
    (cpu0_cpufreq / "cpuinfo_min_freq").write_text("800000\n")
    (cpu0_cpufreq / "scaling_cur_freq").write_text("1800000\n")
    (cpu0_cpufreq / "scaling_max_freq").write_text("3000000\n")

    cpu1_cpufreq = tmp_path / "cpu1" / "cpufreq"
    cpu1_cpufreq.mkdir(parents=True)
    (cpu1_cpufreq / "scaling_max_freq").write_text("3000000\n")

    intel_pstate = tmp_path / "intel_pstate"
    intel_pstate.mkdir(parents=True)
    (intel_pstate / "no_turbo").write_text("0\n")

    return tmp_path


def test_is_cpufreq_configured_true(fake_sysfs: Path):
    assert is_cpufreq_configured(str(fake_sysfs)) is True


def test_is_cpufreq_configured_false(tmp_path: Path):
    assert is_cpufreq_configured(str(tmp_path)) is False


def test_sys_get_cpu_max_freq(fake_sysfs: Path):
    assert sys_get_cpu_max_freq(str(fake_sysfs)) == "3200000"


def test_sys_get_cpu_max_freq_fail(tmp_path: Path):
    assert sys_get_cpu_max_freq(str(tmp_path)) == FAIL_FREQUENCY


def test_sys_get_cpu_min_freq(fake_sysfs: Path):
    assert sys_get_cpu_min_freq(str(fake_sysfs)) == "800000"


def test_sys_get_cpu_min_freq_fail(tmp_path: Path):
    assert sys_get_cpu_min_freq(str(tmp_path)) == FAIL_FREQUENCY


def test_sys_get_cpu_current_freq(fake_sysfs: Path):
    assert sys_get_cpu_current_freq(str(fake_sysfs)) == "1800000"


def test_sys_get_cpu_current_freq_fail(tmp_path: Path):
    assert sys_get_cpu_current_freq(str(tmp_path)) == FAIL_FREQUENCY


def test_sys_get_cpu_max_scaling_freq(fake_sysfs: Path):
    assert sys_get_cpu_max_scaling_freq(str(fake_sysfs)) == "3000000"


def test_sys_get_cpu_max_scaling_freq_fail(tmp_path: Path):
    assert sys_get_cpu_max_scaling_freq(str(tmp_path)) == FAIL_FREQUENCY


def test_sys_set_cpu_max_scaling_freq(fake_sysfs: Path):
    result = sys_set_cpu_max_scaling_freq(2500000, str(fake_sysfs))
    assert result is True
    assert (fake_sysfs / "cpu0" / "cpufreq" / "scaling_max_freq").read_text() == "2500000"
    assert (fake_sysfs / "cpu1" / "cpufreq" / "scaling_max_freq").read_text() == "2500000"


def test_sys_set_cpu_max_scaling_freq_unconfigured(tmp_path: Path, capsys):
    result = sys_set_cpu_max_scaling_freq(2500000, str(tmp_path))
    assert result is False
    captured = capsys.readouterr()
    assert (
        "Error setting sys_set_cpu_max_scaling_freq" in captured.out
        or "Error al establecer sys_set_cpu_max_scaling_freq" in captured.out
    )


def test_sys_set_cpu_turbo_enable_and_disable(fake_sysfs: Path):
    # Enable turbo: sets no_turbo to 0
    assert sys_set_cpu_turbo(True, str(fake_sysfs)) is True
    assert (fake_sysfs / "intel_pstate" / "no_turbo").read_text() == "0"

    # Disable turbo: sets no_turbo to 1
    assert sys_set_cpu_turbo(False, str(fake_sysfs)) is True
    assert (fake_sysfs / "intel_pstate" / "no_turbo").read_text() == "1"


def test_sys_set_cpu_turbo_unconfigured(tmp_path: Path, capsys):
    result = sys_set_cpu_turbo(True, str(tmp_path))
    assert result is False
    captured = capsys.readouterr()
    assert (
        "Error setting sys_set_cpu_turbo" in captured.out
        or "Error al establecer sys_set_cpu_turbo" in captured.out
    )


def test_gettext_translation():
    import gettext
    from pycpufreq import LOCALE_DIR

    t_es = gettext.translation("pycpufreq", localedir=str(LOCALE_DIR), languages=["es"], fallback=False)
    _es = t_es.gettext
    assert _es("Disabling turbo") == "Desactivando turbo"
    assert _es("Enabling turbo") == "Activando turbo"
