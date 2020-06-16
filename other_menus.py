import pygame as pg
from game_tools import get_folder_file, resize, animate, makefont, makeimg, text_animation
from game_constants import channel_2, channel_3, blipclick, txt_sound, storytxt1, storytxt2


def controls_menu(global_running, chosen, scr, scr_width, scr_height, factor):
    running = True

    background_img, background_rect = makeimg("main_menu.png", False, factor)
    background_rect.center = (int(scr_width), int(scr_height / 2))
    pointer_img, pointer_rect = makeimg("pointer.png", True, factor)
    pointer_rect.center = (int(scr_width / 3), int(scr_height * 5 / 6))
    arrowkeys_img, arrowkeys_rect = makeimg("arrowkeys.png", True, factor)
    arrowkeys_rect.center = (int(scr_width * 15 / 20), int(scr_height * 1 / 4))
    spacebar_img, spacebar_rect = makeimg("spacebar.png", True, factor)
    spacebar_rect.center = (int(scr_width * 15 / 20), int(scr_height * 18.5 / 32))

    txt_mainmenu, txt_mainmenu_rect = makefont("MAIN MENU", 7, (int(scr_width / 2), int(scr_height * 5 / 6)), factor)
    txt_arrowkeys, txt_arrowkeys_rect = makefont("ARROW KEYS", 9, (int(scr_width / 4), int(scr_height * 3 / 16)),
                                                 factor)
    txt_expl_arrowkeys1, txt_expl_arrowkeys1_rect = makefont("NAVIGATE THROUGH MENU", 5,
                                                             (int(scr_width / 4), int(scr_height * 8.5 / 32)), factor)
    txt_expl_arrowkeys2, txt_expl_arrowkeys2_rect = makefont("STEER ROCKET", 5,
                                                             (int(scr_width / 4), int(scr_height * 5 / 16)), factor)
    txt_spacebar, txt_spacebar_rect = makefont("SPACE BAR", 9, (int(scr_width / 4), int(scr_height * 1 / 2)), factor)
    txt_expl_spacebar1, txt_expl_spacebar1_rect = makefont("SELECT", 5,
                                                           (int(scr_width / 4), int(scr_height * 18.5 / 32)), factor)
    txt_expl_spacebar2, txt_expl_spacebar2_rect = makefont("PAUSE GAME", 5,
                                                           (int(scr_width / 4), int(scr_height * 10 / 16)), factor)
    txt_expl_spacebar3, txt_expl_spacebar3_rect = makefont("SKIP STORY", 5,
                                                           (int(scr_width / 4), int(scr_height * 43 / 64)), factor)

    while running and global_running:
        pg.event.pump()

        scr.blit(background_img, background_rect)
        scr.blit(pointer_img, pointer_rect)
        scr.blit(txt_mainmenu, txt_mainmenu_rect)
        scr.blit(arrowkeys_img, arrowkeys_rect)
        scr.blit(spacebar_img, spacebar_rect)
        scr.blit(txt_arrowkeys, txt_arrowkeys_rect)
        scr.blit(txt_spacebar, txt_spacebar_rect)
        scr.blit(txt_expl_arrowkeys1, txt_expl_arrowkeys1_rect)
        scr.blit(txt_expl_arrowkeys2, txt_expl_arrowkeys2_rect)
        scr.blit(txt_expl_spacebar1, txt_expl_spacebar1_rect)
        scr.blit(txt_expl_spacebar2, txt_expl_spacebar2_rect)
        scr.blit(txt_expl_spacebar3, txt_expl_spacebar3_rect)

        pg.display.flip()

        keys = pg.key.get_pressed()
        if keys[pg.K_SPACE] and not chosen:
            channel_3.play(blipclick)
            running = False
            chosen = True
        if not keys[pg.K_SPACE]:
            chosen = False

        for event in pg.event.get():
            if event.type == pg.QUIT:
                global_running = False
    return global_running, chosen


