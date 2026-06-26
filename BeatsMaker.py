import hashlib
import math
import os
import random

import librosa
import numpy as np


DIFFICULTY = {
    "easy": {
        "percentile": 75,
        "strong_percentile": 90,
        "very_strong_percentile": 98,
        "subdivisions": 2,
        "max_chord": 2,
        "min_same_lane_gap_rows": 2,
    },
    "normal": {
        "percentile": 65,
        "strong_percentile": 88,
        "very_strong_percentile": 97,
        "subdivisions": 4,
        "max_chord": 2,
        "min_same_lane_gap_rows": 1,
    },
    "hard": {
        "percentile": 55,
        "strong_percentile": 82,
        "very_strong_percentile": 94,
        "subdivisions": 4,
        "max_chord": 3,
        "min_same_lane_gap_rows": 1,
    },
}


def _tempo_to_float(tempo):
    """librosa in different versions can return float or numpy array."""
    tempo_array = np.asarray(tempo).reshape(-1)
    if tempo_array.size == 0:
        return 120.0
    tempo_value = float(tempo_array[0])
    if not math.isfinite(tempo_value) or tempo_value <= 0:
        return 120.0
    return tempo_value


def _choose_lanes(rng, notes_count, last_lane_row, current_row, min_gap_rows):
    """Choose lanes, trying not to repeat the same lane too often."""
    available = [
        lane for lane in range(4)
        if current_row - last_lane_row[lane] >= min_gap_rows
    ]
    if len(available) < notes_count:
        available = list(range(4))

    rng.shuffle(available)
    return available[:notes_count]


def Analis(AUDIO_FILE, difficulty="normal"):
    """
    Creates a beat map for the selected song.

    The map is still a simple .txt file with rows like 0100 / x000.
    New lines starting with # store map metadata. UntitledBeatGame.py reads #STEP
    to keep note timing synced with the song BPM.
    """
    if not AUDIO_FILE or not os.path.exists(AUDIO_FILE):
        raise FileNotFoundError(f"Audio file not found: {AUDIO_FILE}")

    difficulty = difficulty.lower()
    settings = DIFFICULTY.get(difficulty, DIFFICULTY["normal"])

    # y = audio wave, sr = sample rate
    y, sr = librosa.load(AUDIO_FILE, sr=None, mono=True)
    duration = librosa.get_duration(y=y, sr=sr)

    hop_length = 512

    # Percussive audio helps the detector focus on drums/clicks instead of vocals/pads.
    y_percussive = librosa.effects.percussive(y)

    onset_strength = librosa.onset.onset_strength(
        y=y_percussive,
        sr=sr,
        hop_length=hop_length,
        aggregate=np.median,
    )

    tempo, beat_frames = librosa.beat.beat_track(
        y=y_percussive,
        sr=sr,
        onset_envelope=onset_strength,
        hop_length=hop_length,
        trim=False,
    )
    bpm = _tempo_to_float(tempo)
    beat_times = librosa.frames_to_time(beat_frames, sr=sr, hop_length=hop_length)

    onset_frames = librosa.onset.onset_detect(
        onset_envelope=onset_strength,
        sr=sr,
        hop_length=hop_length,
        backtrack=True,
        units="frames",
    )

    # Fallback: if onset detection finds almost nothing, use beat positions.
    if len(onset_frames) == 0:
        onset_frames = beat_frames

    positive_strengths = onset_strength[onset_strength > 0]
    if len(positive_strengths) == 0:
        positive_strengths = np.array([1.0])

    normal_threshold = float(np.percentile(positive_strengths, settings["percentile"]))
    strong_threshold = float(np.percentile(positive_strengths, settings["strong_percentile"]))
    very_strong_threshold = float(np.percentile(positive_strengths, settings["very_strong_percentile"]))

    # Grid step follows the BPM. Example: at 120 BPM normal step is about 0.125 sec.
    beat_length = 60.0 / bpm
    step = beat_length / settings["subdivisions"]
    step = max(0.10, min(0.25, step))

    rows_count = int(math.ceil(duration / step)) + 4
    rows = [["0", "0", "0", "0"] for _ in range(rows_count)]

    seed_text = f"{os.path.basename(AUDIO_FILE)}|{duration:.3f}|{bpm:.3f}|{difficulty}"
    seed = int(hashlib.md5(seed_text.encode("utf-8")).hexdigest()[:8], 16)
    rng = random.Random(seed)

    # Build candidates: onsets + beat positions. For repeated candidates on one row,
    # keep the strongest one.
    candidates_by_row = {}

    def add_candidate(time_sec, strength, is_beat=False):
        if time_sec < 0 or time_sec > duration:
            return
        row = int(round(time_sec / step))
        if row < 0 or row >= rows_count:
            return
        # Beat candidates get a small bonus so kick/snare positions are preferred.
        adjusted_strength = float(strength) * (1.15 if is_beat else 1.0)
        if adjusted_strength < normal_threshold:
            return
        old = candidates_by_row.get(row)
        if old is None or adjusted_strength > old:
            candidates_by_row[row] = adjusted_strength

    onset_times = librosa.frames_to_time(onset_frames, sr=sr, hop_length=hop_length)
    for frame, time_sec in zip(onset_frames, onset_times):
        frame = int(frame)
        frame = max(0, min(frame, len(onset_strength) - 1))
        add_candidate(time_sec, onset_strength[frame], is_beat=False)

    for frame, time_sec in zip(beat_frames, beat_times):
        frame = int(frame)
        frame = max(0, min(frame, len(onset_strength) - 1))
        add_candidate(time_sec, onset_strength[frame], is_beat=True)

    last_lane_row = [-999, -999, -999, -999]
    min_gap_rows = settings["min_same_lane_gap_rows"]

    for row, strength in sorted(candidates_by_row.items()):
        if strength >= very_strong_threshold:
            notes_count = min(settings["max_chord"], 3)
        elif strength >= strong_threshold:
            notes_count = min(settings["max_chord"], 2)
        else:
            notes_count = 1

        lanes = _choose_lanes(rng, notes_count, last_lane_row, row, min_gap_rows)
        for lane in lanes:
            rows[row][lane] = "x"
            last_lane_row[lane] = row

    map_lines = ["".join(row) for row in rows]

    text_file = f"Beats_{os.path.basename(AUDIO_FILE)}.txt"
    with open(text_file, "w", encoding="utf-8") as file:
        file.write("#BEATS_MAKER_VERSION=2\n")
        file.write(f"#AUDIO={os.path.basename(AUDIO_FILE)}\n")
        file.write(f"#BPM={bpm:.3f}\n")
        file.write(f"#STEP={step:.6f}\n")
        file.write(f"#DIFFICULTY={difficulty}\n")
        file.write("#LANES=A,S,W,D\n")
        file.write("\n".join(map_lines))

    return text_file
