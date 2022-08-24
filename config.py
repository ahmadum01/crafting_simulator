from os import path
win_width, win_height = 1280, 800
win_bg_color = 'white'  # '#403c44'

COLOR_TEXT = '#242424'
COLOR_FRAME = '#242424'
COLOR_TEXT_MAIN_SLOT = 'red'
COLOR_TEXT_STATEMENT = '#242424'


image_path = path.join('src', 'images')
images = {}
for letter in 'ABCDE':
    images.update({f'{letter.lower()}{level}': path.join(image_path, f'{letter}{level}.png') for level in range(1, 5)})
for i in range(1, 6):
    images[f'serum_{i}'] = path.join(image_path, f'serum_{i}.png')
images['empty_serum'] = path.join(image_path, 'empty_serum.png')