def credits_menu(global_running, chosen, scr, scr_width, scr_height, factor):
    running = True

    txt1, txt1rect = makefont("GOTTA CATCH E'LON", 12, (int(scr_width / 2), int(scr_height * 1.25 / 10)), factor)
    txt2, txt2rect = makefont("PRODUCTION CREW", 7, (int(scr_width / 2), int(scr_height * 2.5 / 10)), factor)
    txt2_2, txt2_2rect = makefont("CARLOS CASTRO GARCIA", 4, (int(scr_width / 2), int(scr_height * 3.1 / 10)), factor)
    txt2_3, txt2_3rect = makefont("FRANK MEIJERING", 4, (int(scr_width / 2), int(scr_height * 3.4 / 10)), factor)
    txt3, txt3rect = makefont("PROGRAMMING DIRECTOR", 7, (int(scr_width / 2), int(scr_height * 4.2 / 10)), factor)
    txt3_2, txt3_2rect = makefont("FRANK MEIJERING", 4, (int(scr_width / 2), int(scr_height * 4.8 / 10)), factor)
    txt4, txt4rect = makefont("VISUAL ARTS DIRECTOR", 7, (int(scr_width / 2), int(scr_height * 5.6 / 10)), factor)
    txt4_2, txt4_2rect = makefont("CARLOS CASTRO GARCIA", 4, (int(scr_width / 2), int(scr_height * 6.2 / 10)), factor)
    txt5, txt5rect = makefont("MUSIC COMPOSER AND SOUND DESIGNER", 7, (int(scr_width / 2), int(scr_height * 7 / 10)),
                              factor)
    txt5_2, txt5_2rect = makefont("FRANK MEIJERING", 4, (int(scr_width / 2), int(scr_height * 7.6 / 10)), factor)
    txt6, txt6rect = makefont("STORYBOARD AND GAME FLOW COORDINATOR", 7,
                              (int(scr_width / 2), int(scr_height * 8.4 / 10)), factor)
    txt6_2, txt6_2rect = makefont("CARLOS CASTRO GARCIA", 4, (int(scr_width / 2), int(scr_height * 9 / 10)), factor)

    while running and global_running:
        pg.event.pump()

        scr.fill((0, 0, 0))
        scr.blit(txt1, txt1rect)
        scr.blit(txt2, txt2rect)
        scr.blit(txt2_2, txt2_2rect)
        scr.blit(txt2_3, txt2_3rect)
        scr.blit(txt3, txt3rect)
        scr.blit(txt4, txt4rect)
        scr.blit(txt3_2, txt3_2rect)
        scr.blit(txt4_2, txt4_2rect)
        scr.blit(txt5, txt5rect)
        scr.blit(txt5_2, txt5_2rect)
        scr.blit(txt6, txt6rect)
        scr.blit(txt6_2, txt6_2rect)

        pg.display.flip()

        keys = pg.key.get_pressed()
        if keys[pg.K_SPACE] and not chosen:
            channel_3.play(blipclick)
            running = False
            chosen = True
        if not keys[pg.K_SPACE]:
            chosen = False

        for event in pg.event.get():
            if event.type == pg.QUIT:
                global_running = False
    return global_running, chosen


