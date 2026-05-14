# Handles inconsistent transliteration found across ISKCON lecture transcripts.
# The transcript text is speech-to-text converted, so the same name can appear
# in many different spellings depending on the speaker's accent or the STT model.
#
# Add more entries here as you encounter new variants during testing.

NORMALIZATIONS = {
    "shila prabhupada":  "srila prabhupada",
    "sita prabhupada":   "srila prabhupada",
    "sheila prabhupada": "srila prabhupada",
    "parishit maharaj":  "parikshit maharaj",
    "parikshit maharaj": "parikshit maharaj",
    "maharaj rahuguna":  "maharaja rahuguna",
    "jadavarath":        "jada bharata",
    "jadabharata":       "jada bharata",
    "shingy":            "sringi",
    "shringi":           "sringi",
    "vrindaban":         "vrindavan",
    "brindaban":         "vrindavan",
    "sukhdev":           "sukadeva goswami",
    "sukdev":            "sukadeva goswami",
    "chaitanya mahaprabhu": "sri chaitanya mahaprabhu",
}


def normalize_text(text: str) -> str:
    """
    Returns a lowercased, normalized version of the text for embedding.
    The original text is preserved separately for display to users.
    """
    t = text.lower()
    for wrong, correct in NORMALIZATIONS.items():
        t = t.replace(wrong, correct)
    return t