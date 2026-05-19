from pathlib import Path

SOURCE = Path("skills/message-cleaner/SKILL.md")
OUTPUT = Path("generated-hosts/claude/message-cleaner/SKILL.md")


def main() -> None:
    content = SOURCE.read_text(encoding="utf-8")

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(content, encoding="utf-8")

    print(f"Generated Claude skill: {OUTPUT}")


if __name__ == "__main__":
    main()