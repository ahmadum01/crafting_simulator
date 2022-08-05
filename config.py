from os import path
win_width, win_height = 1280, 800
win_bg_color = 'white'  # '#403c44'

COLOR_TEXT = '#242424'
COLOR_FRAME = '#242424'
COLOR_TEXT_MAIN_SLOT = 'red'
COLOR_TEXT_STATEMENT = '#242424'


image_path = path.join('src', 'images')
images = {
    'a': path.join(image_path, 'A.png'),
    'b': path.join(image_path, 'B.png'),
    'c': path.join(image_path, 'C.png'),
    'd': path.join(image_path, 'D.png'),
    'e': path.join(image_path, 'E.png'),
    'serum': path.join(image_path, 'serum.png'),
    'empty_serum': path.join(image_path, 'empty_serum.png'),
}