def intro_story(scr, scr_width, scr_height, volume, factor):
    running = True
    global_running = True
    chosen = False

    pg.mixer.music.load(get_folder_file("Music", "GAME_MENU.ogg"))
    pg.mixer.music.set_volume(volume / 100)
    pg.mixer.music.play(-1)

    channel_2.set_volume(volume * 0.4 / 100)

    lsttxt1_img = list(storytxt1)
    fonttxts1 = []
    fontrects1 = []
    for y in range(len(lsttxt1_img)):
        fonttxt, fontrect = makefont(lsttxt1_img[y], 5, (0, 0), factor)
        fonttxts1.append(fonttxt)
        fontrects1.append(fontrect)

    lsttxt2_img = list(storytxt2)
    fonttxts2 = []
    fontrects2 = []
    for y in range(len(lsttxt2_img)):
        fonttxt, fontrect = makefont(lsttxt2_img[y], 5, (0, 0), factor)
        fonttxts2.append(fonttxt)
        fontrects2.append(fontrect)

    background_img, background_rect = makeimg("bigskyforintro.png", False, factor)
    foreground_img, foreground_rect = makeimg("introforeground.png", True, factor)
    liftoff_imgs = []
    liftoff_rects = []
    for num in range(1, 284):   # exhaust stays behind, so would be complicated to animate in pygame
        img = pg.image.load(get_folder_file("Story", str(num) + ".png"))   # load from folder other than 'images'
        img = pg.transform.scale(img, resize(img, factor)).convert_alpha()
        rect = img.get_rect()
        rect.center = (int(scr_width * 7.6 / 10), int(scr_height / 8))
        liftoff_imgs.append(img)
        liftoff_rects.append(rect)

    fps = 20   # of rocket
    fps2 = 15   # of text
    t_animate1 = 0   # for rocket and first line of text
    t_animate2 = 0   # for second line of text
    t_text = 0    # for text sound

    t_local = pg.time.get_ticks() / 1000
    vx_bgd = 15    # pixels / second   (background)
    dx_bgd = 0

    fade_time1 = 0   # fade in
    fade_time2 = 0   # fade out
    alpha1 = 255   # fade in
    alpha2 = 0     # fade out
    endtime = 0    # to end the story after n seconds after the text is fully displayed
    while running and global_running:
        pg.event.pump()

        # Clock
        t0 = t_local
        t_local = pg.time.get_ticks() / 1000
        dt = t_local - t0

        dx_bgd += vx_bgd * dt
        background_rect.center = (int(background_img.get_size()[0] / 2 - dx_bgd), int(scr_height / 2))
        scr.blit(background_img, background_rect)

        if alpha1 <= 0:   # when fade in has finished
            if t_animate1 < len(liftoff_imgs) / fps:
                animate(liftoff_imgs, liftoff_rects, fps, t_animate1, scr)
            else:
                scr.blit(liftoff_imgs[282], liftoff_rects[282])
            t_animate1 += dt

        foreground_rect.center = (int(scr_width / 2), int(scr_height / 2))
        scr.blit(foreground_img, foreground_rect)

        if alpha1 <= 0:    # when fade in has finished
            if t_animate1 < len(lsttxt1_img) / fps2:
                text_animation(lsttxt1_img, fps2, t_animate1, False, int(scr_height * 8.2 / 10), fonttxts1, fontrects1,
                               scr, scr_width, factor)
                t_text += dt
                if t_text > 1 / fps2:
                    channel_2.play(txt_sound)
                    t_text = 0
            else:
                text_animation(lsttxt1_img, fps2, 0, True, int(scr_height * 8.2 / 10), fonttxts1, fontrects1, scr,
                               scr_width, factor)
                t_animate2 += dt
                if t_animate2 < len(lsttxt2_img) / fps2:
                    text_animation(lsttxt2_img, fps2, t_animate2, False,
                                   int(scr_height * 8.7 / 10), fonttxts2, fontrects2, scr, scr_width, factor)
                    t_text += dt
                    if t_text > 1 / fps2:
                        channel_2.play(txt_sound)
                        t_text = 0
                else:
                    text_animation(lsttxt2_img, fps2, 0, True, int(scr_height * 8.7 / 10), fonttxts2, fontrects2, scr,
                                   scr_width, factor)
                    endtime += dt

        if alpha1 > 0:
            fade_time1 += dt
            if fade_time1 > 2 / 255:  # fade is 1 second
                alpha1 -= 2
                fade_time1 = 0
            fade_1 = pg.Surface((scr_width, scr_height)).convert()
            fade_1.fill((0, 0, 0))
            fade_1.set_alpha(alpha1)
            fade_1_rect = fade_1.get_rect()
            fade_1_rect.center = (int(scr_width / 2), int(scr_height / 2))
            scr.blit(fade_1, fade_1_rect)

        if endtime > 3:
            fade_time2 += dt
            if fade_time2 > 4 / 255:  # fade is 2 seconds
                alpha2 += 2
                fade_time2 = 0
            fade = pg.Surface((scr_width, scr_height)).convert()
            fade.fill((0, 0, 0))
            fade.set_alpha(alpha2)
            fade_rect = fade.get_rect()
            fade_rect.center = (int(scr_width / 2), int(scr_height / 2))
            scr.blit(fade, fade_rect)
            if alpha2 >= 300:    # keep the black screen for a short while
                running = False

        pg.display.flip()
        keys = pg.key.get_pressed()
        if keys[pg.K_SPACE] and not chosen:
            running = False
            chosen = True
        if not keys[pg.K_SPACE]:
            chosen = False

        for event in pg.event.get():
            if event.type == pg.QUIT:
                global_running = False
    return global_running, chosen
