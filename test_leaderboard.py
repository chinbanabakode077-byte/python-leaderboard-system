from leaderboard import Leaderboard

TEST_FILE = "test_data.json"


def make_board():
    board = Leaderboard(TEST_FILE)
    board.scores = {}
    return board


def test_all():
    board = make_board()
    board.add_participant("Asha", 85)
    board.add_participant("Ravi", 92)
    board.add_participant("Meera", 78)

    assert board.get_ranking()[0] == ("Ravi", 92)      # sorted descending

    board.update_score("Meera", 99)
    assert board.get_ranking()[0] == ("Meera", 99)     # instant re-ranking

    ok, _ = board.add_participant("asha", 50)          # duplicate name
    assert ok is False

    assert board.get_top_performers() == [("Meera", 99)]

    # data must survive after reloading from file
    assert Leaderboard(TEST_FILE).scores["Meera"] == 99

    os.remove(TEST_FILE)
    print("All tests passed!")


import os
test_all()