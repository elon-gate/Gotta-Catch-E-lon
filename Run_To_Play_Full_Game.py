import pygame as pg
from game_tools import get_folder_file
from game_constants import res, scr_w, scr_h, scale_factor, rocket_rects_lock, rocket_imgs_lock, rocketimgs, \
    rocketrects, high_score
from main_menu import main_menu
from other_menus import intro_story


# --------------------- MAIN PROGRAM --------------------
# Initialize mixer before pg to avoid audio lag
pg.mixer.pre_init(44100, -16, 2, 512)
pg.mixer.init()
pg.init()

# Window setup
screen = pg.display.set_mode(res)

# Title and icon
pg.display.set_caption("Gotta Catch E'lon")
icon = pg.image.load(get_folder_file("Images", "icon.png"))
pg.display.set_icon(icon)

# Font
pg.font.init()
main_font = get_folder_file("Images", "retro-sans.ttf")

# Music
audiovolume = 100    # volume from 0-100 %

# Play game
glob_run, skip_intro = intro_story(screen, scr_w, scr_h, audiovolume, scale_factor)  # avoid nameclash global_running
main_menu(high_score, glob_run, skip_intro, rocket_rects_lock, rocket_imgs_lock, rocketimgs, rocketrects,
          screen, scr_w, scr_h, audiovolume, scale_factor)
pg.quit()
