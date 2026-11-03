# Acoustic Stapedial Reflex Threshold (ART) Skill

[![License: Apache-2.0](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/)
[![Zero Dependencies](https://img.shields.io/badge/zero--dependencies-standard--lib-brightgreen.svg)](requirements.txt)
[![MCP Protocol Ready](https://img.shields.io/badge/mcp-protocol--ready-orange.svg)](mcp_server.py)
[![OpenClaw Certified](https://img.shields.io/badge/openclaw-certified-purple.svg)](SKILL.md)

Zero-dependency sovereign personal agent skill for evaluating Acoustic Stapedial Reflex Thresholds (ART), sensation level (SL), 10-second reflex decay rate, and middle ear protective resilience.

```mermaid
flowchart TD
    SoundStim["Loud Acoustic Stimulus (70-105 dB HL)"] --> Cochlea["Cochlear Afferent Conduction (CN VIII)"]
    Cochlea --> Brainstem["Ventral Cochlear Nucleus & Superior Olivary Complex"]
    Brainstem --> FacialEfferent["Facial Motor Nucleus (CN VII) Efferent Limb"]
    FacialEfferent --> Stapedius["Stapedius Muscle Bilateral Contraction"]
    Stapedius --> Tympanometry["Acoustic Impedance & Reflex Decay Tracking"]
    Tympanometry --> Agent["OpenClaw / Hermes Personal Agent Sound Guarding"]
```

## Features
- **Deterministic Math**: Pure Python standard library implementation with zero external dependencies.
- **Audiology & Otology Standards**: Formulates ipsilateral/contralateral ART thresholds, Metz loudness recruitment, and acoustic reflex decay.
- **Acoustic Fatigue & Retrocochlear Guard**: Sensitive screening for auditory nerve conduction fatigue and middle ear biomechanical stiffness.
- **Model Context Protocol (MCP)**: Native JSON-RPC tool integration for LLMs and autonomous agents.

## Quickstart

```python
from client import AcousticStapedialReflexClient

client = AcousticStapedialReflexClient()
result = client.evaluate_stapedial_reflex(
    ipsilateral_threshold_db_hl=80.0,
    contralateral_threshold_db_hl=85.0,
    stimulus_freq_hz=1000,
    reflex_decay_10s_pct=12.0
)
print("Sensation Level:", result["sensation_level_db_sl"], "dB SL")
print("Middle Ear Score:", result["middle_ear_score"])
print("Classification:", result["classification"])
```

## License
Apache-2.0
