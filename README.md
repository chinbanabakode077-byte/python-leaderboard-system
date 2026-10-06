# Real-Time Leaderboard System

A Python console application that keeps rankings of participants based on their scores.

## Features
- Add participants
- Update scores
- Rankings auto-sort in descending order
- View the current leaderboard
- Show top performer(s) (handles ties)
- Data saved in a JSON file (data/leaderboard.json)

## Requirements
- Python 3.8 or newer (no extra libraries needed)

## How to run
1. Clone this repository
2. Open a terminal in the project folder
3. Run: `python leaderboard.py`

## How to test
`python test_leaderboard.py`

## Logic summary
- Scores are stored in a dictionary {name: score}.
- Every add/update saves the data to a JSON file immediately.
- The leaderboard uses `sorted(..., reverse=True)` each time it is shown, so ranking is always current.

## Concepts used
Control structures, functions, dictionary, OOP (class), file handling (JSON).

## Author
Chinmay banabakode