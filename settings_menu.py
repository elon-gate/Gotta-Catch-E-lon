import pygame as pg
from game_tools import get_folder_file, makefont, makeimg
from game_constants import channel_1, channel_2, channel_3, blipselect, blipclick, bliplocked, rocket_names, \
    milestones, main_font, original_width, original_height


def settings_menu(highscore, unlocked, global_running, chosen, rocket_idx, rocket_rects_locked, rocket_imgs_locked,
                  rocket_imgs, rocket_rects, scr, scr_width, scr_height, volume, factor):
    running = True
    load_images = False
    reset_scr = False
    pressed = False
    pressed2 = False
    choice = 1
    choice_position = int(scr_height * 0.5)
    reset_choice = 2

    # also load images here to avoid referencing before assignment
    background_img, background_rect = makeimg("main_menu.png", False, factor)
    background_rect.center = (int(scr_width), int(scr_height / 2))
    pointer_img, pointer_rect = makeimg("pointer.png", True, factor)
    arrowright_img, arrowright_rect = makeimg("pointer.png", True, factor)
    arrowright2_rect = arrowright_img.get_rect()
    arrowright_rect.center = (int(scr_width / 2 + 100 * factor), int(scr_height * 0.5))
    arrowright2_rect.center = (int(scr_width / 2 + 100 * factor), int(scr_height * 0.6))
    arrowleft_img = pg.transform.flip(arrowright_img, True, False)
    arrowleft_rect = arrowleft_img.get_rect()
    arrowleft2_rect = arrowleft_img.get_rect()
    arrowleft_rect.center = (int(scr_width / 2), int(scr_height * 0.5))
    arrowleft2_rect.center = (int(scr_width / 2), int(scr_height * 0.6))
    scr_txt1, scr_txt1_rect = makefont("SETTINGS", 10, (int(scr_width / 2), int(scr_height * 0.3)), factor)
    scr_txt2, scr_txt2_rect = makefont("RESOLUTION", 5, (int(scr_width / 3), int(scr_height * 0.5)), factor)
    scr_txt3, scr_txt3_rect = makefont("MAIN MENU", 5, (int(scr_width / 3), int(scr_height * 0.8)), factor)
    scr_txt5, scr_txt5_rect = makefont("AUDIO VOLUME", 5, (int(scr_width / 3), int(scr_height * 0.6)), factor)
    scr_txt4, scr_txt4_rect = makefont("RESET PROGRESS", 5, (int(scr_width / 3), int(scr_height * 0.7)), factor)

    font = pg.font.Font(main_font, factor * 5)

    reso_lst = []
    for q in range(1, 7):
        reso_lst.append(font.render(str(original_width * q) + " X " + str(original_height * q),
                                    False, (255, 255, 255)))
    reso1_rect = reso_lst[0].get_rect()
    reso1_rect.center = (int(scr_width / 2 + 50 * factor), int(scr_height * 0.5))

    vol_lst = []
    for j in range(0, 11):
        vol_lst.append(font.render(str(j * 10) + " %", False, (255, 255, 255)))
    vol1_rect = vol_lst[0].get_rect()
    vol1_rect.center = (int(scr_width / 2 + 50 * factor), int(scr_height * 0.6))

    while running and global_running:
        pg.event.pump()
        if load_images:  # reload images if screen size is changed
            scr_width = original_width * factor
            scr_height = original_height * factor
            reso = (scr_width, scr_height)
            scr = pg.display.set_mode(reso)

            background_img, background_rect = makeimg("main_menu.png", False, factor)
            background_rect.center = (int(scr_width), int(scr_height / 2))
            pointer_img, pointer_rect = makeimg("pointer.png", True, factor)
            arrowright_img, arrowright_rect = makeimg("pointer.png", True, factor)
            arrowright2_rect = arrowright_img.get_rect()
            arrowright_rect.center = (int(scr_width / 2 + 100 * factor), int(scr_height * 0.5))
            arrowright2_rect.center = (int(scr_width / 2 + 100 * factor), int(scr_height * 0.6))
            arrowleft_img = pg.transform.flip(arrowright_img, True, False)
            arrowleft_rect = arrowleft_img.get_rect()
            arrowleft2_rect = arrowleft_img.get_rect()
            arrowleft_rect.center = (int(scr_width / 2), int(scr_height * 0.5))
            arrowleft2_rect.center = (int(scr_width / 2), int(scr_height * 0.6))
            scr_txt1, scr_txt1_rect = makefont("SETTINGS", 10, (int(scr_width / 2), int(scr_height * 0.3)), factor)
            scr_txt2, scr_txt2_rect = makefont("RESOLUTION", 5, (int(scr_width / 3), int(scr_height * 0.5)), factor)
            scr_txt3, scr_txt3_rect = makefont("MAIN MENU", 5, (int(scr_width / 3), int(scr_height * 0.8)), factor)
            scr_txt5, scr_txt5_rect = makefont("AUDIO VOLUME", 5, (int(scr_width / 3), int(scr_height * 0.6)), factor)
            scr_txt4, scr_txt4_rect = makefont("RESET PROGRESS", 5, (int(scr_width / 3), int(scr_height * 0.7)), factor)

            font = pg.font.Font(main_font, factor * 5)

            reso_lst = []
            for q in range(1, 7):
                reso_lst.append(font.render(str(original_width * q) + " X " + str(original_height * q),
                                            False, (255, 255, 255)))
            reso1_rect = reso_lst[0].get_rect()
            reso1_rect.center = (int(scr_width / 2 + 50 * factor), int(scr_height * 0.5))

            vol_lst = []
            for j in range(0, 11):
                vol_lst.append(font.render(str(j * 10) + " %", False, (255, 255, 255)))
            vol1_rect = vol_lst[0].get_rect()
            vol1_rect.center = (int(scr_width / 2 + 50 * factor), int(scr_height * 0.6))

            rocket_imgs = []
            rocket_rects = []
            rocket_imgs_locked = []
            rocket_rects_locked = []
            for q in range(len(rocket_names)):
                temp_rocketimg, temp_rocketrect = makeimg(rocket_names[q] + ".png", True, factor)
                rocket_imgs.append(temp_rocketimg)
                rocket_rects.append(temp_rocketrect)
                temp_rocketlocked, temp_rocket_rectlocked = makeimg(rocket_names[q] + "locked.png", True, factor)
                rocket_imgs_locked.append(temp_rocketlocked)
                rocket_rects_locked.append(temp_rocket_rectlocked)

            load_images = False

        if reset_scr:
            # Let the pointer start at 'no' for safety reasons
            question_img, question_rect = makefont("ARE YOU SURE YOU WANT TO RESET YOUR PROGRESS?", 6,
                                                   (int(scr_width / 2), int(scr_height * 0.4)), factor)
            yes_img, yes_rect = makefont("YES", 5, (int(scr_width / 2), int(scr_height * 0.5)), factor)
            no_img, no_rect = makefont("NO", 5, (int(scr_width / 2), int(scr_height * 0.55)), factor)

            scr.blit(background_img, background_rect)
            scr.blit(question_img, question_rect)
            scr.blit(yes_img, yes_rect)
            scr.blit(no_img, no_rect)

            if reset_choice == 1:  # Yes
                choice_position = int(scr_height * 0.5)
            if reset_choice == 2:  # No
                choice_position = int(scr_height * 0.55)
            pointer_rect.center = (int(scr_width / 6), choice_position)
            scr.blit(pointer_img, pointer_rect)

            keys = pg.key.get_pressed()
            if keys[pg.K_DOWN] and reset_choice != 2 and not pressed:
                channel_3.play(blipselect)
                reset_choice += 1
                pressed = True
            if keys[pg.K_UP] and reset_choice != 1 and not pressed:
                channel_3.play(blipselect)
                reset_choice -= 1
                pressed = True
            if not keys[pg.K_DOWN] and not keys[pg.K_UP]:
                pressed = False
            if keys[pg.K_SPACE] and reset_choice == 1 and not chosen:
                channel_3.play(blipclick)
                reset_scr = False
                txt = open(get_folder_file("Text", "highscore.txt"), "w")
                txt.write("0")
                txt.close()
                highscore = 0
                if highscore >= milestones[rocket_idx]:
                    unlocked = True
                else:
                    unlocked = False
                chosen = True
                reset_choice = 2
            if keys[pg.K_SPACE] and reset_choice == 2 and not chosen:
                channel_3.play(blipclick)
                reset_scr = False
                chosen = True
            if not keys[pg.K_SPACE]:
                chosen = False

        else:
            scr.blit(background_img, background_rect)
            scr.blit(scr_txt1, scr_txt1_rect)
            scr.blit(scr_txt2, scr_txt2_rect)
            scr.blit(scr_txt3, scr_txt3_rect)
            scr.blit(scr_txt4, scr_txt4_rect)
            scr.blit(arrowleft_img, arrowleft_rect)
            scr.blit(arrowright_img, arrowright_rect)
            scr.blit(reso_lst[factor - 1], reso1_rect)
            scr.blit(arrowleft_img, arrowleft2_rect)
            scr.blit(arrowright_img, arrowright2_rect)
            scr.blit(vol_lst[round(volume / 10)], vol1_rect)
            scr.blit(scr_txt5, scr_txt5_rect)

            # Position pointer accordingly
            if choice == 1:  # Resolution
                choice_position = int(scr_height * 0.5)
            if choice == 2:  # Volume
                choice_position = int(scr_height * 0.6)
            if choice == 3:  # Main menu
                choice_position = int(scr_height * 0.7)
            if choice == 4:  # Reset highscore
                choice_position = int(scr_height * 0.8)
            pointer_rect.center = (int(scr_width / 6), choice_position)
            scr.blit(pointer_img, pointer_rect)

            keys = pg.key.get_pressed()
            if keys[pg.K_DOWN] and choice != 4 and not pressed:
                channel_3.play(blipselect)
                choice += 1
                pressed = True
            if keys[pg.K_UP] and choice != 1 and not pressed:
                channel_3.play(blipselect)
                choice -= 1
                pressed = True
            if not keys[pg.K_DOWN] and not keys[pg.K_UP]:
                pressed = False
            if keys[pg.K_SPACE] and choice == 4 and not chosen:
                channel_3.play(blipclick)
                running = False
                chosen = True
            if keys[pg.K_SPACE] and choice == 3 and not chosen:
                channel_3.play(blipclick)
                reset_scr = True
                chosen = True
            if not keys[pg.K_SPACE]:
                chosen = False

            if choice == 1 and keys[pg.K_LEFT] and not pressed2:   # resolution
                if factor == 1:
                    channel_3.play(bliplocked)
                else:
                    channel_3.play(blipselect)
                    factor -= 1
                    load_images = True
                pressed2 = True
            if choice == 1 and keys[pg.K_RIGHT] and not pressed2:   # resolution
                if factor == 6:
                    channel_3.play(bliplocked)
                else:
                    channel_3.play(blipselect)
                    factor += 1
                    load_images = True
                pressed2 = True
            if choice == 2 and keys[pg.K_LEFT] and not pressed2:   # volume
                if volume == 0:
                    channel_3.play(bliplocked)
                else:
                    channel_3.play(blipselect)
                    volume -= 10
                pressed2 = True
            if choice == 2 and keys[pg.K_RIGHT] and not pressed2:   # volume
                if volume == 100:
                    channel_3.play(bliplocked)
                else:
                    channel_3.play(blipselect)
                    volume += 10
                pressed2 = True
            if not keys[pg.K_RIGHT] and not keys[pg.K_LEFT]:
                pressed2 = False

        if running and global_running:
            pg.display.flip()
        pg.mixer.music.set_volume(volume / 100)
        channel_3.set_volume(volume / 100)
        channel_2.set_volume(volume / 100)
        channel_1.set_volume(volume / 100)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                global_running = False
    return highscore, unlocked, global_running, chosen, rocket_rects_locked, rocket_imgs_locked, rocket_imgs, \
        rocket_rects, scr, scr_width, scr_height, volume, factor
