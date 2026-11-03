"""
Example Usage: Acoustic Stapedial Reflex Threshold (ART).
Demonstrates zero-dependency calculation of acoustic reflex threshold, sensation levels, reflex decay, and middle ear scoring.
"""

from client import AcousticStapedialReflexClient


def main():
    client = AcousticStapedialReflexClient()
    print("=== Acoustic Stapedial Reflex Threshold (ART) Demo ===")

    # Test Case 1: Healthy normal acoustic stapedial reflex
    res1 = client.evaluate_stapedial_reflex(
        ipsilateral_threshold_db_hl=80.0,
        contralateral_threshold_db_hl=85.0,
        stimulus_freq_hz=1000,
        reflex_decay_10s_pct=12.0,
        hearing_threshold_db_hl=10.0
    )
    print("\nTest Case 1: Healthy Middle Ear Acoustic Reflex")
    print(f"  Stimulus: {res1['stimulus_freq_hz']} Hz | Hearing Threshold: {res1['hearing_threshold_db_hl']} dB HL")
    print(f"  Ipsilateral ART: {res1['ipsilateral_threshold_db_hl']} dB HL | Sensation Level: {res1['sensation_level_db_sl']} dB SL")
    print(f"  Contralateral ART: {res1['contralateral_threshold_db_hl']} dB HL | Interaural Diff: {res1['interaural_difference_db']} dB")
    print(f"  Reflex Decay (10 s): {res1['reflex_decay_10s_pct']}%")
    print(f"  Middle Ear Score: {res1['middle_ear_score']} / 100")
    print(f"  Classification: {res1['classification']}")
    print(f"  Physiological Interpretation: {res1['physiological_interpretation']}")
    print(f"  Actionable Guidance: {res1['actionable_guidance']}")

    # Test Case 2: Positive reflex decay (auditory nerve fatigue / retrocochlear pattern)
    res2 = client.evaluate_stapedial_reflex(
        ipsilateral_threshold_db_hl=95.0,
        contralateral_threshold_db_hl=90.0,
        stimulus_freq_hz=1000,
        reflex_decay_10s_pct=65.0,
        hearing_threshold_db_hl=20.0
    )
    print("\nTest Case 2: Positive Reflex Decay (Auditory Nerve Fatigue)")
    print(f"  Ipsilateral ART: {res2['ipsilateral_threshold_db_hl']} dB HL | Sensation Level: {res2['sensation_level_db_sl']} dB SL")
    print(f"  Reflex Decay: {res2['reflex_decay_10s_pct']}%")
    print(f"  Middle Ear Score: {res2['middle_ear_score']} / 100")
    print(f"  Classification: {res2['classification']}")
    print(f"  Actionable Guidance: {res2['actionable_guidance']}")


if __name__ == "__main__":
    main()
