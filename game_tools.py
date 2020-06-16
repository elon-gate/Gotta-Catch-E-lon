import pygame as pg
import os
import random


def get_file(file):
    # Returns the full path, if the file is in the same folder as the main .py program.
    # Useful if a computer uses some random directory (like mine)
    path = os.path.join(os.path.dirname(__file__), file)
    return path


def get_folder_file(folder, file):
    # Returns the full path, if the file is not in the same folder as the main .py program.
    # Useful if a computer uses some random directory (like mine)
    extension = os.path.join(folder, file)
    path = get_file(extension)
    return path


def resize(img, scaling):
    # Img should be a surface
    resolution = img.get_size()
    new_reso = (int(resolution[0] * scaling), int(resolution[1] * scaling))
    return new_reso


def animate(img_lst, rect_lst, fps, time, scr):
    # enter a list with surfaces and list with rectangles and the speed of the animation in fps.
    # this function should be called in a loop that has an increasing time t.
    for y in range(len(img_lst)):
        # Modulo makes the time into a value between 0 and 1 seconds.
        # Split time in equal fractions (so e.g. 3 images --> split time into 0-(1/3), (1/3)-(2/3), (2/3)-1).
        # Since we split up the time steps by len(img_lst) components, the time steps get smaller if more images
        # are added. The time should therefore be divided by len(img_lst) to keep the time between the images
        # constant, even if the amount of images changes. So if fps = 1, each time step takes 1 second in real-time.
        # By increasing fps, the opposite happens: a time step takes shorter and thus images will change faster.
        if (y / len(img_lst)) <= ((time * fps / len(img_lst)) % 1) <= ((y + 1) / len(img_lst)):
            scr.blit(img_lst[y], rect_lst[y])


def makefont(txt, size, center, factor):
    # center should be tuple
    # if the image's center is determined by its own size, set center to (0, 0) then use .center and .get_size after.
    font = pg.font.Font(main_font, factor * size)
    img = font.render(txt, False, (255, 255, 255))
    rect = img.get_rect()
    rect.center = center
    return img, rect


def makeimg(name, transparent, factor):
    # all images have to be in the 'Images' folder. Transparent should be a boolean. Scaling factor is equal for
    # every image.
    img = pg.image.load(get_folder_file("Images", name))
    if transparent:
        img = pg.transform.scale(img, resize(img, factor)).convert_alpha()
    else:
        img = pg.transform.scale(img, resize(img, factor)).convert()
    rect = img.get_rect()
    return img, rect


def update_highscore(y, highscore):
    # use in every scenario that the player leaves the game loop
    if y > highscore:
        highscore = y
        prevscore = open(get_folder_file("Text", "highscore.txt"), "w")
        prevscore.write(str(y))
        prevscore.close()
    return highscore


def text_animation(txt_lst, fps, time, blit_all, y_coordinate, fonttxts, fontrects, scr, scr_width, factor):
    # make the text appear letter by letter, similar to animate.
    # 'blit_all' means: if the animation is over and the whole text should be blitted.
    blit_txt = []
    blit_rect = []
    txt_size = 0
    standard, dummy = makefont("A", 5, (0, 0), factor)    # use to give a space a proper width
    for y in range(len(txt_lst)):
        if (y / len(txt_lst)) <= ((time * fps / len(txt_lst)) % 1) or blit_all:
            if txt_lst[y] != " ":
                fonttxt = fonttxts[y]
                fontrect = fontrects[y]
                fontrect.center = (int(scr_width / 20 + txt_size), y_coordinate)
                blit_txt.append(fonttxt)
                blit_rect.append(fontrect)
                txt_size += fonttxt.get_size()[0]
            else:
                txt_size += standard.get_size()[0]

    for x in range(len(blit_txt)):
        scr.blit(blit_txt[x], blit_rect[x])


