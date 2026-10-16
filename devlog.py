#!/usr/bin/env python3
import argparse
import json
from datetime import datetime
from pathlib import Path

LOG_FILE = Path("devlog_entries.json")
SUMMARY_FILE = Path("DEVLOG_SUMMARY.md")


def load_entries(path: Path) -> list:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8") as file:
        data = json.load(file)
    if not isinstance(data, list):
        raise ValueError("Log file must contain a JSON list of entries.")
    return data


def save_entries(path: Path, entries: list) -> None:
    with path.open("w", encoding="utf-8") as file:
        json.dump(entries, file, indent=2)


def add_entry(title: str, category: str, notes: str, log_path: Path) -> None:
    entries = load_entries(log_path)
    entries.append(
        {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "title": title,
            "category": category,
            "notes": notes,
        }
    )
    save_entries(log_path, entries)
    print(f"Added entry: {title}")


def view_entries(log_path: Path) -> None:
    entries = load_entries(log_path)
    if not entries:
        print("No devlog entries found.")
        return

    for index, entry in enumerate(entries, start=1):
        print(f"{index}. [{entry.get('date', 'N/A')}] {entry.get('title', 'Untitled')}")
        print(f"   Category: {entry.get('category', 'N/A')}")
        print(f"   Notes: {entry.get('notes', '')}\n")


def export_summary(log_path: Path, summary_path: Path) -> None:
    entries = load_entries(log_path)
    lines = ["# Development Log Summary", ""]

    if not entries:
        lines.append("No entries available.")
    else:
        for entry in entries:
            lines.extend(
                [
                    f"## {entry.get('date', 'N/A')} - {entry.get('title', 'Untitled')}",
                    f"- **Category:** {entry.get('category', 'N/A')}",
                    f"- **Notes:** {entry.get('notes', '')}",
                    "",
                ]
            )

    summary_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"Exported Markdown summary to {summary_path}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Developer daily devlog CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    add_parser = subparsers.add_parser("add", help="Add a devlog entry")
    add_parser.add_argument("--title", required=True, help="Entry title")
    add_parser.add_argument("--category", required=True, help="Entry category")
    add_parser.add_argument("--notes", required=True, help="Entry notes")

    subparsers.add_parser("view", help="View all devlog entries")
    subparsers.add_parser("export", help="Export entries to Markdown summary")

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "add":
        add_entry(args.title, args.category, args.notes, LOG_FILE)
    elif args.command == "view":
        view_entries(LOG_FILE)
    elif args.command == "export":
        export_summary(LOG_FILE, SUMMARY_FILE)


if __name__ == "__main__":
    main()
