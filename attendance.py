#!/usr/bin/env python3
"""Attendance Tracker - track classes attended per subject and see how many
you can still skip (or must attend) to stay above the required percentage."""

import json
import math
import sys
from pathlib import Path

DATA_FILE = Path("attendance.json")
REQUIRED = 75.0  # minimum attendance percentage


def load():
    if DATA_FILE.exists():
        return json.loads(DATA_FILE.read_text())
    return {}


def save(data):
    DATA_FILE.write_text(json.dumps(data, indent=2))


def percentage(attended, total):
    return (attended / total * 100) if total else 0.0


def classes_to_attend(attended, total, required=REQUIRED):
    """Consecutive classes you must attend to reach `required` %."""
    r = required / 100
    if percentage(attended, total) >= required:
        return 0
    return math.ceil((r * total - attended) / (1 - r))


def classes_can_skip(attended, total, required=REQUIRED):
    """Classes you can miss and still stay at or above `required` %."""
    r = required / 100
    if total == 0:
        return 0
    return max(0, math.floor(attended / r - total))


def add_subject(data, name):
    if name in data:
        print(f"'{name}' already exists.")
        return
    data[name] = {"attended": 0, "total": 0}
    print(f"Added subject '{name}'.")


def mark(data, name, present):
    if name not in data:
        print(f"No subject named '{name}'. Add it first.")
        return
    data[name]["total"] += 1
    if present:
        data[name]["attended"] += 1
    print(f"Marked {'present' if present else 'absent'} for '{name}'.")


def report(data):
    if not data:
        print("No subjects yet. Use: add <subject>")
        return
    print(f"\n{'Subject':<20}{'Attended':>9}{'Total':>7}{'%':>8}  Status")
    print("-" * 62)
    for name, rec in data.items():
        a, t = rec["attended"], rec["total"]
        pct = percentage(a, t)
        if t == 0:
            status = "no classes yet"
        elif pct >= REQUIRED:
            status = f"OK - can skip {classes_can_skip(a, t)} more"
        else:
            status = f"LOW - attend next {classes_to_attend(a, t)}"
        print(f"{name:<20}{a:>9}{t:>7}{pct:>7.1f}%  {status}")
    print()


HELP = """Commands:
  add <subject>       add a new subject
  present <subject>   mark one class as attended
  absent <subject>    mark one class as missed
  report              show attendance summary
  help                show this message
  quit                exit
"""


def handle(data, line):
    parts = line.strip().split(maxsplit=1)
    if not parts:
        return True
    cmd, arg = parts[0].lower(), (parts[1] if len(parts) > 1 else "")
    if cmd in ("quit", "exit"):
        return False
    if cmd == "help":
        print(HELP)
    elif cmd == "report":
        report(data)
    elif cmd in ("add", "present", "absent"):
        if not arg:
            print(f"Usage: {cmd} <subject>")
        elif cmd == "add":
            add_subject(data, arg)
        else:
            mark(data, arg, cmd == "present")
        save(data)
    else:
        print("Unknown command. Type 'help'.")
    return True


def main():
    data = load()
    if len(sys.argv) > 1:  # one-shot mode: python attendance.py report
        handle(data, " ".join(sys.argv[1:]))
        return
    print("Attendance Tracker (type 'help')")
    while True:
        try:
            line = input("> ")
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if not handle(data, line):
            break


if __name__ == "__main__":
    main()
