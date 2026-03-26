from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class GuidanceSource:
    name: str
    organization: str
    url: str


@dataclass(frozen=True)
class GuidanceTechnique:
    title: str
    summary: str
    source_key: str


GUIDANCE_SOURCES: dict[str, GuidanceSource] = {
    "who_stress": GuidanceSource(
        name="Doing What Matters in Times of Stress",
        organization="World Health Organization",
        url="https://www.who.int/publications/m/item/implementing-doing-what-matters-in-times-of-stress-in-chatbots",
    ),
    "nimh_help": GuidanceSource(
        name="My Mental Health: Do I Need Help?",
        organization="National Institute of Mental Health",
        url="https://www.nimh.nih.gov/health/publications/my-mental-health-do-i-need-help",
    ),
    "nhs_mood": GuidanceSource(
        name="Dealing with stress",
        organization="NHS Every Mind Matters",
        url="https://www.nhs.uk/every-mind-matters/mental-health-issues/stress/",
    ),
    "samhsa_stress": GuidanceSource(
        name="How to Cope With Mental Health, Drug, and Alcohol Issues",
        organization="SAMHSA",
        url="https://www.samhsa.gov/find-support/how-to-cope",
    ),
}


GUIDANCE_LIBRARY: dict[str, dict[str, object]] = {
    "stress_overwhelm": {
        "signals": {
            "overwhelmed",
            "burned out",
            "burnout",
            "too much",
            "stressed",
            "pressure",
            "behind",
            "exhausted",
            "drained",
            "can't keep up",
        },
        "summary": "The user sounds overloaded or mentally stretched thin.",
        "techniques": [
            GuidanceTechnique(
                title="Shrink the next step",
                summary=(
                    "Break the problem into the smallest possible next action so the user can restart without needing full motivation."
                ),
                source_key="nimh_help",
            ),
            GuidanceTechnique(
                title="One-minute grounding pause",
                summary=(
                    "Guide the user to notice feet on the floor, slow the breath, and name what is happening right now before problem-solving."
                ),
                source_key="who_stress",
            ),
            GuidanceTechnique(
                title="Protect basic regulation",
                summary=(
                    "Encourage food, water, rest, movement, and a short screen or task break before asking the mind to do more."
                ),
                source_key="samhsa_stress",
            ),
        ],
    },
    "anxiety_worry": {
        "signals": {
            "anxious",
            "anxiety",
            "worry",
            "worried",
            "racing thoughts",
            "panic",
            "panic attack",
            "what if",
            "can't calm down",
            "uneasy",
        },
        "summary": "The user sounds stuck in worry, fear, or a body state of alarm.",
        "techniques": [
            GuidanceTechnique(
                title="Ground to the present",
                summary=(
                    "Use a brief sensory grounding exercise such as naming visible objects, sounds, or sensations to reduce spiraling."
                ),
                source_key="who_stress",
            ),
            GuidanceTechnique(
                title="Question the worry gently",
                summary=(
                    "Help the user examine what the mind is predicting and whether there is a more balanced or testable thought."
                ),
                source_key="nhs_mood",
            ),
            GuidanceTechnique(
                title="Reduce body amplifiers",
                summary=(
                    "Suggest lowering caffeine, adding a slow exhale, or stepping away from triggering input when anxiety is peaking."
                ),
                source_key="nimh_help",
            ),
        ],
    },
    "low_mood": {
        "signals": {
            "sad",
            "empty",
            "low",
            "hopeless",
            "numb",
            "unmotivated",
            "worthless",
            "down",
            "no energy",
            "can't get out of bed",
        },
        "summary": "The user may be dealing with low mood, discouragement, or emotional shutdown.",
        "techniques": [
            GuidanceTechnique(
                title="Behavior before motivation",
                summary=(
                    "Encourage one very small meaningful action now, because mood often shifts after action rather than before it."
                ),
                source_key="nimh_help",
            ),
            GuidanceTechnique(
                title="Gentle connection",
                summary=(
                    "Suggest a low-pressure point of contact with another person instead of waiting to feel social enough."
                ),
                source_key="samhsa_stress",
            ),
            GuidanceTechnique(
                title="Name the emotion without judging it",
                summary=(
                    "Help the user describe the feeling clearly and with kindness rather than treating it as a personal failure."
                ),
                source_key="nhs_mood",
            ),
        ],
    },
    "sleep": {
        "signals": {
            "can't sleep",
            "sleep",
            "insomnia",
            "waking up",
            "awake all night",
            "restless",
            "nightmares",
        },
        "summary": "The user's distress may be tied to poor sleep or difficulty winding down.",
        "techniques": [
            GuidanceTechnique(
                title="Protect a wind-down window",
                summary=(
                    "Encourage a brief pre-sleep routine with lower stimulation, dimmer light, and no pressure to sleep instantly."
                ),
                source_key="nimh_help",
            ),
            GuidanceTechnique(
                title="Offload the thought loop",
                summary=(
                    "Suggest writing worries or tomorrow's tasks down so the brain is not trying to hold them all through the night."
                ),
                source_key="nhs_mood",
            ),
            GuidanceTechnique(
                title="Reset the body gently",
                summary=(
                    "Use slow breathing, a body scan, or unclenching muscles rather than fighting with wakefulness."
                ),
                source_key="who_stress",
            ),
        ],
    },
    "loneliness_relationships": {
        "signals": {
            "lonely",
            "alone",
            "nobody",
            "isolated",
            "relationship",
            "breakup",
            "fight",
            "argument",
            "rejected",
        },
        "summary": "The user may be hurting from isolation, conflict, or loss in a relationship.",
        "techniques": [
            GuidanceTechnique(
                title="Name the relational wound",
                summary=(
                    "Reflect whether the user feels rejected, disconnected, unsafe, or unseen so the support matches the real hurt."
                ),
                source_key="nhs_mood",
            ),
            GuidanceTechnique(
                title="Choose one reachable person",
                summary=(
                    "Encourage one realistic contact point instead of making the user feel they need a perfect support network immediately."
                ),
                source_key="samhsa_stress",
            ),
            GuidanceTechnique(
                title="Use a steadying action first",
                summary=(
                    "Suggest grounding or a short walk before responding in the middle of a charged conflict."
                ),
                source_key="who_stress",
            ),
        ],
    },
    "general_distress": {
        "signals": set(),
        "summary": "The user sounds emotionally strained but the exact problem is not yet clear.",
        "techniques": [
            GuidanceTechnique(
                title="Slow down and identify the main pain point",
                summary=(
                    "Help the user sort whether this is mostly stress, anxiety, sadness, anger, loneliness, or exhaustion before offering several solutions."
                ),
                source_key="who_stress",
            ),
            GuidanceTechnique(
                title="Start with one stabilizing step",
                summary=(
                    "Offer a small grounding or regulation step first so the conversation stays helpful instead of abstract."
                ),
                source_key="nimh_help",
            ),
        ],
    },
}


