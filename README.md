# RoboEats Cafe: Multi-Robot Task Allocation

This project implements a two-robot delivery planner in IRSim for the RoboEats Cafe environment.

Given a list of target tables, the system:
- Allocates tables across two robots.
- Optimizes visit order for each robot.
- Adds return waypoints to reduce conflicts near the kitchen.
- Runs the simulation and reports trajectory/time metrics.

## Repository Structure

```text
roboeats-multi-robot-task-allocation/
  config/
    RoboEatsCafe_config.yaml
  demo/
  docs/
    Report.pdf
  src/
    lab4.py
    my_solver.py
  .gitignore
  README.md
  requirements.txt
```

## Requirements

- Python 3.10+
- PowerShell, Command Prompt, or any shell

## Setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

If script activation is blocked in PowerShell:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
```

## Run

Run from repository root:

```powershell
python .\src\lab4.py 4 6 8 3
```

Examples:

```powershell
python .\src\lab4.py 7 9 2
python .\src\lab4.py 7 9
python .\src\lab4.py 1 4 7 9 2
```

## Expected Output

Typical terminal output includes:
- Requested table list.
- Planned routes and planned distances for each robot.
- Real trajectory length of each robot.
- Total simulation time.

Example (case `4 6 8 3`):
- `R1: [6, 8] (13.30m) | R2: [4, 3] (21.62m)`
- `Trajectory length R1: 14.33 meters`
- `Trajectory length R2: 26.34 meters`
- `Time spent: 34.20 seconds`

## Algorithm Overview

Core logic is in `src/my_solver.py`:
- `find_optimal_allocation(...)`
  - Tries all table split combinations between robots.
  - Solves route ordering for each split.
  - Chooses the best split by a combined metric.
- `solve_tsp(...)`
  - Uses brute-force permutations to find shortest visit order.
- `find_balanced_allocation(...)`
  - Splits by x-position (left/right side of cafe).
- `call(...)`
  - Evaluates both strategies.
  - Prefers balanced dual-robot routes when both robots can serve in parallel.
  - Appends return waypoints and final kitchen goals.

Simulation entry is `src/lab4.py`:
- Loads config from `config/RoboEatsCafe_config.yaml`.
- Parses CLI table IDs.
- Calls solver and executes robot goals.
- Computes and prints trajectory lengths and runtime.

## Demo Folder

The `demo/` directory is included in this repository.
