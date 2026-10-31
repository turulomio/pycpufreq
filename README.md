# pycpufreq

<p align="center">
  <a href="https://github.com/turulomio/pycpufreq/actions/workflows/ci.yml">
    <img src="https://github.com/turulomio/pycpufreq/actions/workflows/ci.yml/badge.svg" alt="CI Status" />
  </a>
  <a href="https://pypi.org/project/pycpufreq/">
    <img src="https://img.shields.io/pypi/v/pycpufreq.svg" alt="PyPI version" />
  </a>
  <a href="https://pypi.org/project/pycpufreq/">
    <img src="https://img.shields.io/pypi/pyversions/pycpufreq.svg" alt="Python Versions" />
  </a>
  <a href="https://github.com/turulomio/pycpufreq/blob/main/LICENSE">
    <img src="https://img.shields.io/github/license/turulomio/pycpufreq.svg" alt="License" />
  </a>
  <a href="https://github.com/astral-sh/uv">
    <img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json" alt="uv" />
  </a>
</p>

---

**pycpufreq** is a modern Python library and CLI utility to monitor and configure CPU scaling frequencies and Intel Turbo Boost via Linux `sysfs` (`/sys/devices/system/cpu`).

## ✨ Key Features

- **Query CPU Frequencies**: Retrieve minimum, maximum, current, and scaling CPU frequencies.
- **Multicore Scaling Configuration**: Safely set scaling maximum frequency across all present CPU cores (`cpu0`, `cpu1`, ...).
- **Intel Turbo Boost Toggle**: Enable or disable turbo state on Intel processors through `intel_pstate/no_turbo`.
- **Target Frequency Validation**: CLI validates custom frequencies against real hardware bounds ($f_{min} \le f_{target} \le f_{max}$).
- **Standard Internationalization (`gettext`)**: Multi-language support (English, Spanish, French, Romanian, Russian, Chinese, Hindi).
- **Modern Packaging with `uv` & `poethepoet`**: High-performance task runner, dependency management and zero-dependency runtime.

---

## 📦 Installation

Install with `uv`:

```bash
uv add pycpufreq
```

Or using `pip`:

```bash
pip install pycpufreq
```

---

## 🚀 Quick Start

### Python Library

```python
from pycpufreq import (
    is_cpufreq_configured,
    sys_get_cpu_max_freq,
    sys_get_cpu_min_freq,
    sys_get_cpu_current_freq,
    sys_set_cpu_max_scaling_freq,
    sys_set_cpu_turbo,
)

if is_cpufreq_configured():
    print(f"Max Frequency:     {sys_get_cpu_max_freq()} kHz")
    print(f"Min Frequency:     {sys_get_cpu_min_freq()} kHz")
    print(f"Current Frequency: {sys_get_cpu_current_freq()} kHz")

    # Set scaling frequency (requires write permissions to sysfs):
    # sys_set_cpu_max_scaling_freq(2400000)

    # Enable or disable Turbo boost:
    # sys_set_cpu_turbo(True)
```

### Command Line Interface (CLI)

Run the CLI directly:

```bash
# Display CPU stats, run dynamic scaling test and restore maximum frequency:
pycpufreq

# Run and leave CPU at a validated target frequency (e.g. 2400000 kHz):
pycpufreq 2400000

# Show help & options:
pycpufreq --help
```

Or via `uv`:

```bash
uv run pycpufreq
```

---

## 🛠️ Development & Tasks

This project uses [`poethepoet`](https://github.com/nat-n/poethepoet) to streamline development tasks.

### Run Tests

```bash
poe test
# or directly:
uv run pytest
```

### Update Translations

Extract translatable strings, update catalogs and compile binary `.mo` files:

```bash
poe translate
```

### Release Checklist

Print release steps and commands for tag, build and publish:

```bash
poe release
```

---

## 📄 License

Distributed under the terms of the [GNU General Public License v3 or later (GPL-3.0-or-later)](LICENSE).
