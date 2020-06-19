import pygame as pg
from game_tools import get_folder_file, makefont, makeimg
from game_constants import channel_3, blipselect, blipclick, rocket_names, milestones, main_font
from other_menus import credits_menu, controls_menu
from settings_menu import settings_menu
from rocket_menu import rocket_menu


def main_menu(highscore, global_running, chosen, rocket_rects_locked, rocket_imgs_locked, rocket_imgs, rocket_rects,
              scr, scr_width, scr_height, volume, factor):
    running = True
    play_game = False
    settings = False
    load_images = False
    controls = False
    credit_scr = False
    unlocked = True
    pressed = False
    rocket_idx = 0

    # image and text info. Also place here to avoid referencing before assignment
    background_img, background_rect = makeimg("main_menu.png", False, factor)
    pointer_img, pointer_rect = makeimg("pointer.png", True, factor)
    scr_txt1, scr_txt1_rect = makefont("GOTTA CATCH E'LON", 10, (int(scr_width / 2), int(scr_height * 0.3)),
                                       factor)
    txt_score1, txt_score1_rect = makefont("HIGHSCORE", 5, (0, 0), factor)
    txt_score2, txt_score2_rect = makefont(f"{highscore:,.2f} KM", 5, (0, 0), factor)
    scr_txt2, scr_txt2_rect = makefont("PLAY GAME", 5, (int(scr_width / 2), int(scr_height * 0.5)), factor)
    scr_txt3, scr_txt3_rect = makefont("QUIT", 5, (int(scr_width / 2), int(scr_height * 0.7)), factor)
    scr_txt4, scr_txt4_rect = makefont("SETTINGS", 5, (int(scr_width / 2), int(scr_height * 0.55)), factor)
    scr_txt5, scr_txt5_rect = makefont("SPLASHTEST", 5, (int(scr_width * 3 / 4), int(scr_height * 0.35)), factor)
    txt_controls, txt_controls_rect = makefont("CONTROLS", 5, (int(scr_width / 2), int(scr_height * 0.6)),
                                               factor)
    txt_credits, txt_credits_rect = makefont("CREDITS", 5, (int(scr_width / 2), int(scr_height * 0.65)), factor)

    # Pointer conditions
    choice = 1
    choice_position = int(scr_height * 0.5)
    while running and global_running:
        if load_images:  # if the screen size is changed the images need to be loaded again to get the right size
            background_img, background_rect = makeimg("main_menu.png", False, factor)
            pointer_img, pointer_rect = makeimg("pointer.png", True, factor)
            scr_txt1, scr_txt1_rect = makefont("GOTTA CATCH E'LON", 10, (int(scr_width / 2), int(scr_height * 0.3)),
                                               factor)
            txt_score1, txt_score1_rect = makefont("HIGHSCORE", 5, (0, 0), factor)
            txt_score2, txt_score2_rect = makefont(f"{highscore:,.2f} KM", 5, (0, 0), factor)
            scr_txt2, scr_txt2_rect = makefont("PLAY GAME", 5, (int(scr_width / 2), int(scr_height * 0.5)), factor)
            scr_txt3, scr_txt3_rect = makefont("QUIT", 5, (int(scr_width / 2), int(scr_height * 0.7)), factor)
            scr_txt4, scr_txt4_rect = makefont("SETTINGS", 5, (int(scr_width / 2), int(scr_height * 0.55)), factor)
            scr_txt5, scr_txt5_rect = makefont("SPLASHTEST", 5, (int(scr_width * 3 / 4), int(scr_height * 0.35)), factor)
            txt_controls, txt_controls_rect = makefont("CONTROLS", 5, (int(scr_width / 2), int(scr_height * 0.6)),
                                                       factor)
            txt_credits, txt_credits_rect = makefont("CREDITS", 5, (int(scr_width / 2), int(scr_height * 0.65)), factor)

            load_images = False

        pg.event.pump()

        # Re-orient positions if the game loop has been started before
        background_rect.center = (scr_width, int(scr_height / 2))
        scr.blit(background_img, background_rect)
        scr.blit(scr_txt1, scr_txt1_rect)
        txt_score1_rect.center = (int((scr_width / 15) + txt_score1.get_size()[0] / 2), int(scr_height / 15))
        txt_score2_rect.center = (int((scr_width / 15) + txt_score2.get_size()[0] / 2), int(scr_height / 10))
        scr.blit(txt_score1, txt_score1_rect)
        scr.blit(txt_score2, txt_score2_rect)
        scr.blit(scr_txt2, scr_txt2_rect)
        scr.blit(scr_txt3, scr_txt3_rect)
        scr.blit(scr_txt4, scr_txt4_rect)
        scr.blit(scr_txt5, scr_txt5_rect)
        scr.blit(txt_controls, txt_controls_rect)
        scr.blit(txt_credits, txt_credits_rect)

        # Position pointer accordingly
        if choice == 1:    # Play game
            choice_position = int(scr_height * 0.5)
        if choice == 2:    # Choose settings
            choice_position = int(scr_height * 0.55)
        if choice == 3:    # Controls
            choice_position = int(scr_height * 0.6)
        if choice == 4:    # Credits
            choice_position = int(scr_height * 0.65)
        if choice == 5:    # Quit
            choice_position = int(scr_height * 0.7)
        pointer_rect.center = (int(scr_width / 3), choice_position)
        scr.blit(pointer_img, pointer_rect)

        keys = pg.key.get_pressed()
        if keys[pg.K_DOWN] and choice != 5 and not pressed:
            channel_3.play(blipselect)
            choice += 1
            pressed = True
        if keys[pg.K_UP] and choice != 1 and not pressed:
            channel_3.play(blipselect)
            choice -= 1
            pressed = True
        if not keys[pg.K_DOWN] and not keys[pg.K_UP]:
            pressed = False
        if keys[pg.K_SPACE] and not chosen:
            channel_3.play(blipclick)
            if choice == 1:
                play_game = True
            if choice == 2:
                settings = True
            if choice == 3:
                controls = True
            if choice == 4:
                credit_scr = True
            if choice == 5:
                global_running = False
            chosen = True
        if not keys[pg.K_SPACE]:
            chosen = False

        for event in pg.event.get():
            if event.type == pg.QUIT:
                global_running = False

        if running and global_running:
            pg.display.flip()

        if play_game:
            # Screen scrolls when going to rocket_menu
            ax = 150 * factor
            vx = 0
            dx = 0
            t = pg.time.get_ticks() / 1000

            arrowright_img, arrowright_rect = makeimg("pointer.png", True, factor)
            arrowleft_img = pg.transform.flip(arrowright_img, True, False)
            arrowleft_rect = arrowleft_img.get_rect()
            pointer_rect2 = pointer_img.get_rect()
            lock_img, lock_rect = makeimg("lock.png", True, factor)
            textbox_img, textbox_rect = makeimg("descriptiontextbox.png", True, factor)

            scr_txt6, scr_txt6_rect = makefont("MAIN MENU", 7, (0, 0), factor)
            scr_txt7, scr_txt7_rect = makefont("LAUNCH", 7, (0, 0), factor)
            scr_txt8, scr_txt8_rect = makefont(rocket_names[rocket_idx].upper(), 10, (0, 0), factor)
            txt_locked1, txt_locked1_rect = makefont("LOCKED", 10, (0, 0), factor)
            txt_locked2, txt_locked2_rect = makefont(f"REACH {milestones[rocket_idx]:,.2f} KM TO UNLOCK.", 5, (0, 0),
                                                     factor)

            x_rocket = int(scr_width / 7)
            y_rocket = int(scr_height - 32 * factor - (rocket_imgs[rocket_idx].get_size()[1] / 2))

            # read rocket explanations from texts
            font = pg.font.Font(main_font, factor * 5)
            f = open(get_folder_file("Text", rocket_names[rocket_idx] + ".txt"), "r")
            lines = f.readlines()
            f.close()

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
                background_rect.center = (int(scr_width - dx), int(scr_height / 2))
                scr.blit(background_img, background_rect)
                textbox_rect.center = (int(scr_width * 3 / 2 - dx), int(scr_height * 3 / 20))
                scr.blit(textbox_img, textbox_rect)
                scr_txt1_rect.center = (int(scr_width / 2 - dx), int(scr_height * 0.3))
                scr.blit(scr_txt1, scr_txt1_rect)
                scr_txt2_rect.center = (int(scr_width / 2 - dx), int(scr_height * 0.5))
                scr.blit(scr_txt2, scr_txt2_rect)
                scr_txt3_rect.center = (int(scr_width / 2 - dx), int(scr_height * 0.7))
                scr.blit(scr_txt3, scr_txt3_rect)
                scr_txt4_rect.center = (int(scr_width / 2 - dx), int(scr_height * 0.55))
                scr.blit(scr_txt4, scr_txt4_rect)
                pointer_rect.center = (int(scr_width / 3 - dx), choice_position)
                scr.blit(pointer_img, pointer_rect)
                arrowleft_rect.center = (int(scr_width * 1.65 - scr_width / 3.5 - dx), int(scr_height / 2))
                scr.blit(arrowleft_img, arrowleft_rect)
                arrowright_rect.center = (int(scr_width * 1.65 + scr_width / 3.5 - dx), int(scr_height / 2))
                scr.blit(arrowright_img, arrowright_rect)
                pointer_rect2.center = (int(scr_width / 4 + scr_width - dx), int(scr_height / 2))
                scr.blit(pointer_img, pointer_rect2)
                scr_txt6_rect.center = (int(scr_width * 0.65 + scr_width - dx), int(scr_height / 1.35))
                scr.blit(scr_txt6, scr_txt6_rect)
                scr_txt7_rect.center = (int(scr_width * 0.65 + scr_width - dx), int(scr_height / 1.5))
                scr.blit(scr_txt7, scr_txt7_rect)
                txt_controls_rect.center = (int(scr_width / 2 - dx), int(scr_height * 0.6))
                scr.blit(txt_controls, txt_controls_rect)
                txt_credits_rect.center = (int(scr_width / 2 - dx), int(scr_height * 0.65))
                scr.blit(txt_credits, txt_credits_rect)

                if unlocked:
                    rocket_rects[rocket_idx].center = (int(x_rocket + scr_width - dx), y_rocket)
                    scr.blit(rocket_imgs[rocket_idx], rocket_rects[rocket_idx])
                    scr_txt8_rect.center = (int(scr_width * 0.65 + scr_width - dx), int(scr_height / 2))
                    scr.blit(scr_txt8, scr_txt8_rect)

                    explain_txts = []
                    explain_txts_rects = []
                    j = 0
                    for q in lines:
                        explanation = q.strip()
                        explain_txts.append(font.render(explanation.upper(), False, (255, 255, 255)))
                        explain_txts_rects.append(explain_txts[j].get_rect())
                        explain_txts_rects[j].center = (int(scr_width / 2 + scr_width - dx),
                                                        int(scr_height / 10 + j * scr_height / 20))
                        j += 1
                    for k in range(len(explain_txts)):
                        scr.blit(explain_txts[k], explain_txts_rects[k])
                else:
                    rocket_rects_locked[rocket_idx].center = (int(scr_width + x_rocket - dx), y_rocket)
                    scr.blit(rocket_imgs_locked[rocket_idx], rocket_rects_locked[rocket_idx])
                    lock_rect.center = (int(scr_width + scr_width / 7 - dx),
                                        int(scr_height - 34 * factor - (20 * factor)))
                    scr.blit(lock_img, lock_rect)
                    txt_locked1_rect.center = (int(scr_width * 1.65 - dx), int(scr_height / 2))
                    scr.blit(txt_locked1, txt_locked1_rect)
                    txt_locked2_rect.center = (int(3 * scr_width / 2 - dx), int(scr_height / 10 + scr_height / 20))
                    scr.blit(txt_locked2, txt_locked2_rect)
                txt_score1_rect.center = (int((scr_width / 15) + txt_score1.get_size()[0] / 2 - dx),
                                          int(scr_height / 15))
                txt_score2_rect.center = (int((scr_width / 15) + txt_score2.get_size()[0] / 2 - dx),
                                          int(scr_height / 10))
                scr.blit(txt_score1, txt_score1_rect)
                scr.blit(txt_score2, txt_score2_rect)

                if running and global_running:
                    pg.display.flip()
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        global_running = False
            if global_running:
                highscore, unlocked, global_running, chosen, rocket_idx, rocket_rects_locked, rocket_imgs_locked, \
                    rocket_imgs, rocket_rects = rocket_menu(highscore, unlocked, global_running, chosen, rocket_idx,
                                                            rocket_rects_locked, rocket_imgs_locked, rocket_imgs,
                                                            rocket_rects, scr, scr_width, scr_height, volume, factor)
                play_game = False
            load_images = True

        if settings:
            highscore, unlocked, global_running, chosen, rocket_rects_locked, rocket_imgs_locked, rocket_imgs, \
                rocket_rects, scr, scr_width, scr_height, volume, factor = \
                settings_menu(highscore, unlocked, global_running, chosen, rocket_idx, rocket_rects_locked,
                              rocket_imgs_locked, rocket_imgs, rocket_rects, scr, scr_width, scr_height, volume, factor)
            settings = False
            load_images = True

        if controls:
            global_running, chosen = controls_menu(global_running, chosen, scr, scr_width, scr_height, factor)
            controls = False
            load_images = True

        if credit_scr:
            global_running, chosen = credits_menu(global_running, chosen, scr, scr_width, scr_height, factor)
            credit_scr = False
            load_images = True
