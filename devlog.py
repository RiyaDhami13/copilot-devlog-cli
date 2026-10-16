#!/usr/bin/env python3
import argparse
import json
from datetime import datetime
from pathlib import Path
from typing import Any, List

LOG_FILE = Path("devlog_entries.json")
SUMMARY_FILE = Path("DEVLOG_SUMMARY.md")


class DevlogError(Exception):
    """Raised when a devlog file cannot be read, written, or validated."""


def load_json(path: Path, default: Any) -> Any:
    """Load JSON from path, returning default only when the file is missing."""
    try:
        with path.open("r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return default
    except json.JSONDecodeError as error:
        raise DevlogError(f"Invalid JSON in {path}: {error.msg}.") from error
    except (OSError, UnicodeError) as error:
        raise DevlogError(f"Could not read {path}: {error}") from error


def load_entries(path: Path) -> List[dict]:
    data = load_json(path, [])
    if not isinstance(data, list):
        raise DevlogError(f"Log file {path} must contain a JSON list of entries.")
    if not all(isinstance(entry, dict) for entry in data):
        raise DevlogError(f"Log file {path} must contain only JSON objects.")
    return data


def save_entries(path: Path, entries: List[dict]) -> None:
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(entries, indent=2) + "\n", encoding="utf-8")
    except (OSError, TypeError, ValueError) as error:
        raise DevlogError(f"Could not write {path}: {error}") from error


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

    try:
        summary_path.parent.mkdir(parents=True, exist_ok=True)
        summary_path.write_text("\n".join(lines), encoding="utf-8")
    except (OSError, UnicodeError) as error:
        raise DevlogError(f"Could not write {summary_path}: {error}") from error
    print(f"Exported Markdown summary to {summary_path}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Developer daily devlog CLI")
    parser.add_argument(
        "--log-file",
        type=Path,
        default=LOG_FILE,
        help="JSON file used to store entries (default: devlog_entries.json)",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    add_parser = subparsers.add_parser("add", help="Add a devlog entry")
    add_parser.add_argument("--title", required=True, help="Entry title")
    add_parser.add_argument("--category", required=True, help="Entry category")
    add_parser.add_argument("--notes", required=True, help="Entry notes")

    subparsers.add_parser("view", help="View all devlog entries")
    export_parser = subparsers.add_parser(
        "export", help="Export entries to Markdown summary"
    )
    export_parser.add_argument(
        "--output",
        type=Path,
        default=SUMMARY_FILE,
        help="Markdown output file (default: DEVLOG_SUMMARY.md)",
    )

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "add":
        add_entry(args.title, args.category, args.notes, args.log_file)
    elif args.command == "view":
        view_entries(args.log_file)
    elif args.command == "export":
        export_summary(args.log_file, args.output)


if __name__ == "__main__":
    try:
        main()
    except DevlogError as error:
        raise SystemExit(f"Error: {error}") from error
