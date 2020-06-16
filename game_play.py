import pygame as pg
import random
from game_tools import get_folder_file, animate, makefont, makeimg, update_highscore, get_asteroid_info, \
    get_bird_info, get_plane_info, get_sat_info
from game_constants import channel_1, channel_2, channel_3, hit1, explode, blipselect, blipclick, milestones, \
    altscale, aa_lst, rocket_ax_lst, lives


def game_loop(highscore, global_running, unlocked, chosen, rocket_idx, rocket_imgs, scr, scr_width, scr_height, volume,
              factor):
    # Load images (and convert for smoother blitting (note: don't convert transparent images; they lose
    # transparency))
    rocket0_imgs = []
    rocket0_rects = []
    if rocket_idx == 0:
        for idx in range(1, 5):
            temp_img, temp_rect = makeimg("Water Rocket" + str(idx) + ".png", True, factor)
            rocket0_imgs.append(temp_img)
            rocket0_rects.append(temp_rect)
        rocket1_img = rocket_imgs[rocket_idx]
        rocket1_rect = rocket1_img.get_rect()
    else:
        rocket1_img = rocket_imgs[rocket_idx]
        rocket1_rect = rocket1_img.get_rect()

    # Size of skyloop and spaceloop should be equal
    skyloop_img, skyloop_rect1 = makeimg("cloudrandom3.png", False, factor)
    skyloop_rect2 = skyloop_img.get_rect()  # two images are needed for infinite scrolling of the background
    spaceloop_img, spaceloop_rect1 = makeimg("spaceloop.png", False, factor)
    spaceloop_rect2 = spaceloop_img.get_rect()
    skytospace_img, skytospace_rect = makeimg("skytospace.png", False, factor)
    launchpad_img, launchpad_rect = makeimg("launchsite.png", False, factor)

    if rocket_idx == 0:
        flames_img = []
        flames_rect = []
        for p in range(1, 5):
            flame_temp_img, flame_temp_rect = makeimg("water" + str(p) + ".png", True, factor)
            flames_img.append(flame_temp_img)
            flames_rect.append(flame_temp_rect)
    elif rocket_idx == 6:
        flames_img = []
        flames_rect = []
        for p in range(1, 4):
            flame_temp_img, flame_temp_rect = makeimg("rainfume" + str(p) + ".png", True, factor)
            flames_img.append(flame_temp_img)
            flames_rect.append(flame_temp_rect)
    else:
        flames_img = []
        flames_rect = []
        for p in range(1, 4):
            flame_temp_img, flame_temp_rect = makeimg("fume" + str(p) + ".png", True, factor)
            flames_img.append(flame_temp_img)
            flames_rect.append(flame_temp_rect)

    # asteroid also gets loaded in loop, to choose random asteroid images each time
    rand = random.randint(1, 4)
    asteroid_img, asteroid_rect = makeimg("asteroid" + str(rand) + ".png", True, factor)

    bird1_img, bird1_rect = makeimg("bird1.png", True, factor)  # birds initially look to the left
    bird2_img, bird2_rect = makeimg("bird2.png", True, factor)

    exps_img = []       # explosion images
    expsw_img = []      # white explosion images
    exps_rect1 = []     # rects to animate multiple explosions at once
    exps_rect2 = []
    exps_rect3 = []
    expsw_rect1 = []
    expsw_rect2 = []
    for y in range(1, 17):
        exp_temp_img, exp_temp_rect = makeimg("exp" + str(y) + ".png", True, factor)
        expw_temp_img, expw_temp_rect = makeimg("expw" + str(y) + ".png", True, factor)
        exps_img.append(exp_temp_img)
        expsw_img.append(expw_temp_img)
        exps_rect1.append(exp_temp_rect)
        exps_rect2.append(exp_temp_img.get_rect())  # use command get_rect again to make a complete new rect
        exps_rect3.append(exp_temp_img.get_rect())
        expsw_rect1.append(expw_temp_rect)
        expsw_rect2.append(expw_temp_img.get_rect())

    heart_img, dummy_heart_rect = makeimg("heart.png", True, factor)    # use dummy since amount of hearts can vary
    heart_rects = []
    number_lives = lives[rocket_idx]

    unlock_img, unlock_rect = makeimg("unlock.png", True, factor)
    unlock_rect.center = (int(scr_width * 8.5 / 10), int(scr_height * 9 / 10))

    pointer_img, pointer_rect = makeimg("pointer.png", True, factor)
    backgroundpause_img, backgroundpause_rect = makeimg("backgroundpause.png", True, factor)
    backgroundpause_rect.center = (int(scr_width / 2), int(scr_height / 2))

    plane_img, plane_rect = makeimg("A380.png", True, factor)   # plane initially looks to left

    sat_img, sat_rect1 = makeimg("satellite.png", True, factor)  # satellites (two)
    sat_rect2 = sat_img.get_rect()

    moon_img, moon_rect = makeimg("moon.png", True, factor)
    moon_x = scr_width * random.uniform(0.3, 0.7)
    moon_y = - scr_height / 2
    moon_rect.center = (int(moon_x), int(moon_y))
    moon = False

    # Rocket movement
    x_rocket = int(scr_width / 7)
    if rocket_idx == 0:
        y_rocket = int(scr_height - 32 * factor - (rocket1_img.get_size()[1] / 2))
        for s in range(len(rocket0_imgs)):
            rocket0_rects[s].center = (x_rocket, y_rocket)
        rocket1_rect.center = (x_rocket, y_rocket)
    else:
        y_rocket = int(scr_height - 32 * factor - (rocket1_img.get_size()[1] / 2))
        rocket1_rect.center = (x_rocket, y_rocket)
    vx_rocket = 0               # speed in [pixels/s]
    ax_rocket = 2 * (factor + rocket_ax_lst[rocket_idx])       # acceleration in [pixels/s^2]
    vx_rocket_lim = (rocket_ax_lst[rocket_idx] ** 2) * 25 * factor    # speed limit in [pixels/s]
    vy_rocket = 0      # only just after launch, to bring the rocket down a bit
    ay_rocket = factor * 2 + rocket_ax_lst[rocket_idx] / (2 * factor)   # only just after launch, lower the rocket

    # Background movement
    x_skyloop = int(scr_width / 2)
    y_skyloop0 = int(scr_height - (skyloop_img.get_size()[1] / 2))
    y_skyloop = y_skyloop0
    vy_skyloop = 0   # speed in [pixels/s]
    ay_skyloop = factor * (3 + rocket_ax_lst[rocket_idx] / 3)    # acceleration in [pixels/s^2]
    vy_skyloop_lim = rocket_ax_lst[rocket_idx] * 200 * factor

    y_skytospace = 0

    x_launchpad = int(scr_width / 2)
    y_launchpad0 = int(scr_height - (launchpad_img.get_size()[1] / 2))
    y_launchpad = y_launchpad0

    y_asteroid, diff_vy_asteroid, x_asteroid, vx_asteroid = get_asteroid_info(vy_skyloop, scr_width, scr_height, factor)

    bird_flip = False
    y_bird, diff_vy_bird, x_bird, vx_bird, bird1_img, bird2_img, bird_flip = \
        get_bird_info(vy_skyloop, bird1_img, bird2_img, bird_flip, scr_width, scr_height, factor)
    t_birds = 0

    plane_flip = False
    y_plane, diff_vy_plane, x_plane, vx_plane, plane_img, plane_flip = \
        get_plane_info(vy_skyloop, plane_img, plane_flip, scr_width, scr_height, factor)

    # two satellites, since they are slow and it shouldn't be too easy
    y_sat1, diff_vy_sat1, x_sat1, vx_sat1 = get_sat_info(vy_skyloop, scr_width, scr_height, factor)
    y_sat2, diff_vy_sat2, x_sat2, vx_sat2 = get_sat_info(vy_skyloop, scr_width, scr_height, factor)

    # Game loop
    running = True
    t = pg.time.get_ticks() / 1000
    t_local = 0
    y = (y_skyloop - y_skyloop0) / 3000     # in km
    bird_flying = True
    plane_flying = False
    first_plane = True    # see when the plane starts blitting (otherwise vx_plane will stay constant thus never blit)
    change_plane = True    # set to false if plane has changed (so that it doesn't have to make the img every time)
    sat_flying1 = False
    first_sat1 = True
    sat_flying2 = False
    first_sat2 = True
    asteroid_flying = False
    in_space = False
    collidecheck = True    # have a 5 second no-hit time after you have been hit
    timeout = 3    # seconds
    check_timeout = 0    # seconds  (if you get hit but still have lives left)

    unlock_note = 5    # seconds (message appears if you unlock a new rocket)
    # See if a new rocket is unlocked: find next locked rocket
    next_rocket = 0
    for g in milestones:
        if highscore >= g:
            next_rocket += 1
    t_check = 0     # reference time to remove message after x seconds
    a_note = 500 * factor      # make the notification fly in/out screen
    v_note = 0
    x_note = scr_width + unlock_img.get_size()[0]

    pause_clock = 0    # use pause time to continue where you left off after pausing game

    aa = 0

    to_rocket_menu = False    # see if user goes to rocket menu after dying or pause screen
    pressed = False    # see if arrow keys are pressed

    pg.mixer.music.stop()
    time_passed_music = 0.      # used for timing of song intro and song loop
    intro_time = 3.50           # seconds    (time the intro of the song plays)
    intro_running = True
    intro_music = pg.mixer.Sound(get_folder_file("Music", "GAME_MAIN_THEME_INTRO.ogg"))
    channel_1.set_volume(volume / 100)
    channel_1.play(intro_music)
    countdown = pg.mixer.Sound(get_folder_file("Music", "countdown3.ogg"))
    channel_2.set_volume(volume / 100)
    channel_2.play(countdown)
    channel_3.set_volume(volume / 100)

    while running and global_running:
        pg.event.pump()
        # Clock
        t0 = t
        t = (pg.time.get_ticks() - pause_clock) / 1000
        dt = t - t0
        t_local += dt
        t_birds += dt

        # Music handling
        time_passed_music += dt
        if time_passed_music > intro_time and intro_running:
            pg.mixer.music.load(get_folder_file("Music", "GAME_MAIN_THEME_LOOP.ogg"))
            pg.mixer.music.play(-1)
            intro_running = False

        # Key handling
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] and x_rocket > rocket1_img.get_width():
            x_rocket -= vx_rocket * dt
        if keys[pg.K_RIGHT] and x_rocket < (scr_width - rocket1_img.get_width()):
            x_rocket += vx_rocket * dt
        if keys[pg.K_SPACE] and not chosen:    # enter pause menu
            play_again = False
            paused = True
            chosen = True
            choose_rocket = False
            pg.mixer.pause()
            pg.mixer.music.pause()

            # Pointer properties
            choice = 1
            choice_position = int(scr_height * 0.5)

            rel_y = (y_skyloop - y_skyloop0) % skyloop_img.get_size()[1]  # to prevent that that it is undefined
            y = ((((y_skyloop - y_skyloop0) / factor) + aa ** (1 + t_local / 100)) ** 1.2) * altscale[rocket_idx] / \
                15000

            scr_txt1, scr_txt1_rect = makefont("ALTITUDE", 5, (0, 0), factor)
            scr_txt1_rect.center = (int((scr_width * 14 / 15) - scr_txt1.get_size()[0] / 2),
                                    int(scr_height / 15))
            scr_txt2, scr_txt2_rect = makefont(f"{y:,.2f} KM", 5, (0, 0), factor)
            scr_txt2_rect.center = (int((scr_width * 14 / 15) - scr_txt2.get_size()[0] / 2),
                                    int(scr_height / 10))
            txt_pause1, txt_pause1_rect = makefont("GAME PAUSED", 10, (int(scr_width / 2), int(scr_height * 0.4)),
                                                   factor)
            txt_pause2, txt_pause2_rect = makefont("RESUME", 5, (int(scr_width / 2), int(scr_height * 0.5)), factor)
            txt_pause3, txt_pause3_rect = makefont("RESTART", 5, (int(scr_width / 2), int(scr_height * 0.55)), factor)
            txt_pause6, txt_pause6_rect = makefont("CHOOSE ROCKET", 5, (int(scr_width / 2), int(scr_height * 0.6)),
                                                   factor)
            txt_pause4, txt_pause4_rect = makefont("MAIN MENU", 5, (int(scr_width / 2), int(scr_height * 0.65)), factor)
            txt_pause5, txt_pause5_rect = makefont("QUIT", 5, (int(scr_width / 2), int(scr_height * 0.7)), factor)

            while paused and global_running and running:
                pg.event.pump()
                # Clock
                t0 = t
                t = pg.time.get_ticks() / 1000
                dt = t - t0

                pause_clock += dt
                # Add second picture to fill up empty space
                if rel_y >= (skyloop_img.get_size()[1] - scr_height) and y_skytospace < scr_height and running:
                    scr.blit(skyloop_img, skyloop_rect2)
                if rel_y >= (spaceloop_img.get_size()[1] - scr_height) and y_skytospace > scr_height and running:
                    scr.blit(spaceloop_img, spaceloop_rect2)

                if y_skytospace < scr_height and running:
                    scr.blit(skyloop_img, skyloop_rect1)
                if in_space:
                    scr.blit(spaceloop_img, spaceloop_rect1)
                if y >= 100 and y_skytospace < skytospace_img.get_size()[1] * 2:  # transition from sky to space
                    skytospace_rect.center = (int(x_skyloop), int(y_skytospace - skytospace_img.get_size()[1] / 2))
                    scr.blit(skytospace_img, skytospace_rect)

                if y_launchpad <= launchpad_img.get_size()[1] * 2:  # only shows during launch
                    launchpad_rect.center = (int(x_launchpad), int(y_launchpad))
                    scr.blit(launchpad_img, launchpad_rect)
                if moon:
                    scr.blit(moon_img, moon_rect)

                # Altitude meter
                scr.blit(scr_txt1, scr_txt1_rect)
                scr.blit(scr_txt2, scr_txt2_rect)

                # Hearts / lives
                for j in range(number_lives):
                    heart_rects.append(heart_img.get_rect())
                    heart_rects[j].center = (int((scr_width / 15) + j * heart_img.get_size()[0] * 1.5),
                                             int(scr_height / 15))
                    scr.blit(heart_img, heart_rects[j])

                rocket1_rect.center = (int(x_rocket), int(y_rocket))
                scr.blit(rocket1_img, rocket1_rect)

                if t_local > 4:
                    flames_rect[0].center = (int(x_rocket), int(y_rocket + factor * 20 + rocket1_img.get_size()[1] / 2))
                    scr.blit(flames_img[0], flames_rect[0])

                if next_rocket != 7:
                    unlock_rect.center = (int(x_note), int(scr_height * 9 / 10))
                    scr.blit(unlock_img, unlock_rect)

                if bird_flying and t_local > 5:
                    bird1_rect.center = (int(x_bird), int(y_bird))
                    scr.blit(bird1_img, bird1_rect)

                if plane_flying:
                    plane_rect.center = (int(x_plane), int(y_plane))
                    scr.blit(plane_img, plane_rect)

                if sat_flying1:
                    sat_rect1.center = (int(x_sat1), int(y_sat1))
                    scr.blit(sat_img, sat_rect1)
                if sat_flying2:
                    sat_rect2.center = (int(x_sat2), int(y_sat2))
                    scr.blit(sat_img, sat_rect2)

                if asteroid_flying:
                    asteroid_rect.center = (int(x_asteroid), int(y_asteroid))
                    scr.blit(asteroid_img, asteroid_rect)

                scr.blit(backgroundpause_img, backgroundpause_rect)
                scr.blit(txt_pause1, txt_pause1_rect)
                scr.blit(txt_pause2, txt_pause2_rect)
                scr.blit(txt_pause3, txt_pause3_rect)
                scr.blit(txt_pause6, txt_pause6_rect)
                scr.blit(txt_pause4, txt_pause4_rect)
                scr.blit(txt_pause5, txt_pause5_rect)

                # Position pointer accordingly
                for num in range(1, 6):
                    if choice == num:
                        choice_position = int(scr_height * (0.45 + num * 0.05))
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
                        paused = False
                    if choice == 2:
                        play_again = True
                    if choice == 3:
                        choose_rocket = True
                    if choice == 4:
                        running = False
                    if choice == 5:
                        global_running = False
                    chosen = True
                if not keys[pg.K_SPACE]:
                    chosen = False

                if running and global_running:
                    pg.display.flip()

                if play_again:
                    highscore = update_highscore(y, highscore)    # update again to make new rocket detection work
                    highscore, global_running, unlocked, to_rocket_menu, chosen = \
                        game_loop(highscore, global_running, unlocked, chosen, rocket_idx, rocket_imgs, scr, scr_width,
                                  scr_height, volume, factor)
                    running = False
                if choose_rocket:
                    to_rocket_menu = True
                    running = False

                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        global_running = False
            if global_running and running:
                pg.mixer.unpause()
                pg.mixer.music.unpause()
        if not keys[pg.K_SPACE]:
            chosen = False

        # Integration of speeds and accelerations (up to a maximum)
        if 4 < t_local and y_rocket < scr_height - 32 * factor - (rocket1_img.get_size()[1] / 3.3):
            vy_rocket += ay_rocket * dt
            y_rocket += vy_rocket * dt
        elif vy_rocket > 0:
            vy_rocket -= ay_rocket * dt
            y_rocket += vy_rocket * dt
        else:
            vy_rocket = 0
        if vx_rocket < vx_rocket_lim and t_local > 6:
            vx_rocket += ax_rocket * dt
        if vy_skyloop < vy_skyloop_lim and t_local > 4:
            vy_skyloop += ay_skyloop * dt
        y_skyloop += vy_skyloop * dt

        # Check if the image has scrolled its own length, then let it loop again. Note: rel_y starts at zero and
        # continues from there again if it exceeds the image size (e.g. when the image fully leaves the screen)
        rel_y = (y_skyloop - y_skyloop0) % skyloop_img.get_size()[1]
        skyloop_rect1.center = (int(x_skyloop), int(rel_y + y_skyloop0))
        skyloop_rect2.center = (int(x_skyloop), int(rel_y + y_skyloop0 - skyloop_img.get_size()[1]))
        spaceloop_rect1.center = (int(x_skyloop), int(rel_y + y_skyloop0))
        spaceloop_rect2.center = (int(x_skyloop), int(rel_y + y_skyloop0 - skyloop_img.get_size()[1]))

        # Draw screen
        # Add second picture to fill up empty space
        # Use skytospace transition to figure out if the images should be blitted. If skytospace is in the center of
        # the screen, it covers the whole screen.
        if rel_y >= (skyloop_img.get_size()[1] - scr_height) and y_skytospace < scr_height and running:
            scr.blit(skyloop_img, skyloop_rect2)
        if rel_y >= (spaceloop_img.get_size()[1] - scr_height) and y_skytospace > scr_height and running:
            scr.blit(spaceloop_img, spaceloop_rect2)

        if y_skytospace < scr_height and running:
            scr.blit(skyloop_img, skyloop_rect1)
        if in_space:
            scr.blit(spaceloop_img, spaceloop_rect1)
        if y >= 100 and y_skytospace < skytospace_img.get_size()[1] * 2:    # transition from sky to space
            y_skytospace += vy_skyloop * dt   # y_skytospace is location of BOTTOM of image!
            skytospace_rect.center = (int(x_skyloop), int(y_skytospace - skytospace_img.get_size()[1] / 2))
            scr.blit(skytospace_img, skytospace_rect)
            if y_skytospace > skytospace_img.get_size()[1] - scr_height:
                in_space = True

        y_launchpad += vy_skyloop * dt
        if y_launchpad <= launchpad_img.get_size()[1] * 2:      # only shows during launch
            launchpad_rect.center = (int(x_launchpad), int(y_launchpad))
            scr.blit(launchpad_img, launchpad_rect)

        if y > 384400 and moon_y < scr_height * 1.5:
            moon = True
            moon_y += 0.5 * vy_skyloop * dt
            moon_rect.center = (int(moon_x), int(moon_y))
            scr.blit(moon_img, moon_rect)
        else:
            moon = False

        if rocket_idx == 0 and running:
            if not collidecheck:
                if (check_timeout % 0.6) > 0.3:    # make rocket flicker to indicate timeout
                    for r in range(len(rocket0_imgs)):
                        rocket0_rects[r].center = (int(x_rocket), int(y_rocket))
                    animate(rocket0_imgs, rocket0_rects, 5, t, scr)
                    rocket1_rect.center = (int(x_rocket), int(y_rocket))
            else:
                for r in range(len(rocket0_imgs)):
                    rocket0_rects[r].center = (int(x_rocket), int(y_rocket))
                animate(rocket0_imgs, rocket0_rects, 5, t, scr)
                rocket1_rect.center = (int(x_rocket), int(y_rocket))
        else:
            if not collidecheck:
                if (check_timeout % 0.6) > 0.3:
                    rocket1_rect.center = (int(x_rocket), int(y_rocket))
                    scr.blit(rocket1_img, rocket1_rect)
            else:
                rocket1_rect.center = (int(x_rocket), int(y_rocket))
                scr.blit(rocket1_img, rocket1_rect)

        # Generate random obstacles. Range is amount of obstacles to be blitted.
        # Check if bird has left screen so that it doesn't disappear when a new bird appears (only 1 bird img available)
        if y_bird > random.uniform(1.15, 1.3) * scr_height or - scr_width * 0.35 > x_bird or x_bird > scr_width * 1.35:
            y_bird, diff_vy_bird, x_bird, vx_bird, bird1_img, bird2_img, bird_flip = \
                get_bird_info(vy_skyloop, bird1_img, bird2_img, bird_flip, scr_width, scr_height, factor)
            if y > 5:           # check if too high to fly, check nested because bird should not suddenly disappear
                bird_flying = False
            t_birds = 0
        if y > 5 and not bird_flying:
            if y_plane > random.uniform(1.3, 2) * scr_height or - scr_width * random.uniform(3, 6) > x_plane or \
                    x_plane > scr_width * random.uniform(3, 6) or first_plane:
                plane_flying = True
                first_plane = False
                if y > 40 and change_plane:    # change airplane type. Dynamics stay the same
                    plane_img, plane_rect = makeimg("concorde.png", True, factor)  # plane initially looks to left
                    plane_flip = False
                    change_plane = False
                y_plane, diff_vy_plane, x_plane, vx_plane, plane_img, plane_flip = \
                    get_plane_info(vy_skyloop, plane_img, plane_flip, scr_width, scr_height, factor)
                if y > 100:   # nested because otherwise a plane might disappear suddenly at y = 100
                    plane_flying = False
        if y > 100 and not plane_flying:   # check if satellites should fly
            if y_sat1 > random.uniform(1.2, 2) * scr_height or - scr_width * 0.11 > x_sat1 \
                    or x_sat1 > scr_width * 1.11 or first_sat1:
                sat_flying1 = True
                first_sat1 = False
                y_sat1, diff_vy_sat1, x_sat1, vx_sat1 = get_sat_info(vy_skyloop, scr_width, scr_height, factor)
                if y > 35000:
                    sat_flying1 = False
            if y_sat2 > random.uniform(1.2, 2) * scr_height or - scr_width * 0.11 > x_sat2 \
                    or x_sat2 > scr_width * 1.11 or first_sat2:
                sat_flying2 = True
                first_sat2 = False
                y_sat2, diff_vy_sat2, x_sat2, vx_sat2 = get_sat_info(vy_skyloop, scr_width, scr_height, factor)
                if y > 35000:
                    sat_flying2 = False

        if y > 35000 and not sat_flying1 and not sat_flying2:    # if asteroid should appear
            asteroid_flying = True
            if y_asteroid > random.uniform(1.2, 5) * scr_height or - scr_width * 0.15 > x_asteroid \
                    or x_asteroid > scr_width * 1.15:     # check if asteroid has left screen
                y_asteroid, diff_vy_asteroid, x_asteroid, vx_asteroid = get_asteroid_info(vy_skyloop, scr_width,
                                                                                          scr_height, factor)
                rand = random.randint(1, 4)
                asteroid_img, asteroid_rect = makeimg("asteroid" + str(rand) + ".png", True, factor)

        if bird_flying and t_local > 5:
            vy_bird = vy_skyloop / diff_vy_bird
            y_bird += vy_bird * dt
            x_bird += vx_bird * dt
            bird1_rect.center = (int(x_bird), int(y_bird))
            bird2_rect.center = (int(x_bird), int(y_bird))
            birds_img = [bird1_img, bird2_img]
            birds_rect = [bird1_rect, bird2_rect]
            animate(birds_img, birds_rect, 3, t, scr)
        if plane_flying:
            vy_plane = vy_skyloop / diff_vy_plane
            y_plane += vy_plane * dt
            x_plane += vx_plane * dt
            plane_rect.center = (int(x_plane), int(y_plane))
            scr.blit(plane_img, plane_rect)
        if asteroid_flying:
            vy_asteroid = vy_skyloop / diff_vy_asteroid
            y_asteroid += vy_asteroid * dt
            x_asteroid += vx_asteroid * dt
            asteroid_rect.center = (int(x_asteroid), int(y_asteroid))
            scr.blit(asteroid_img, asteroid_rect)
        if sat_flying1:
            vy_sat1 = vy_skyloop / diff_vy_sat1
            y_sat1 += vy_sat1 * dt
            x_sat1 += vx_sat1 * dt
            sat_rect1.center = (int(x_sat1), int(y_sat1))
            scr.blit(sat_img, sat_rect1)
        if sat_flying2:
            vy_sat2 = vy_skyloop / diff_vy_sat2
            y_sat2 += vy_sat2 * dt
            x_sat2 += vx_sat2 * dt
            sat_rect2.center = (int(x_sat2), int(y_sat2))
            scr.blit(sat_img, sat_rect2)

        # Fume animation
        for j in flames_rect:
            j.center = (int(x_rocket), int(y_rocket + factor * 20 + rocket1_img.get_size()[1] / 2))
        if t_local > 4:
            if not collidecheck:
                if (check_timeout % 0.6) > 0.3:
                    animate(flames_img, flames_rect, 15, t, scr)
            else:
                animate(flames_img, flames_rect, 15, t, scr)

        # Altitude meter
        if t_local > 4:
            aa += aa_lst[rocket_idx] * dt
        y = ((((y_skyloop - y_skyloop0) / factor) + aa ** (1 + t_local / 100)) ** 1.2) * altscale[rocket_idx] / 15000
        scr_txt1, scr_txt1_rect = makefont("ALTITUDE", 5, (0, 0), factor)
        scr_txt1_rect.center = (int((scr_width * 14 / 15) - scr_txt1.get_size()[0] / 2), int(scr_height / 15))
        scr_txt2, scr_txt2_rect = makefont(f"{y:,.2f} KM", 5, (0, 0), factor)
        scr_txt2_rect.center = (int((scr_width * 14 / 15) - scr_txt2.get_size()[0] / 2), int(scr_height / 10))
        scr.blit(scr_txt1, scr_txt1_rect)
        scr.blit(scr_txt2, scr_txt2_rect)

        # Hearts / lives
        for j in range(number_lives):
            heart_rects.append(heart_img.get_rect())
            heart_rects[j].center = (int((scr_width / 15) + j * heart_img.get_size()[0] * 1.5), int(scr_height / 15))
            scr.blit(heart_img, heart_rects[j])

        # Check if altitude is above the next milestone
        if next_rocket != 7 and running:
            if y > milestones[next_rocket] and t_check < unlock_note:
                t_check += dt
                if t_check < 0.45:
                    v_note += a_note * dt
                elif 0.45 < t_check < 0.9:
                    v_note -= a_note * dt
                elif unlock_note - 0.9 < t_check < unlock_note - 0.45:
                    v_note -= a_note * dt
                elif t_check > unlock_note - 0.45:
                    v_note += a_note * dt
                else:
                    v_note = 0
                x_note -= v_note * dt
                unlock_rect.center = (int(x_note), int(scr_height * 9 / 10))
                scr.blit(unlock_img, unlock_rect)
            if t_check > unlock_note:
                next_rocket += 1
                t_check = 0
                x_note = scr_width + unlock_img.get_size()[0]

        # Update screen
        if running and global_running:
            pg.display.flip()

        if not collidecheck:
            check_timeout += dt
            if check_timeout >= timeout:
                check_timeout = 0
                collidecheck = True

        # Check collisions
        if (rocket1_rect.colliderect(asteroid_rect) or rocket1_rect.colliderect(bird1_rect) or
                rocket1_rect.colliderect(plane_rect) or rocket1_rect.colliderect(sat_rect1) or
                rocket1_rect.colliderect(sat_rect2)) and check_timeout == 0:
            number_lives -= 1
            if number_lives != 0:
                channel_2.play(hit1)
            collidecheck = False
        if (rocket1_rect.colliderect(asteroid_rect) or rocket1_rect.colliderect(bird1_rect) or
                rocket1_rect.colliderect(plane_rect) or rocket1_rect.colliderect(sat_rect1) or
                rocket1_rect.colliderect(sat_rect2)) and number_lives == 0 and check_timeout == 0:
            channel_2.play(explode)
            pg.mixer.music.stop()
            pg.mixer.music.load(get_folder_file("Music", "game_over_music3.ogg"))
            pg.mixer.music.play(0)
            for k in exps_rect1:
                k.center = (int(x_rocket + rocket1_img.get_size()[0] / 5), int(y_rocket))
            for n in exps_rect2:
                n.center = (int(x_rocket - rocket1_img.get_size()[0]/2), int(y_rocket - rocket1_img.get_size()[1]))
            for m in exps_rect3:
                m.center = (int(x_rocket - rocket1_img.get_size()[0]), int(y_rocket + rocket1_img.get_size()[1]/1.5))
            for p in expsw_rect1:
                p.center = (int(x_rocket + rocket1_img.get_size()[0]/3), int(y_rocket - rocket1_img.get_size()[1]/3))
            for z in expsw_rect2:
                z.center = (int(x_rocket + rocket1_img.get_size()[0]), int(y_rocket + rocket1_img.get_size()[1]))

            t00 = t

            play_again = False
            rocket_choose = False

            # Pointer properties
            choice = 1
            choice_position = int(scr_height * 0.5)

            # Screen fade. alpha1 is fade out for game play, alpha2 is fade in for menu
            alpha1 = 0   # transparency; 0 is transparent, 255 is opaque
            fade_time1 = 0
            alpha2 = 255
            fade_time2 = 0
            while running and global_running:
                pg.event.pump()
                # Clock
                t0 = t
                t = ((pg.time.get_ticks()) / 1000) - t00
                dt = t - t0

                # add second picture to fill empty space
                if rel_y >= (skyloop_img.get_size()[1] - scr_height) and y_skytospace < scr_height and running:
                    scr.blit(skyloop_img, skyloop_rect2)
                if rel_y >= (spaceloop_img.get_size()[1] - scr_height) and y_skytospace > scr_height and running:
                    scr.blit(spaceloop_img, spaceloop_rect2)

                if y_skytospace < scr_height and running:
                    scr.blit(skyloop_img, skyloop_rect1)
                if in_space:
                    scr.blit(spaceloop_img, spaceloop_rect1)
                if y >= 100 and y_skytospace < skytospace_img.get_size()[1] * 2:  # transition from sky to space
                    skytospace_rect.center = (int(x_skyloop), int(y_skytospace - skytospace_img.get_size()[1] / 2))
                    scr.blit(skytospace_img, skytospace_rect)

                if y_launchpad <= launchpad_img.get_size()[1] * 2:  # only shows during launch
                    launchpad_rect.center = (int(x_launchpad), int(y_launchpad))
                    scr.blit(launchpad_img, launchpad_rect)

                if moon:
                    scr.blit(moon_img, moon_rect)

                if bird_flying and t_local > 5:
                    scr.blit(bird1_img, bird1_rect)
                if plane_flying:
                    scr.blit(plane_img, plane_rect)
                if asteroid_flying:
                    scr.blit(asteroid_img, asteroid_rect)
                if sat_flying1:
                    scr.blit(sat_img, sat_rect1)
                if sat_flying2:
                    scr.blit(sat_img, sat_rect2)
                scr.blit(scr_txt1, scr_txt1_rect)
                scr.blit(scr_txt2, scr_txt2_rect)
                ani_duration = (len(exps_img)) / 20
                if t < 2 * ani_duration:
                    animate(exps_img, exps_rect1, 20, t, scr)
                if (ani_duration / 5) < t < ((ani_duration / 5) + 2 * ani_duration):
                    t = t - (ani_duration / 5)
                    animate(expsw_img, expsw_rect1, 20, t, scr)
                    t = (pg.time.get_ticks() / 1000) - t00
                if (2 * (ani_duration / 5)) < t < ((2 * ani_duration / 5) + 2 * ani_duration):
                    t = t - 2 * ani_duration / 5
                    animate(exps_img, exps_rect3, 20, t, scr)
                    t = (pg.time.get_ticks() / 1000) - t00
                if (3 * (ani_duration / 5)) < t < ((3 * ani_duration / 5) + 2 * ani_duration):
                    t = t - 3 * ani_duration / 5
                    animate(expsw_img, expsw_rect2, 20, t, scr)
                    t = (pg.time.get_ticks() / 1000) - t00
                if (4 * (ani_duration / 5)) < t < ((4 * ani_duration / 5) + 2 * ani_duration):
                    t = t - 4 * ani_duration / 5
                    animate(exps_img, exps_rect2, 20, t, scr)
                    t = (pg.time.get_ticks() / 1000) - t00

                if t > ani_duration:
                    fade_time1 += dt
                    if fade_time1 > 4 / 255:     # fade is 2 seconds
                        alpha1 += 2
                        fade_time1 = 0
                    fade = pg.Surface((scr_width, scr_height))
                    fade.fill((0, 0, 0))
                    fade.set_alpha(alpha1)
                    fade_rect = fade.get_rect()
                    fade_rect.center = (int(scr_width / 2), int(scr_height / 2))
                    scr.blit(fade, fade_rect)

                    if alpha1 > 255:
                        # Blit text
                        scr_txt1, scr_txt1_rect = makefont("YOU'RE OUT!", 10,
                                                           (int(scr_width / 2), int(scr_height * 0.3)), factor)
                        scr.blit(scr_txt1, scr_txt1_rect)
                        scr_txt2, scr_txt2_rect = makefont("PLAY AGAIN", 5, (int(scr_width / 2), int(scr_height * 0.5)),
                                                           factor)
                        scr.blit(scr_txt2, scr_txt2_rect)
                        txt_choose_rocket, txt_choose_rocket_rect = makefont("CHOOSE ROCKET", 5,
                                                                             (int(scr_width / 2),
                                                                              int(scr_height * 0.55)), factor)
                        scr.blit(txt_choose_rocket, txt_choose_rocket_rect)
                        scr_txt3, scr_txt3_rect = makefont("MAIN MENU", 5, (int(scr_width / 2), int(scr_height * 0.6)),
                                                           factor)
                        scr.blit(scr_txt3, scr_txt3_rect)
                        scr_txt4, scr_txt4_rect = makefont("QUIT", 5, (int(scr_width / 2), int(scr_height * 0.65)),
                                                           factor)
                        scr.blit(scr_txt4, scr_txt4_rect)
                        txt_final_score, txt_final_score_rect = \
                            makefont(f"YOU REACHED {y:,.2f} KM.", 4, (int(scr_width / 2), int(scr_height * 0.38)),
                                     factor)
                        scr.blit(txt_final_score, txt_final_score_rect)

                        # Position pointer accordingly
                        if choice == 1:  # Play again
                            choice_position = int(scr_height * 0.5)
                        if choice == 2:  # Choose rocket
                            choice_position = int(scr_height * 0.55)
                        if choice == 3:  # main menu
                            choice_position = int(scr_height * 0.6)
                        if choice == 4:   # quit
                            choice_position = int(scr_height * 0.65)
                        pointer_rect.center = (int(scr_width / 3), choice_position)
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
                        if keys[pg.K_SPACE] and not chosen:
                            channel_3.play(blipclick)
                            if choice == 1:
                                play_again = True
                            if choice == 2:
                                rocket_choose = True
                            if choice == 3:
                                running = False
                            if choice == 4:
                                global_running = False
                            chosen = True
                        if not keys[pg.K_SPACE]:
                            chosen = False

                        fade_time2 += dt
                        if fade_time2 > 4 / 255 and alpha2 > 0:  # make sure it stays positive
                            alpha2 -= 2
                            fade_time2 = 0
                        fade.set_alpha(alpha2)
                        scr.blit(fade, fade_rect)

                if running and global_running:
                    pg.display.flip()

                # Event handling
                if play_again:
                    highscore, global_running, unlocked, to_rocket_menu, chosen = \
                        game_loop(highscore, global_running, unlocked, chosen, rocket_idx, rocket_imgs, scr, scr_width,
                                  scr_height, volume, factor)
                    running = False
                if rocket_choose:
                    to_rocket_menu = True
                    running = False

                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        global_running = False

        # Event handling
        for event in pg.event.get():
            if event.type == pg.QUIT:
                global_running = False
        # always update highscore if game_loop is left
        if not running or not global_running:
            highscore = update_highscore(y, highscore)

    return highscore, global_running, unlocked, to_rocket_menu, chosen
