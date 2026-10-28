# Attendance Tracker

A simple command-line tool that tracks your attendance per subject and tells you
exactly how many classes you can still skip, or must attend, to stay at or above
the 75% requirement.

## Features
- Add subjects and mark each class as present or absent
- Per-subject attendance percentage
- "Can skip N more" / "Attend next N" calculation
- Data saved locally in `attendance.json`
- No external dependencies, pure Python 3

## How to run
```bash
python attendance.py            # interactive mode
python attendance.py report     # one-shot command
```

### Commands
| Command | What it does |
|---|---|
| `add <subject>` | Add a new subject |
| `present <subject>` | Mark one class attended |
| `absent <subject>` | Mark one class missed |
| `report` | Show summary table |
| `quit` | Exit |

### Example
```
> add Physics
> present Physics
> absent Physics
> report

Subject             Attended  Total       %  Status
--------------------------------------------------------------
Physics                    1      2   50.0%  LOW - attend next 4
```

## How the math works
- Attendance % = attended / total x 100
- To reach 75% you need to attend `ceil((0.75 x total - attended) / 0.25)` consecutive classes
- You can skip `floor(attended / 0.75 - total)` classes while staying above 75%

## Possible improvements
- Change the required percentage per subject
- Export the report to CSV
- Build a GUI with Tkinter or a web version with Flask

## Tech
Python 3, JSON file storage
