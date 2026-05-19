from pathlib import Path

OUTPUT = Path("reports/lifecycle-diagram.md")

MERMAID_DIAGRAM = '''# Skill Lifecycle Diagram

This diagram shows the proposed lifecycle states for a skill version and the events that move it between states.

```mermaid
stateDiagram-v2
    [*] --> draft

    draft --> testing: SkillUpdated
    draft --> archived: ArchiveApproved

    testing --> candidate: ValidationPassed
    testing --> rejected: ValidationFailed
    testing --> needs_review: ReviewRequired
    testing --> disabled: DisableRequested

    candidate --> active: SkillPromoted
    candidate --> rejected: PromotionRejected
    candidate --> disabled: DisableRequested
    candidate --> archived: ArchiveApproved

    active --> superseded: NewVersionPromoted
    active --> needs_review: TelemetryIssueDetected
    active --> degraded: DegradationDetected
    active --> disabled: DisableRequested
    active --> deprecated: DeprecationApproved

    needs_review --> active: ReviewPassed
    needs_review --> degraded: DegradationDetected
    needs_review --> disabled: DisableRequested
    needs_review --> deprecated: DeprecationApproved
    needs_review --> archived: ArchiveApproved

    degraded --> active: ReviewPassed
    degraded --> needs_review: FurtherIssuesDetected
    degraded --> disabled: DisableRequested
    degraded --> deprecated: DeprecationApproved

    superseded --> active: RollbackTriggered
    superseded --> deprecated: DeprecationApproved
    superseded --> archived: ArchiveApproved

    deprecated --> archived: ArchiveApproved
    deprecated --> disabled: DisableRequested

    disabled --> active: EnableApproved
    disabled --> deprecated: DeprecationApproved
    disabled --> archived: ArchiveApproved

    rejected --> draft: AuthorReworksSkill
    rejected --> archived: ArchiveApproved

    archived --> [*]
```

## Status Notes

- `draft`: skill version is still being authored.
- `testing`: CI/CD, evals, or validation checks are running.
- `candidate`: validation passed, but the version is not promoted yet.
- `active`: current recommended version.
- `superseded`: older version replaced by a newer active version.
- `needs_review`: issue detected and review is required.
- `degraded`: still usable, but quality/reliability is worse.
- `disabled`: usage is blocked.
- `deprecated`: future usage is discouraged.
- `archived`: frozen for history, auditability, or rollback reference.
- `rejected`: failed validation.
'''


def main() -> None:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(MERMAID_DIAGRAM, encoding="utf-8")

    print(f"Lifecycle diagram generated: {OUTPUT}")


if __name__ == "__main__":
    main()
