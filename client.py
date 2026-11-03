"""
Acoustic Stapedial Reflex Threshold (ART) & Middle Ear Protective Engine.
Provides deterministic, zero-dependency modeling of ipsilateral and contralateral stapedius reflex thresholds,
sensation levels (SL), 10-second reflex decay rate, and auditory nerve (CN VIII) / facial nerve (CN VII) arc integrity.
"""

from typing import Dict, Any, List, Optional


class AcousticStapedialReflexClient:
    """
    Deterministic client for calculating Acoustic Stapedial Reflex Thresholds (ART).
    Assesses stapedius muscle contraction, middle ear acoustic impedance attenuation,
    loudness recruitment (Metz test), and retrocochlear auditory nerve fatigue.
    """

    def __init__(self):
        pass

    def evaluate_stapedial_reflex(
        self,
        ipsilateral_threshold_db_hl: float,
        contralateral_threshold_db_hl: float,
        stimulus_freq_hz: int = 1000,
        reflex_decay_10s_pct: Optional[float] = 15.0,
        hearing_threshold_db_hl: float = 15.0
    ) -> Dict[str, Any]:
        """
        Calculates Acoustic Reflex Threshold (ART), sensation level (SL), and auditory fatigue.
        Normative values for 500 / 1000 Hz:
        - ART: 70.0 - 95.0 dB HL
        - Sensation Level (ART - Pure Tone Threshold): 65.0 - 85.0 dB SL
        - Metz recruitment test: SL < 60.0 dB suggests cochlear loudness recruitment
        - 10-second Reflex Decay at +10 dB SL: < 50.0% amplitude reduction
        - Interaural Threshold Difference: <= 15.0 dB
        """
        if ipsilateral_threshold_db_hl < 0 or contralateral_threshold_db_hl < 0:
            return {"error": "Reflex thresholds must be non-negative"}
        if stimulus_freq_hz not in (500, 1000, 2000, 4000):
            return {"error": "Supported stimulus frequencies are 500, 1000, 2000, or 4000 Hz"}

        # Sensation Level relative to pure-tone audiometric threshold
        sensation_level_db_sl = round(ipsilateral_threshold_db_hl - hearing_threshold_db_hl, 1)

        # Interaural difference
        interaural_diff_db = round(abs(ipsilateral_threshold_db_hl - contralateral_threshold_db_hl), 1)

        # Middle Ear Protective Reserve Score (0 - 100)
        score = 80.0
        if 70.0 <= ipsilateral_threshold_db_hl <= 90.0:
            score += 10.0
        elif ipsilateral_threshold_db_hl > 105.0:
            score -= 25.0
        elif ipsilateral_threshold_db_hl > 95.0:
            score -= 10.0
        elif ipsilateral_threshold_db_hl < 65.0:
            score -= 10.0  # Hyper-reflexive / hyperacusis

        if interaural_diff_db <= 10.0:
            score += 5.0
        elif interaural_diff_db > 20.0:
            score -= 15.0

        has_decay = reflex_decay_10s_pct is not None
        if has_decay:
            if reflex_decay_10s_pct <= 25.0:
                score += 5.0
            elif reflex_decay_10s_pct >= 50.0:
                score -= 30.0  # Pathological reflex decay
            elif reflex_decay_10s_pct > 35.0:
                score -= 10.0

        stapedial_score = round(min(100.0, max(5.0, score)), 1)

        is_decay_positive = has_decay and (reflex_decay_10s_pct >= 50.0)
        is_recruitment_positive = sensation_level_db_sl < 60.0 and hearing_threshold_db_hl > 25.0

        if stapedial_score >= 85.0 and not is_decay_positive:
            tier = "OPTIMAL_STAPEDIAL_ACOUSTIC_REFLEX"
            interp = f"Robust middle ear acoustic reflex (Ipsi {ipsilateral_threshold_db_hl} dB HL, Contra {contralateral_threshold_db_hl} dB HL, SL {sensation_level_db_sl} dB); no pathological decay."
            guidance = "Superior acoustic overload protection. Cochlear hair cells and brainstem reflex arc functioning optimally."
        elif is_decay_positive:
            tier = "POSITIVE_ACOUSTIC_REFLEX_DECAY"
            interp = f"Pathological reflex fatigue (Decay {reflex_decay_10s_pct}% >= 50% over 10 s at {stimulus_freq_hz} Hz); indicative of retrocochlear or vestibulocochlear nerve conduction block."
            guidance = "Significant auditory nerve fatigue detected. Avoid high-volume acoustic exposure; recommend neuro-otological workup."
        elif is_recruitment_positive:
            tier = "COCHLEAR_LOUDNESS_RECRUITMENT"
            interp = f"Narrow sensation level ({sensation_level_db_sl} dB SL < 60 dB) alongside hearing loss; indicates outer hair cell loss with abnormal inner hair cell recruitment."
            guidance = "Metz test positive for cochlear recruitment. Calibrate audio output to avoid discomfort thresholds; utilize dynamic range compression."
        elif ipsilateral_threshold_db_hl > 95.0 or contralateral_threshold_db_hl > 95.0:
            tier = "ELEVATED_STAPEDIAL_THRESHOLD"
            interp = f"Elevated acoustic reflex thresholds (Ipsi {ipsilateral_threshold_db_hl} dB HL); suggests middle ear conductive stiffness or sensorineural deficit."
            guidance = "Reduced acoustic attenuation. Use ear protection in environments exceeding 85 dBA."
        else:
            tier = "ASYMMETRIC_MIDDLE_EAR_REFLEX"
            interp = f"Interaural threshold divergence ({interaural_diff_db} dB > 15 dB); indicates unilateral middle ear or efferent facial nerve imbalance."
            guidance = "Check tympanic membrane compliance and unilateral noise exposure history."

        return {
            "stimulus_freq_hz": stimulus_freq_hz,
            "ipsilateral_threshold_db_hl": ipsilateral_threshold_db_hl,
            "contralateral_threshold_db_hl": contralateral_threshold_db_hl,
            "hearing_threshold_db_hl": hearing_threshold_db_hl,
            "sensation_level_db_sl": sensation_level_db_sl,
            "interaural_difference_db": interaural_diff_db,
            "reflex_decay_10s_pct": reflex_decay_10s_pct,
            "middle_ear_score": stapedial_score,
            "classification": tier,
            "physiological_interpretation": interp,
            "actionable_guidance": guidance
        }
