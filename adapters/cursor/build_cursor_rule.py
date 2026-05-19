from pathlib import Path

SOURCE = Path("skills/message-cleaner/SKILL.md")
OUTPUT = Path("generated-hosts/cursor/.cursor/rules/message-cleaner.mdc")


def split_frontmatter(content: str) -> tuple[str, str]:
    if not content.startswith("---"):
        return "", content.strip()

    parts = content.split("---", 2)

    if len(parts) != 3:
        raise ValueError("Invalid frontmatter format in canonical SKILL.md")

    frontmatter = parts[1].strip()
    body = parts[2].strip()

    return frontmatter, body


def main() -> None:
    content = SOURCE.read_text(encoding="utf-8")
    frontmatter, body = split_frontmatter(content)

    cursor_frontmatter = f"""---
{frontmatter}
globs:
  - "**/*"
alwaysApply: false
---"""

    output = f"{cursor_frontmatter}\n\n{body}\n"

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(output, encoding="utf-8")

    print(f"Generated Cursor rule: {OUTPUT}")


if __name__ == "__main__":
    main()