def infer_concerns(message: str, history: list[dict]) -> list[str]:
    combined_text = " ".join(
        [item.get("content", "") for item in history[-3:]] + [message]
    ).lower()

    scored: list[tuple[int, str]] = []
    for concern, entry in GUIDANCE_LIBRARY.items():
        signals = entry["signals"]
        score = sum(1 for signal in signals if signal in combined_text)
        if score > 0:
            scored.append((score, concern))

    if not scored:
        return ["general_distress"]

    scored.sort(key=lambda item: (-item[0], item[1]))
    concerns = [concern for _, concern in scored[:2]]
    return concerns


def build_guidance_context(message: str, history: list[dict]) -> str:
    concerns = infer_concerns(message, history)
    concern_blocks: list[str] = []

    for concern in concerns:
        entry = GUIDANCE_LIBRARY[concern]
        concern_blocks.append(f"- Likely concern: {concern.replace('_', ' ')}")
        concern_blocks.append(f"  Summary: {entry['summary']}")
        for technique in entry["techniques"]:
            source = GUIDANCE_SOURCES[technique.source_key]
            concern_blocks.append(
                f"  Technique: {technique.title} | Why it helps: {technique.summary} | Source: {source.organization}"
            )

    return "\n".join(
        [
            "Evidence-based guidance notes for this turn:",
            *concern_blocks,
            "Support strategy:",
            "- First show that you understand what the user's main problem seems to be.",
            "- If the problem is still unclear, ask one clarifying question before offering more than one coping idea.",
            "- If the problem is clear enough, offer 2 or 3 practical options that fit this exact situation.",
            "- Explain briefly why each option fits the user's current problem.",
            "- Prefer low-burden actions the user can try in the next 2 to 15 minutes.",
            "- If symptoms sound intense, persistent, or are affecting daily functioning, gently encourage professional support.",
            "- Do not keep the conversation going just to sound warm. Be useful, specific, and calm.",
        ]
    )
