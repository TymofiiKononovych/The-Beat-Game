import pygame
import tkinter as tk
import tkinter.filedialog
import os
import math as m


def runMenu():
    cadr = 0
    centr_qd = [475, 250]
    centr_qd_2 = [475, 362]
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((950, 600))
    pygame.display.set_caption("Untitled Beat game Menu")
    navedenie = pygame.mixer.Sound("SetButton.mp3")
    navedenie_naoborot = pygame.mixer.Sound("UnSetButton.mp3")
    pygame.mixer_music.load("MenuMusik.mp3")
    PressSound = pygame.mixer.Sound("PressSound.mp3")
    musik = None
    message = ""
    message_timer = 0

    font = pygame.font.Font("start_game.ttf", 40)
    fontt = pygame.font.Font("start_game.ttf", 30)

    photo = pygame.image.load("menu photo.jpg").convert()
    photo = pygame.transform.scale(photo, (950, 600))
    StartGameButton = pygame.Rect(325, 200, 300, 100)
    TextButton = pygame.Rect(311, 322, 300, 70)
    pygame.mixer.music.play()
    was_Navedeno = False
    was_Navedeno_2 = False
    running = True

    while running:
        mouse_pos = pygame.mouse.get_pos()
        IFmouseON_StartGameButton = StartGameButton.collidepoint(mouse_pos)
        IFmouseON_TextButtonButton = TextButton.collidepoint(mouse_pos)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if IFmouseON_StartGameButton:
                    PressSound.play()
                    if musik:
                        pygame.mixer.music.stop()
                        pygame.quit()
                        return {
                            "event": "play",
                            "audio": musik,
                            "way": "Beats_" + os.path.basename(musik) + ".txt",
                        }
                    else:
                        message = "Pick a song first"
                        message_timer = 180

                if IFmouseON_TextButtonButton:
                    PressSound.play()
                    okno = tk.Tk()
                    okno.withdraw()
                    okno.attributes("-topmost", True)
                    file = tkinter.filedialog.askopenfilename(
                        title="choice ur musik",
                        filetypes=[("Audio", "*.ogg *.mp3 *.wav")],
                    )
                    okno.destroy()
                    if file:
                        musik = file
                        message = ""
                        message_timer = 0

        scale = 19
        cadr += 0.0023
        denom = 1 + m.sin(cadr) ** 2
        X_knopka = scale * m.cos(cadr) / denom
        Y_knopka = scale * m.sin(cadr) * m.cos(cadr) / denom

        screen.blit(photo, (0, 0))
        if musik:
            MusikName = os.path.basename(musik)
            fonttt = pygame.font.Font("start_game.ttf", 17)
            SongsRender = fonttt.render(MusikName, True, (255, 255, 255))
            screen.blit(SongsRender, (400, 570))

        if message_timer > 0:
            message_timer -= 1
            font_message = pygame.font.Font("start_game.ttf", 22)
            message_render = font_message.render(message, True, (255, 255, 255))
            screen.blit(message_render, (365, 520))

        knopka_move = pygame.Rect(
            centr_qd[0] + X_knopka - StartGameButton.width // 2,
            centr_qd[1] + Y_knopka - StartGameButton.height // 2,
            StartGameButton.width,
            StartGameButton.height,
        )
        TextButton_move = pygame.Rect(
            centr_qd_2[0] - X_knopka - TextButton.width // 2,
            centr_qd_2[1] - Y_knopka - TextButton.height // 2,
            TextButton.width,
            TextButton.height,
        )
        text_move = (
            centr_qd[0] + X_knopka - StartGameButton.width // 2 + 40,
            centr_qd[1] + Y_knopka - StartGameButton.height // 2 + 25,
        )
        text_move_2 = (
            centr_qd_2[0] - X_knopka - TextButton_move.width // 2 + 65,
            centr_qd_2[1] - Y_knopka - TextButton.height // 2 + 15,
        )

        if IFmouseON_StartGameButton:
            knopka_move = pygame.Rect(
                knopka_move.x - 5,
                knopka_move.y - 5,
                knopka_move.width + 10,
                knopka_move.height + 10,
            )
            font = pygame.font.Font("start_game.ttf", 45)
            text_move = (
                centr_qd[0] + X_knopka - StartGameButton.width // 2 + 30,
                centr_qd[1] + Y_knopka - StartGameButton.height // 2 + 25,
            )
        else:
            font = pygame.font.Font("start_game.ttf", 40)
            text_move = (
                centr_qd[0] + X_knopka - StartGameButton.width // 2 + 40,
                centr_qd[1] + Y_knopka - StartGameButton.height // 2 + 25,
            )

        if IFmouseON_TextButtonButton:
            TextButton_move = pygame.Rect(
                TextButton_move.x - 5,
                TextButton_move.y - 5,
                TextButton_move.width + 10,
                TextButton_move.height + 10,
            )
            fontt = pygame.font.Font("start_game.ttf", 35)
            text_move_2 = (
                centr_qd_2[0] - X_knopka - TextButton.width // 2 + 55,
                centr_qd_2[1] - Y_knopka - TextButton.height // 2 + 15,
            )
        else:
            fontt = pygame.font.Font("start_game.ttf", 30)
            text_move_2 = (
                centr_qd_2[0] - X_knopka - TextButton.width // 2 + 65,
                centr_qd_2[1] - Y_knopka - TextButton.height // 2 + 15,
            )

        if IFmouseON_TextButtonButton and not was_Navedeno:
            navedenie.play()
        if not IFmouseON_TextButtonButton and was_Navedeno:
            navedenie_naoborot.play()
        if not IFmouseON_StartGameButton and was_Navedeno_2:
            navedenie_naoborot.play()
        if IFmouseON_StartGameButton and not was_Navedeno_2:
            navedenie.play()

        was_Navedeno = IFmouseON_TextButtonButton
        was_Navedeno_2 = IFmouseON_StartGameButton

        pygame.draw.rect(screen, (0, 0, 0), knopka_move, border_radius=20)
        pygame.draw.rect(screen, (255, 255, 255), knopka_move, border_radius=20, width=2)

        pygame.draw.rect(screen, (0, 0, 0), TextButton_move, border_radius=20)
        pygame.draw.rect(screen, (255, 255, 255), TextButton_move, border_radius=20, width=2)

        startGameRender = font.render("Start Game", True, (255, 255, 255))
        screen.blit(startGameRender, text_move)

        PickASongRender = fontt.render("Pick a Song", True, (255, 255, 255))
        screen.blit(PickASongRender, text_move_2)

        pygame.display.flip()
        clock.tick(240)

    pygame.mixer.music.stop()
    pygame.quit()
    return {"event": "quit", "audio": None, "way": None}
