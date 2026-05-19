from pathlib import Path
from datetime import datetime

#Big lines:  allowed status transition -> event triggers -> simulates skill version flow -> generates report

REPORT_PATH = Path("reports/lifecycle-report.md")

# Allowed transitions for the prototype
ALLOWED_TRANSITIONS = {
    "draft": ["testing", "archived"],
    "testing": ["candidate", "rejected", "needs_review", "disabled"],
    "candidate": ["active", "rejected", "disabled", "archived"],
    "active": ["superseded", "needs_review", "degraded", "disabled", "deprecated"],
    "superseded": ["active", "deprecated", "archived"],
    "needs_review": ["active", "degraded", "disabled", "deprecated", "archived"],
    "degraded": ["active", "needs_review", "disabled", "deprecated"],
    "deprecated": ["archived", "disabled"],
    "disabled": ["active", "deprecated", "archived"],
    "archived": [],
    "rejected": ["draft", "archived"],
    "removed": [],
}

# Events that cause status changes.
# Each event can support multiple possible source statuses.
EVENT_TRANSITIONS = {
    "SkillUpdated": {
        "from": ["draft"],
        "to": "testing",
    },
    "ValidationPassed": {
        "from": ["testing"],
        "to": "candidate",
    },
    "ValidationFailed": {
        "from": ["testing"],
        "to": "rejected",
    },
    "SkillPromoted": {
        "from": ["candidate"],
        "to": "active",
    },
    "NewVersionPromoted": {
        "from": ["active"],
        "to": "superseded",
    },
    "TelemetryIssueDetected": {
        "from": ["active"],
        "to": "needs_review",
    },
    "DegradationDetected": {
        "from": ["active", "needs_review"],
        "to": "degraded",
    },
    "ReviewPassed": {
        "from": ["needs_review", "degraded"],
        "to": "active",
    },
    "RollbackTriggered": {
        "from": ["superseded"],
        "to": "active",
    },
    "DeprecationApproved": {
        "from": ["active", "superseded", "needs_review", "degraded"],
        "to": "deprecated",
    },
    "DisableRequested": {
        "from": ["active", "candidate", "testing", "needs_review", "degraded", "deprecated"],
        "to": "disabled",
    },
    "EnableApproved": {
        "from": ["disabled"],
        "to": "active",
    },
    "ArchiveApproved": {
        "from": ["deprecated", "superseded", "needs_review", "disabled", "rejected"],
        "to": "archived",
    },
}


def validate_transition(current_status: str, next_status: str) -> bool:
    return next_status in ALLOWED_TRANSITIONS.get(current_status, [])


def simulate() -> list[dict]:
    events = [
        # First version release flow
        ("message-cleaner", "0.1.0", "SkillUpdated"),
        ("message-cleaner", "0.1.0", "ValidationPassed"),
        ("message-cleaner", "0.1.0", "SkillPromoted"),

        # New version release flow
        ("message-cleaner", "0.2.0", "SkillUpdated"),
        ("message-cleaner", "0.2.0", "ValidationPassed"),
        ("message-cleaner", "0.2.0", "SkillPromoted"),

        # Old version becomes superseded once new version is promoted
        ("message-cleaner", "0.1.0", "NewVersionPromoted"),

        # Runtime telemetry detects a problem with the new active version
        ("message-cleaner", "0.2.0", "TelemetryIssueDetected"),

        # Rollback to previous stable version
        ("message-cleaner", "0.1.0", "RollbackTriggered"),

        # Problematic version gets deprecated after review
        ("message-cleaner", "0.2.0", "DeprecationApproved"),
    ]

    statuses = {
        "message-cleaner@0.1.0": "draft",
        "message-cleaner@0.2.0": "draft",
    }

    history = []

    for skill_name, version, event_name in events:
        skill_id = f"{skill_name}@{version}"
        current_status = statuses[skill_id]

        transition = EVENT_TRANSITIONS[event_name]
        allowed_sources = transition["from"]
        next_status = transition["to"]

        if current_status not in allowed_sources:
            result = "skipped"
            reason = (
                f"Expected one of {allowed_sources}, "
                f"but current status is '{current_status}'"
            )
            final_status = current_status

        elif validate_transition(current_status, next_status):
            statuses[skill_id] = next_status
            result = "success"
            reason = ""
            final_status = next_status

        else:
            result = "invalid"
            reason = f"Transition {current_status} -> {next_status} is not allowed"
            final_status = current_status

        history.append({
            "timestamp": datetime.now().isoformat(timespec="seconds"),
            "skill": skill_id,
            "event": event_name,
            "from": current_status,
            "to": final_status,
            "result": result,
            "reason": reason,
        })

    return history


def write_report(history: list[dict]) -> None:
    lines = [
        "# Lifecycle Simulation Report",
        "",
        "| Time | Skill Version | Event | From | To | Result | Notes |",
        "|---|---|---|---|---|---|---|",
    ]

    for item in history:
        lines.append(
            f"| {item['timestamp']} | {item['skill']} | {item['event']} | "
            f"{item['from']} | {item['to']} | {item['result']} | {item['reason']} |"
        )

    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")

    print(f"Lifecycle report generated: {REPORT_PATH}")


if __name__ == "__main__":
    lifecycle_history = simulate()
    write_report(lifecycle_history)