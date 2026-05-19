from pathlib import Path

SOURCE = Path("skills/message-cleaner/SKILL.md")
OUTPUT = Path("generated-hosts/copilot/.github/copilot-instructions.md")


def remove_frontmatter(content: str) -> str:
    if not content.startswith("---"):
        return content.strip()

    parts = content.split("---", 2)

    if len(parts) != 3:
        raise ValueError("Invalid frontmatter format in canonical SKILL.md")

    return parts[2].strip()


def main() -> None:
    content = SOURCE.read_text(encoding="utf-8")
    body = remove_frontmatter(content)

    output = f"""# Copilot Instructions: Message Cleaner

Use these instructions when the user asks to clean, rewrite, polish, shorten, clarify, or change the tone of a Slack, Teams, or internal message.

{body}
"""

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(output, encoding="utf-8")

    print(f"Generated Copilot instructions: {OUTPUT}")


if __name__ == "__main__":
    main()