def get_bird_info(vy_skyloop, bird1_img, bird2_img, bird_flip, scr_width, scr_height, factor):
    y_bird = - scr_height * random.uniform(0.15, 0.3)
    diff_vy_bird = random.uniform(0.7, 0.9)
    x_bird = scr_width * random.uniform(-0.3, 1.3)
    if x_bird < scr_width / 4:
        sign = 1
        magnitude = random.uniform(0.3, 0.8)
    elif x_bird > scr_width * 3 / 4:
        sign = -1
        magnitude = random.uniform(0.3, 0.8)
    else:
        sign = random.randrange(-1, 2, 2)
        magnitude = random.uniform(0.1, 0.6)
    vx_bird = sign * (magnitude * 60 * factor + vy_skyloop / 2)

    if vx_bird > 0 and not bird_flip:  # check orientation of bird
        bird1_img = pg.transform.flip(bird1_img, True, False)
        bird2_img = pg.transform.flip(bird2_img, True, False)
        bird_flip = True
    elif vx_bird < 0 and bird_flip:
        bird1_img = pg.transform.flip(bird1_img, True, False)
        bird2_img = pg.transform.flip(bird2_img, True, False)
        bird_flip = False

    return y_bird, diff_vy_bird, x_bird, vx_bird, bird1_img, bird2_img, bird_flip


def get_asteroid_info(vy_skyloop, scr_width, scr_height, factor):
    diff_vy_asteroid = random.uniform(0.7, 0.9)
    y_asteroid = - scr_height * random.uniform(0.2, 0.5)
    x_asteroid = scr_width * random.uniform(-0.1, 1.1)
    if x_asteroid < scr_width / 4:
        sign = 1
        magnitude = random.uniform(0.2, 0.8)
    elif x_asteroid > scr_width * 3 / 4:
        sign = -1
        magnitude = random.uniform(0.2, 0.8)
    else:
        sign = random.randrange(-1, 2, 2)
        magnitude = random.uniform(0.1, 0.7)
    vx_asteroid = sign * (0.5 * magnitude * 100 * factor + vy_skyloop / 3)
    return y_asteroid, diff_vy_asteroid, x_asteroid, vx_asteroid


def get_plane_info(vy_skyloop, plane_img, plane_flip, scr_width, scr_height, factor):
    y_plane = scr_height * random.uniform(-0.6, 0.3)
    diff_vy_plane = random.uniform(1, 1.4)
    if random.random() > 0.5:   # random choice for plane to appear on left or right side of screen
        x_plane = - scr_width * random.uniform(0.2, 0.4)
        sign = 1
    else:
        x_plane = scr_width * (1 + random.uniform(0.2, 0.4))
        sign = -1

    magnitude = random.uniform(0.8, 1.5)
    vx_plane = sign * (magnitude * 100 * factor + vy_skyloop / 2)

    if vx_plane > 0 and not plane_flip:  # check orientation of plane
        plane_img = pg.transform.flip(plane_img, True, False)
        plane_flip = True
    elif vx_plane < 0 and plane_flip:
        plane_img = pg.transform.flip(plane_img, True, False)
        plane_flip = False

    return y_plane, diff_vy_plane, x_plane, vx_plane, plane_img, plane_flip


def get_sat_info(vy_skyloop, scr_width, scr_height, factor):
    diff_vy_sat = random.uniform(1, 1.5)
    y_sat = - scr_height * random.uniform(0.2, 0.5)
    x_sat = scr_width * random.uniform(-0.1, 1.1)
    if x_sat < scr_width / 4:
        sign = 1
        magnitude = random.uniform(0.2, 0.7)
    elif x_sat > scr_width * 3 / 4:
        sign = -1
        magnitude = random.uniform(0.2, 0.7)
    else:
        sign = random.randrange(-1, 2, 2)
        magnitude = random.uniform(0.1, 0.6)
    vx_sat = sign * (0.5 * magnitude * 70 * factor + vy_skyloop / 3)
    return y_sat, diff_vy_sat, x_sat, vx_sat


# Some constants needed for the functions (cannot import from game_constants since circular import error)
main_font = get_folder_file("Images", "retro-sans.ttf")

original_width = 320
original_height = 240
scale_factor = 3    # Factor is used for all parameters to make the whole game scalable
scr_w = original_width * scale_factor
scr_h = original_height * scale_factor
res = (scr_w, scr_h)
screen = pg.display.set_mode(res)
