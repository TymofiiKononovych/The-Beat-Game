import pygame
import sys
import time
import pygame.mixer


def Game(Audio, Way):
    pygame.init()
    screen = pygame.display.set_mode((950, 600))
    pygame.display.set_caption("Untitled Beat game")
    clock = pygame.time.Clock()

    time_of_white_color = [0.0, 0.0, 0.0, 0.0]

    hits = 0
    sick = 0
    good = 0
    norm = 0
    bad = 0
    miss = 0

    Music_play = False

    # The map stores HIT times inside the song.
    # The song starts after NOTE_TRAVEL_TIME seconds, so early notes can fly in first.
    NOTE_TRAVEL_TIME = 1.0
    MUSIC_START_DELAY = NOTE_TRAVEL_TIME
    NOTE_START_Y = -70
    HIT_Y = 445
    NOTE_SPEED = (HIT_Y - NOTE_START_Y) / NOTE_TRAVEL_TIME

    # Hit windows in seconds. Time-based scoring is more accurate than Y-position scoring.
    SICK_WINDOW = 0.060
    GOOD_WINDOW = 0.110
    NORM_WINDOW = 0.170
    BAD_WINDOW = 0.250

    Digitqal_circus_beats = Way
    pygame.mixer_music.load(Audio)
    pygame.mixer_music.set_volume(0.1)

    font = pygame.font.Font("Score_fromBeatGame.ttf", 30)
    fontt = pygame.font.Font("Sick_fromBeatGame.ttf", 28)
    fonttt = pygame.font.Font("Acuraccy_FromBeatGame.ttf", 32)

    the_Buttons_X = [170, 370, 570, 770]
    button_y = 410

    # Fallback for old maps that do not have #STEP.
    delay_lines = 0.2

    collors_of_buttons_flying = [
        (255, 0, 128),
        (0, 255, 128),
        (0, 128, 255),
        (178, 102, 255),
    ]

    def readBeatGameTXT(Musik_Path):
        nonlocal delay_lines
        Beats = []
        map_lines = []

        with open(Musik_Path, "r", encoding="utf-8") as OpenTheFile:
            for raw_line in OpenTheFile:
                line = raw_line.strip()
                if not line:
                    continue

                if line.startswith("#"):
                    if line.startswith("#STEP="):
                        try:
                            delay_lines = float(line.split("=", 1)[1])
                        except ValueError:
                            delay_lines = 0.2
                    continue

                map_lines.append(line)

        for index, line in enumerate(map_lines):
            song_hit_time = index * delay_lines
            game_hit_time = MUSIC_START_DELAY + song_hit_time
            spawn_time = game_hit_time - NOTE_TRAVEL_TIME

            for index_line, symbol in enumerate(line[:4]):
                if symbol.lower() == "x":
                    Beats.append({
                        "spawn_time": max(0.0, spawn_time),
                        "hit_time": game_hit_time,
                        "X": the_Buttons_X[index_line],
                    })

        Beats.sort(key=lambda beat: beat["spawn_time"])
        return Beats

    Beats_time_X = readBeatGameTXT(Digitqal_circus_beats)
    activated_notes = []

    Start_time = time.perf_counter()

    running = True
    while running:
        current_time = time.perf_counter() - Start_time

        if not Music_play and current_time >= MUSIC_START_DELAY:
            pygame.mixer.music.play()
            Music_play = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    X_tap_Button = the_Buttons_X[0]
                    time_of_white_color[0] = 1.0
                elif event.key == pygame.K_s:
                    X_tap_Button = the_Buttons_X[1]
                    time_of_white_color[1] = 1.0
                elif event.key == pygame.K_w:
                    X_tap_Button = the_Buttons_X[2]
                    time_of_white_color[2] = 1.0
                elif event.key == pygame.K_d:
                    X_tap_Button = the_Buttons_X[3]
                    time_of_white_color[3] = 1.0
                else:
                    X_tap_Button = None

                if X_tap_Button is not None:
                    activated_notes_IN_line_list = [
                        b for b in activated_notes if b["X"] == X_tap_Button
                    ]
                    if activated_notes_IN_line_list:
                        one_Activated_note = min(
                            activated_notes_IN_line_list,
                            key=lambda b: abs(current_time - b["hit_time"]),
                        )
                        otklanenie = abs(current_time - one_Activated_note["hit_time"])

                        if otklanenie <= SICK_WINDOW:
                            sick += 1
                        elif otklanenie <= GOOD_WINDOW:
                            good += 1
                        elif otklanenie <= NORM_WINDOW:
                            norm += 1
                        elif otklanenie <= BAD_WINDOW:
                            bad += 1

                        if otklanenie <= BAD_WINDOW:
                            activated_notes.remove(one_Activated_note)
                            hits += 1

        while Beats_time_X and current_time >= Beats_time_X[0]["spawn_time"]:
            bit = Beats_time_X.pop(0)
            activated_notes.append({
                "Spawn_Time": bit["spawn_time"],
                "hit_time": bit["hit_time"],
                "X": bit["X"],
                "Y": NOTE_START_Y,
            })

        for i in activated_notes[:]:
            time_since_note_spawn = current_time - i["Spawn_Time"]
            i["Y"] = NOTE_START_Y + time_since_note_spawn * NOTE_SPEED

            if current_time > i["hit_time"] + BAD_WINDOW:
                activated_notes.remove(i)
                miss += 1

        note = hits + miss
        if note > 0:
            acurracy = (
                (0 * miss + 0.25 * bad + 0.5 * norm + 0.75 * good + 1 * sick)
                / note
                * 100
            )
        else:
            acurracy = 0.0

        for idk in range(4):
            if time_of_white_color[idk]:
                time_of_white_color[idk] -= 0.05
                if time_of_white_color[idk] < 0:
                    time_of_white_color[idk] = 0

        screen.fill((0, 0, 0))
        pygame.draw.line(
            screen,
            color=(255, 255, 255),
            start_pos=(135, 0),
            end_pos=(135, 600),
            width=3,
        )

        colors_of_Buttons = [
            (255, 0, 128),
            (0, 255, 128),
            (0, 128, 255),
            (178, 102, 255),
        ]

        for four in range(4):
            color_of_Button = colors_of_Buttons[four]
            if time_of_white_color[four] > 0:
                color_of_Button = (255, 255, 255)
            pygame.draw.rect(
                screen,
                color=color_of_Button,
                rect=(the_Buttons_X[four], button_y, 160, 70),
            )
            pygame.draw.rect(
                screen,
                color=(255, 255, 255),
                rect=(the_Buttons_X[four], button_y, 160, 70),
                width=5,
            )

        for note_rect in activated_notes:
            lane_index = the_Buttons_X.index(note_rect["X"])
            pygame.draw.rect(
                screen,
                color=collors_of_buttons_flying[lane_index],
                rect=(note_rect["X"], note_rect["Y"], 160, 70),
            )
            pygame.draw.rect(
                screen,
                color=(255, 255, 255),
                rect=(note_rect["X"], note_rect["Y"], 160, 70),
                width=5,
            )

        notes_render = font.render(f"notes: {note}", True, (255, 255, 255))
        screen.blit(notes_render, (10, 10))

        sick_render = fontt.render(f"sick: {sick}", True, (255, 0, 255))
        screen.blit(sick_render, (10, 60))

        good_render = fontt.render(f"good: {good}", True, (0, 255, 0))
        screen.blit(good_render, (10, 100))

        norm_render = fontt.render(f"norm: {norm}", True, (255, 255, 0))
        screen.blit(norm_render, (10, 140))

        bad_render = fontt.render(f"bad: {bad}", True, (225, 153, 51))
        screen.blit(bad_render, (10, 180))

        miss_render = fontt.render(f"miss: {miss}", True, (225, 0, 0))
        screen.blit(miss_render, (10, 220))

        acurracy_render = fonttt.render(
            f"acurracy: {acurracy:.1f}%", True, (225, 255, 255)
        )
        screen.blit(acurracy_render, (450, 550))

        pygame.display.flip()
        clock.tick(120)

    pygame.quit()
    sys.exit()
