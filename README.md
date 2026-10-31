# pycpufreq

Python library and CLI tool to inspect and configure CPU frequencies and Intel Turbo Boost via Linux sysfs interfaces (`/sys/devices/system/cpu`).

## Features

- Query CPU minimum, maximum, current, and scaling frequencies.
- Set CPU maximum scaling frequency across all available cores.
- Enable or disable Intel Turbo Boost (`intel_pstate/no_turbo`).
- Native internationalization (`gettext`) supporting Spanish (`es`), French (`fr`), Romanian (`ro`), Russian (`ru`), Chinese (`zh`), and Hindi (`hi`).
- Comprehensive unit tests using `pytest` with simulated sysfs environments.

## Installation

Using `uv`:

```bash
uv add pycpufreq
```

Or for development:

```bash
uv sync
```

## Usage

### In Python

```python
from pycpufreq import (
    is_cpufreq_configured,
    sys_get_cpu_max_freq,
    sys_get_cpu_min_freq,
    sys_get_cpu_current_freq,
    sys_get_cpu_max_scaling_freq,
    sys_set_cpu_max_scaling_freq,
    sys_set_cpu_turbo,
)

if is_cpufreq_configured():
    print(f"Max CPU frequency: {sys_get_cpu_max_freq()} kHz")
    print(f"Current frequency: {sys_get_cpu_current_freq()} kHz")

    # Set scaling frequency (requires root privileges on real system)
    # sys_set_cpu_max_scaling_freq(2500000)

    # Enable or disable Turbo boost
    # sys_set_cpu_turbo(False)
```

### CLI

Run directly with uv:

```bash
uv run pycpufreq
```

## Running Tests

Execute pytest with uv or poe:

```bash
uv run pytest
# or
poe test
```

## Translations

Extract strings, update PO catalogs, and compile MO binary catalogs using the configured task:

```bash
poe translate
# or via uv:
uv run poe translate
```
