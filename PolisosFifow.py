import os

from BeatsMaker import Analis
from BeatGameMenu import runMenu
from UntitledBeatGame import Game


DIFFICULTY = "hard"  # можно поменять на "easy" или "hard"


def map_needs_regeneration(path):
    if not path or not os.path.exists(path):
        return True

    # Old maps did not store #BEATS_MAKER_VERSION=2 and often used wrong timing.
    try:
        with open(path, "r", encoding="utf-8") as file:
            for _ in range(6):
                line = file.readline()
                if not line:
                    break
                if line.strip() == "#BEATS_MAKER_VERSION=2":
                    return False
    except OSError:
        return True

    return True


result = runMenu()

if result["event"] == "play" and result["audio"]:
    audio = result["audio"]
    way = result["way"]

    if map_needs_regeneration(way):
        way = Analis(audio, difficulty=DIFFICULTY)

    Game(audio, way)
