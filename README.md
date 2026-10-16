# copilot-devlog-cli

A lightweight Python CLI to record daily development logs and export them to Markdown.

## Requirements

- Python 3.8+

## Usage

From the repository root, run:

```bash
python devlog.py <command> [options]
```

### Add a log entry

```bash
python devlog.py add --title "Fix auth bug" --category "Bugfix" --notes "Resolved token refresh issue"
```

### View all entries

```bash
python devlog.py view
```

### Export Markdown summary

```bash
python devlog.py export
```

## Output files

- `devlog_entries.json`: local JSON storage for all entries
- `DEVLOG_SUMMARY.md`: generated Markdown summary document
