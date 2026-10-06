"""Real-Time Leaderboard System
Stores participant scores in a JSON file and keeps them sorted."""

import json
import os

DATA_FILE = os.path.join("data", "leaderboard.json")


class Leaderboard:
    """Keeps all participants and their scores."""

    def __init__(self, filename=DATA_FILE):
        self.filename = filename
        self.scores = {}      # dictionary: {"Asha": 90, "Ravi": 75}
        self.load()           # read old data from the file

    # ---------- File handling ----------
    def load(self):
        """Read the scores from the file (if it exists)."""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, "r") as file:
                    self.scores = json.load(file)
            except json.JSONDecodeError:
                self.scores = {}   # file was empty or broken

    def save(self):
        """Write the scores to the file."""
        folder = os.path.dirname(self.filename)
        if folder:
            os.makedirs(folder, exist_ok=True)
        with open(self.filename, "w") as file:
            json.dump(self.scores, file, indent=4)

    # ---------- Helper ----------
    def find_name(self, name):
        """Find a name ignoring capital/small letters. Returns None if not found."""
        for existing in self.scores:
            if existing.lower() == name.strip().lower():
                return existing
        return None

    # ---------- Main features ----------
    def add_participant(self, name, score):
        name = name.strip()
        if name == "":
            return False, "Name cannot be empty."
        if self.find_name(name) is not None:
            return False, "Participant already exists. Use 'Update score'."
        self.scores[name] = score
        self.save()   # saved immediately
        return True, f"{name} added with score {score}."

    def update_score(self, name, new_score):
        existing = self.find_name(name)
        if existing is None:
            return False, "Participant not found."
        self.scores[existing] = new_score
        self.save()   # saved immediately
        return True, f"{existing}'s score updated to {new_score}."

    def get_ranking(self):
        """Return list of (name, score), highest score first."""
        return sorted(self.scores.items(), key=lambda item: item[1], reverse=True)

    def get_top_performers(self):
        """Return everyone who has the highest score (handles ties)."""
        ranking = self.get_ranking()
        if not ranking:
            return []
        highest = ranking[0][1]
        return [(name, score) for name, score in ranking if score == highest]


# ---------- Screen functions ----------
def show_leaderboard(board):
    ranking = board.get_ranking()
    if not ranking:
        print("\nLeaderboard is empty.")
        return
    print("\n===== LEADERBOARD =====")
    print(f"{'Rank':<6}{'Name':<20}{'Score':>8}")
    print("-" * 34)
    for position, (name, score) in enumerate(ranking, start=1):
        print(f"{position:<6}{name:<20}{score:>8}")


def show_top_performers(board):
    top = board.get_top_performers()
    if not top:
        print("\nNo participants yet.")
        return
    print("\n*** TOP PERFORMER(S) ***")
    for name, score in top:
        print(f"{name} - {score}")


def ask_score():
    """Keep asking until the user types a valid number."""
    while True:
        text = input("Enter score: ")
        try:
            return float(text) if "." in text else int(text)
        except ValueError:
            print("Please enter a valid number.")


def main():
    board = Leaderboard()
    while True:
        print("\n===== MENU =====")
        print("1. Add participant")
        print("2. Update score")
        print("3. View leaderboard")
        print("4. Show top performer(s)")
        print("5. Exit")
        choice = input("Choose (1-5): ").strip()

        if choice == "1":
            name = input("Enter participant name: ")
            score = ask_score()
            ok, message = board.add_participant(name, score)
            print(message)
            if ok:
                show_leaderboard(board)   # instant update
        elif choice == "2":
            name = input("Enter participant name: ")
            if board.find_name(name) is None:
                print("Participant not found.")
            else:
                score = ask_score()
                ok, message = board.update_score(name, score)
                print(message)
                show_leaderboard(board)   # instant update
        elif choice == "3":
            show_leaderboard(board)
        elif choice == "4":
            show_top_performers(board)
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please type 1 to 5.")


if __name__ == "__main__":
    main()