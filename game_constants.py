import pygame as pg
from game_tools import get_folder_file, makeimg

# Window setup
original_width = 320
original_height = 240
scale_factor = 3    # Factor is used for all parameters to make the whole game scalable
scr_w = original_width * scale_factor
scr_h = original_height * scale_factor
res = (scr_w, scr_h)

# Music
pg.mixer.pre_init(44100, -16, 2, 512)
pg.mixer.init()
channel_1 = pg.mixer.Channel(0)
channel_2 = pg.mixer.Channel(1)
channel_3 = pg.mixer.Channel(2)
hit1 = pg.mixer.Sound(get_folder_file("Music", "hit1.ogg"))
explode = pg.mixer.Sound(get_folder_file("Music", "explode.ogg"))
blipselect = pg.mixer.Sound(get_folder_file("Music", "blipselect.ogg"))
blipclick = pg.mixer.Sound(get_folder_file("Music", "blipclick.ogg"))
bliplocked = pg.mixer.Sound(get_folder_file("Music", "bliplocked.ogg"))
txt_sound = pg.mixer.Sound(get_folder_file("Music", "txt_sound.ogg"))
pg.mixer.quit()

# Font
main_font = get_folder_file("Images", "retro-sans.ttf")

# Story texts
file1 = open(get_folder_file("Text", "story1.txt"), "r")
storytxt1 = file1.readline().upper()
file1.close()

file2 = open(get_folder_file("Text", "story2.txt"), "r")
storytxt2 = file2.readline().upper()
file2.close()

# Previous highscore
file3 = open(get_folder_file("Text", "highscore.txt"), "r")
high_score = float(file3.readline())    # avoid name clash with underscore
file3.close()

# Rocket lists
rocket_names = ["Water Rocket", "North Korean Rocket", "Stratos IV",
                "N1 Moon Rocket", "Saturn V", "Starship", "Testla Roadster"]
rocketimgs = []
rocketrects = []
rocket_imgs_lock = []
rocket_rects_lock = []
for i in range(len(rocket_names)):
    temp_rocket_img, temp_rocket_rect = makeimg(rocket_names[i] + ".png", True, scale_factor)
    rocketimgs.append(temp_rocket_img)
    rocketrects.append(temp_rocket_rect)
    temp_rocket_locked, temp_rocket_rect_locked = makeimg(rocket_names[i] + "locked.png", True, scale_factor)
    rocket_imgs_lock.append(temp_rocket_locked)
    rocket_rects_lock.append(temp_rocket_rect_locked)

rocket_ax_lst = [1, 2, 3, 4, 5, 6, 7]   # acceleration in x or y  per rocket [pixels / s] (later multiplied by factor)
lives = [1, 2, 3, 4, 5, 6, 7]       # lives that the player gets per rocket

# Heights to reach for unlocking rockets [km]
milestones = [0, 0.2, 100, 10000, 500000, 165000000, 1000000000]

# Altitude scale (better rocket, altitude increases faster)
altscale = [1, 1.2, 1.4, 1.6, 1.8, 2, 2.2]         # acceleration of altitude meter (multiply with y)
aa_lst = [0, 15, 20, 80, 300, 500, 1000]     # acceleration of the altitude meter (add to y, indep. of vy_skyloop)
