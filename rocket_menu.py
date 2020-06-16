import pygame as pg
from game_tools import get_folder_file, makefont, makeimg
from game_constants import channel_3, blipselect, blipclick, bliplocked, rocket_names, milestones, main_font, lives
from game_play import game_loop


def rocket_menu(highscore, unlocked, global_running, chosen, rocket_idx, rocket_rects_locked, rocket_imgs_locked,
                rocket_imgs, rocket_rects, scr, scr_width, scr_height, volume, factor):
    running = True

    launchpad_img, launchpad_rect = makeimg("launchsite.png", False, factor)
    x_launchpad = int(scr_width / 2)
    y_launchpad0 = int(scr_height - (launchpad_img.get_size()[1] / 2))
    launchpad_rect.center = (x_launchpad, y_launchpad0)
    arrowright_img, arrowright_rect = makeimg("pointer.png", True, factor)
    arrowright_rect.center = (int(scr_width * 0.65 + scr_width / 3.5), int(scr_height / 2))
    arrowleft_img = pg.transform.flip(arrowright_img, True, False)
    arrowleft_rect = arrowleft_img.get_rect()
    arrowleft_rect.center = (int(scr_width * 0.65 - scr_width / 3.5), int(scr_height / 2))
    pointer_img, pointer_rect = makeimg("pointer.png", True, factor)
    heart_img, dummyheartrect = makeimg("heart.png", True, factor)  # rect is dummy since amount of hearts will vary
    lock_img, lock_rect = makeimg("lock.png", True, factor)
    lock_rect.center = (int(scr_width / 7), int(scr_height - 34 * factor - (20 * factor)))
    textbox_img, textbox_rect = makeimg("descriptiontextbox.png", True, factor)
    textbox_rect.center = (int(scr_width / 2), int(scr_height * 3 / 20))

    scr_txt1, scr_txt1_rect = makefont("MAIN MENU", 7, (int(scr_width * 0.65), int(scr_height / 1.35)), factor)
    scr_txt4, scr_txt4_rect = makefont("LAUNCH", 7, (int(scr_width * 0.65), int(scr_height / 1.5)), factor)
    txt_locked1, txt_locked1_rect = makefont("LOCKED", 10, (int(scr_width * 0.65), int(scr_height / 2)), factor)

    choice = 1
    new_choice = False
    to_menu = False
    pressed = False
    pressed2 = False
    play_game = False
    choice_position = (0, 0)

    # also put info here to avoid referencing before assignment
    x_rocket = int(scr_width / 7)
    y_rocket = int(scr_height - 32 * factor - (rocket_imgs[rocket_idx].get_size()[1] / 2))
    rocket_rects[rocket_idx].center = (x_rocket, y_rocket)
    rocket_rects_locked[rocket_idx].center = (x_rocket, y_rocket)

    scr_txt3, scr_txt3_rect = makefont(rocket_names[rocket_idx].upper(), 10,
                                       (int(scr_width * 0.65), int(scr_height / 2)), factor)

    # read rocket explanations from texts
    font = pg.font.Font(main_font, factor * 5)
    f = open(get_folder_file("Text", rocket_names[rocket_idx] + ".txt"), "r")
    lines = f.readlines()
    f.close()
    explain_txts = []
    explain_txts_rects = []
    j = 0
    for q in lines:
        explanation = q.strip()
        explain_txts.append(font.render(explanation.upper(), False, (255, 255, 255)))
        explain_txts_rects.append(explain_txts[j].get_rect())
        explain_txts_rects[j].center = (int(scr_width / 2), int(scr_height / 10 + j * scr_height / 20))
        j += 1

    txt_locked2, txt_locked2_rect = makefont(f"REACH {milestones[rocket_idx]:,.2f} KM TO UNLOCK.", 5,
                                             (int(scr_width / 2), int(scr_height / 10 + scr_height / 20)),
                                             factor)

    while running and global_running:
        pg.event.pump()

        if new_choice:
            x_rocket = int(scr_width / 7)
            y_rocket = int(scr_height - 32 * factor - (rocket_imgs[rocket_idx].get_size()[1] / 2))
            rocket_rects[rocket_idx].center = (x_rocket, y_rocket)
            rocket_rects_locked[rocket_idx].center = (x_rocket, y_rocket)

            scr_txt3, scr_txt3_rect = makefont(rocket_names[rocket_idx].upper(), 10,
                                               (int(scr_width * 0.65), int(scr_height / 2)), factor)

            # read rocket explanations from texts
            font = pg.font.Font(main_font, factor * 5)
            f = open(get_folder_file("Text", rocket_names[rocket_idx] + ".txt"), "r")
            lines = f.readlines()
            f.close()
            explain_txts = []
            explain_txts_rects = []
            j = 0
            for q in lines:
                explanation = q.strip()
                explain_txts.append(font.render(explanation.upper(), False, (255, 255, 255)))
                explain_txts_rects.append(explain_txts[j].get_rect())
                explain_txts_rects[j].center = (int(scr_width / 2), int(scr_height / 10 + j * scr_height / 20))
                j += 1

            txt_locked2, txt_locked2_rect = makefont(f"REACH {milestones[rocket_idx]:,.2f} KM TO UNLOCK.", 5,
                                                     (int(scr_width / 2), int(scr_height / 10 + scr_height / 20)),
                                                     factor)

            new_choice = False

        if highscore >= milestones[rocket_idx]:
            unlocked = True
        else:
            unlocked = False

        scr.blit(launchpad_img, launchpad_rect)
        scr.blit(textbox_img, textbox_rect)
        if unlocked:
            scr.blit(rocket_imgs[rocket_idx], rocket_rects[rocket_idx])
            scr.blit(scr_txt3, scr_txt3_rect)
            for p in range(len(explain_txts)):
                scr.blit(explain_txts[p], explain_txts_rects[p])
        else:
            scr.blit(txt_locked1, txt_locked1_rect)
            scr.blit(txt_locked2, txt_locked2_rect)
            scr.blit(rocket_imgs_locked[rocket_idx], rocket_rects_locked[rocket_idx])
            scr.blit(lock_img, lock_rect)
        scr.blit(arrowleft_img, arrowleft_rect)
        scr.blit(arrowright_img, arrowright_rect)
        scr.blit(scr_txt1, scr_txt1_rect)
        scr.blit(scr_txt4, scr_txt4_rect)

        # Position pointer accordingly
        if choice == 3:  # Main menu
            choice_position = (int(scr_width / 4), int(scr_height / 1.35))
        if choice == 2:  # Play game
            choice_position = (int(scr_width / 4), int(scr_height / 1.5))
        if choice == 1:  # Choose rocket
            choice_position = (int(scr_width / 4), int(scr_height / 2))
        pointer_rect.center = choice_position
        scr.blit(pointer_img, pointer_rect)

        keys = pg.key.get_pressed()
        if keys[pg.K_DOWN] and choice != 3 and not pressed:
            channel_3.play(blipselect)
            choice += 1
            pressed = True
        if keys[pg.K_UP] and choice != 1 and not pressed:
            channel_3.play(blipselect)
            choice -= 1
            pressed = True
        if not keys[pg.K_DOWN] and not keys[pg.K_UP]:
            pressed = False
        if keys[pg.K_SPACE] and choice == 3 and not chosen:
            channel_3.play(blipclick)
            to_menu = True
            chosen = True
        if keys[pg.K_SPACE] and choice == 2 and not chosen and unlocked:
            channel_3.play(blipclick)
            play_game = True
            chosen = True
        if keys[pg.K_SPACE] and choice == 2 and not chosen and not unlocked:
            channel_3.play(bliplocked)
            chosen = True
        if not keys[pg.K_SPACE]:
            chosen = False

        # choose rocket
        if choice == 1 and keys[pg.K_LEFT] and rocket_idx != 0 and not pressed2:
            channel_3.play(blipselect)
            rocket_idx -= 1
            pressed2 = True
            new_choice = True
        if choice == 1 and keys[pg.K_RIGHT] and rocket_idx != (len(rocket_names) - 1) and not pressed2:
            channel_3.play(blipselect)
            rocket_idx += 1
            pressed2 = True
            new_choice = True
        if not keys[pg.K_RIGHT] and not keys[pg.K_LEFT]:
            pressed2 = False

        if play_game:
            # Screen scrolls when going to game_loop
            ax = 150 * factor
            vx = 0
            dx = 0
            t = pg.time.get_ticks() / 1000

            scr_txt6, scr_txt6_rect = makefont("MAIN MENU", 7, (0, 0), factor)
            scr_txt7, scr_txt7_rect = makefont("LAUNCH", 7, (0, 0), factor)
            scr_txt8, scr_txt8_rect = makefont(rocket_names[rocket_idx].upper(), 10, (0, 0), factor)
            scr_txt9, scr_txt9_rect = makefont("ALTITUDE", 5, (0, 0), factor)
            scr_txt10, scr_txt10_rect = makefont("0.00 KM", 5, (0, 0), factor)

            # read rocket explanations from texts
            font = pg.font.Font(main_font, factor * 5)
            f = open(get_folder_file("Text", rocket_names[rocket_idx] + ".txt"), "r")
            lines = f.readlines()
            f.close()

            heart_rects = []
            number_lives = lives[rocket_idx]

            while vx >= 0 and global_running:
                pg.event.pump()
                # Clock
                t0 = t
                t = pg.time.get_ticks() / 1000
                dt = t - t0
                if dx < scr_width / 1.99:
                    vx += ax * dt
                    dx += vx * dt
                elif vx >= 0 and dx < scr_width:
                    vx -= ax * dt
                    dx += vx * dt
                else:
                    dx = scr_width
                    vx = -5

                scr.blit(launchpad_img, launchpad_rect)
                textbox_rect.center = (int(scr_width / 2 + dx), int(scr_height * 3 / 20))
                scr.blit(textbox_img, textbox_rect)
                arrowleft_rect.center = (int(scr_width * 0.65 - scr_width / 3.5 - dx), int(scr_height / 2))
                scr.blit(arrowleft_img, arrowleft_rect)
                arrowright_rect.center = (int(scr_width * 0.65 + scr_width / 3.5 - dx), int(scr_height / 2))
                scr.blit(arrowright_img, arrowright_rect)
                pointer_rect.center = (int(scr_width / 4 + dx), int(scr_height / 1.5))
                scr.blit(pointer_img, pointer_rect)
                scr_txt6_rect.center = (int(scr_width * 0.65 + dx), int(scr_height / 1.35))
                scr.blit(scr_txt6, scr_txt6_rect)
                scr_txt7_rect.center = (int(scr_width * 0.65 + dx), int(scr_height / 1.5))
                scr.blit(scr_txt7, scr_txt7_rect)
                scr.blit(rocket_imgs[rocket_idx], rocket_rects[rocket_idx])
                scr_txt8_rect.center = (int(scr_width * 0.65 - dx), int(scr_height / 2))
                scr.blit(scr_txt8, scr_txt8_rect)
                scr_txt9_rect.center = (int((scr_width - scr_width / 15) - scr_txt9.get_size()[0] / 2),
                                        int(scr_height / 15 - scr_width + dx))
                scr.blit(scr_txt9, scr_txt9_rect)
                scr_txt10_rect.center = (int((scr_width - scr_width / 15) - scr_txt10.get_size()[0] / 2),
                                         int(scr_height / 10 - scr_width + dx))
                scr.blit(scr_txt10, scr_txt10_rect)

                # Hearts / lives
                for j in range(number_lives):
                    heart_rects.append(heart_img.get_rect())
                    heart_rects[j].center = (int((scr_width / 15) + j * heart_img.get_size()[0] * 1.5),
                                             int(scr_height / 15 - scr_width + dx))
                    scr.blit(heart_img, heart_rects[j])

                explain_txts = []
                explain_txts_rects = []
                j = 0
                for q in lines:
                    explanation = q.strip()
                    explain_txts.append(font.render(explanation.upper(), False, (255, 255, 255)))
                    explain_txts_rects.append(explain_txts[j].get_rect())
                    explain_txts_rects[j].center = (int(scr_width / 2 + dx),
                                                    int(scr_height / 10 + j * scr_height / 20))
                    j += 1
                for k in range(len(explain_txts)):
                    scr.blit(explain_txts[k], explain_txts_rects[k])

                if running and global_running:
                    pg.display.flip()
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        global_running = False
            if global_running:
                highscore, global_running, unlocked, running, chosen = \
                    game_loop(highscore, global_running, unlocked, chosen, rocket_idx, rocket_imgs, scr, scr_width,
                              scr_height, volume, factor)
            play_game = False
            arrowright_rect.center = (int(scr_width * 0.65 + scr_width / 3.5), int(scr_height / 2))
            arrowleft_rect.center = (int(scr_width * 0.65 - scr_width / 3.5), int(scr_height / 2))
            lock_rect.center = (int(scr_width / 7), int(scr_height - 34 * factor - (20 * factor)))
            textbox_rect.center = (int(scr_width / 2), int(scr_height * 3 / 20))
            new_choice = True

            pg.mixer.music.load(get_folder_file("Music", "GAME_MENU.ogg"))
            pg.mixer.music.play(-1)

        if to_menu:
            # Screen scrolls when going to game_loop
            ax = 150 * factor
            vx = 0
            dx = 0
            t = pg.time.get_ticks() / 1000

            background_img, background_rect = makeimg("main_menu.png", False, factor)

            scr_txt1, scr_txt1_rect = makefont("GOTTA CATCH E'LON", 10, (0, 0), factor)
            scr_txt2, scr_txt2_rect = makefont("PLAY GAME", 5, (0, 0), factor)
            scr_txt3, scr_txt3_rect = makefont("QUIT", 5, (0, 0), factor)
            scr_txt4, scr_txt4_rect = makefont("SETTINGS", 5, (0, 0), factor)
            scr_txt6, scr_txt6_rect = makefont("MAIN MENU", 7, (0, 0), factor)
            scr_txt7, scr_txt7_rect = makefont("LAUNCH", 7, (0, 0), factor)
            scr_txt8, scr_txt8_rect = makefont(rocket_names[rocket_idx].upper(), 10, (0, 0), factor)
            txt_controls, txt_controls_rect = makefont("CONTROLS", 5, (int(scr_width / 2), int(scr_height * 0.6)),
                                                       factor)
            txt_score1, txt_score1_rect = makefont("HIGHSCORE", 5, (0, 0), factor)
            txt_score2, txt_score2_rect = makefont(f"{highscore:,.2f} KM", 5, (0, 0), factor)
            txt_credits, txt_credits_rect = makefont("CREDITS", 5, (0, 0), factor)

            pointer_rect2 = pointer_img.get_rect()

            # read rocket explanations from texts
            font = pg.font.Font(main_font, factor * 5)
            f = open(get_folder_file("Text", rocket_names[rocket_idx] + ".txt"), "r")
            lines = f.readlines()
            f.close()

            while vx >= 0 and global_running and running:
                pg.event.pump()
                # Clock
                t0 = t
                t = pg.time.get_ticks() / 1000
                dt = t - t0
                if dx < scr_width / 1.99:
                    vx += ax * dt
                    dx += vx * dt
                elif vx >= 0 and dx < scr_width:
                    vx -= ax * dt
                    dx += vx * dt
                else:
                    dx = scr_width
                    vx = -5

                background_rect.center = (int(dx), int(scr_height / 2))
                scr.blit(background_img, background_rect)
                textbox_rect.center = (int(scr_width / 2 + dx), int(scr_height * 3 / 20))
                scr.blit(textbox_img, textbox_rect)
                scr_txt1_rect.center = (int(- scr_width / 2 + dx), int(scr_height * 0.3))
                scr.blit(scr_txt1, scr_txt1_rect)
                scr_txt2_rect.center = (int(- scr_width / 2 + dx), int(scr_height * 0.5))
                scr.blit(scr_txt2, scr_txt2_rect)
                scr_txt3_rect.center = (int(- scr_width / 2 + dx), int(scr_height * 0.7))
                scr.blit(scr_txt3, scr_txt3_rect)
                scr_txt4_rect.center = (int(- scr_width / 2 + dx), int(scr_height * 0.55))
                scr.blit(scr_txt4, scr_txt4_rect)
                pointer_rect.center = (int(scr_width / 3 - scr_width + dx), int(scr_height * 0.5))
                scr.blit(pointer_img, pointer_rect)
                arrowleft_rect.center = (int(scr_width * 0.65 - scr_width / 3.5 + dx), int(scr_height / 2))
                scr.blit(arrowleft_img, arrowleft_rect)
                arrowright_rect.center = (int(scr_width * 0.65 + scr_width / 3.5 + dx), int(scr_height / 2))
                scr.blit(arrowright_img, arrowright_rect)
                pointer_rect2.center = (int(scr_width / 4 + dx), int(scr_height / 1.35))
                scr.blit(pointer_img, pointer_rect2)
                scr_txt6_rect.center = (int(scr_width * 0.65 + dx), int(scr_height / 1.35))
                scr.blit(scr_txt6, scr_txt6_rect)
                scr_txt7_rect.center = (int(scr_width * 0.65 + dx), int(scr_height / 1.5))
                scr.blit(scr_txt7, scr_txt7_rect)
                txt_controls_rect.center = (int(- scr_width / 2 + dx), int(scr_height * 0.6))
                scr.blit(txt_controls, txt_controls_rect)
                txt_credits_rect.center = (int(- scr_width / 2 + dx), int(scr_height * 0.65))
                scr.blit(txt_credits, txt_credits_rect)

                if unlocked:
                    rocket_rects[rocket_idx].center = (int(x_rocket + dx), y_rocket)
                    scr.blit(rocket_imgs[rocket_idx], rocket_rects[rocket_idx])
                    scr_txt8_rect.center = (int(scr_width * 0.65 + dx), int(scr_height / 2))
                    scr.blit(scr_txt8, scr_txt8_rect)

                    explain_txts = []
                    explain_txts_rects = []
                    j = 0
                    for q in lines:
                        explanation = q.strip()
                        explain_txts.append(font.render(explanation.upper(), False, (255, 255, 255)))
                        explain_txts_rects.append(explain_txts[j].get_rect())
                        explain_txts_rects[j].center = (int(scr_width / 2 + dx),
                                                        int(scr_height / 10 + j * scr_height / 20))
                        j += 1
                    for k in range(len(explain_txts)):
                        scr.blit(explain_txts[k], explain_txts_rects[k])

                else:
                    rocket_rects_locked[rocket_idx].center = (int(x_rocket + dx), y_rocket)
                    scr.blit(rocket_imgs_locked[rocket_idx], rocket_rects_locked[rocket_idx])
                    lock_rect.center = (int(scr_width / 7 + dx),
                                        int(scr_height - 34 * factor - (20 * factor)))
                    scr.blit(lock_img, lock_rect)
                    txt_locked1_rect.center = (int(scr_width * 0.65 + dx), int(scr_height / 2))
                    scr.blit(txt_locked1, txt_locked1_rect)
                    txt_locked2_rect.center = (int(scr_width / 2 + dx), int(scr_height / 10 + scr_height / 20))
                    scr.blit(txt_locked2, txt_locked2_rect)
                txt_score1_rect.center = (int((-14 * scr_width / 15) + txt_score1.get_size()[0] / 2 + dx),
                                          int(scr_height / 15))
                txt_score2_rect.center = (int((-14 * scr_width / 15) + txt_score2.get_size()[0] / 2 + dx),
                                          int(scr_height / 10))
                scr.blit(txt_score1, txt_score1_rect)
                scr.blit(txt_score2, txt_score2_rect)

                if running and global_running:
                    pg.display.flip()
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        global_running = False
            running = False

        if running and global_running:
            pg.display.flip()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                global_running = False
    return highscore, unlocked, global_running, chosen, rocket_idx, rocket_rects_locked, rocket_imgs_locked, \
        rocket_imgs, rocket_rects
