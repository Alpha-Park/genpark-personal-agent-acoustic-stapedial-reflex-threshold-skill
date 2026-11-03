---
name: genpark-personal-agent-acoustic-stapedial-reflex-threshold-skill
version: 1.0.0
description: Zero-dependency sovereign personal agent skill for calculating Acoustic Stapedial Reflex Threshold (ART), sensation level (SL), 10-second reflex decay, and middle ear protective resilience.
author: AlphaPark Inc.
license: Apache-2.0
tags:
  - personal-agent
  - ai-agent
  - openclaw
  - genpark
  - mcp
  - mcp-server
  - model-context-protocol
  - python
  - zero-dependency
  - wellness
  - productivity
  - production-ready
metadata:
  openclaw_compatible: true
  hermes_compatible: true
  zero_dependency: true
---

# Acoustic Stapedial Reflex Threshold (ART) Skill

A sovereign personal agent capability for assessing middle ear acoustic impedance attenuation, stapedius muscle reflex threshold (ART in dB HL), reflex decay kinetics, and brainstem vestibulocochlear (CN VIII) and facial (CN VII) reflex arcs.

## Core Capabilities
- **Reflex Threshold Mapping**: Determines pure-tone acoustic reflex thresholds (500, 1000, 2000, 4000 Hz) for ipsilateral and contralateral stimulus presentations.
- **Sensation Level (SL) Calculation**: Computes dynamic difference ($ART - \text{Hearing Threshold}$), evaluating Metz cochlear loudness recruitment.
- **10-Second Acoustic Reflex Decay**: Analyzes rate of reflex adaptation at $+10\text{ dB SL}$ to screen for auditory nerve conduction fatigue and retrocochlear lesions.
- **Audio Volume & Headphone Gating**: Dynamically prescribes maximum safe decibel limits and quiet recovery intervals to protect cochlear stereocilia.

## Fast Invocation
```python
from client import AcousticStapedialReflexClient

client = AcousticStapedialReflexClient()
res = client.evaluate_stapedial_reflex(
    ipsilateral_threshold_db_hl=80.0,
    contralateral_threshold_db_hl=85.0,
    stimulus_freq_hz=1000
)
print("Sensation Level:", res["sensation_level_db_sl"], "dB SL")
print("Middle Ear Score:", res["middle_ear_score"], "/ 100")
```
