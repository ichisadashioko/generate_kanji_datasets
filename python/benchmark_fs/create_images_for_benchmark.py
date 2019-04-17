import random

import numpy as np
from PIL import Image


def create_64_kb_image():
    img = Image.new('L', (256, 254))
    np_img = np.array(img)

    height, width = np_img.shape[:2]

    for i in range(height):
        for j in range(width):
            np_img[i][j] = random.randint(0, 255)

    img = Image.fromarray(np_img, mode='L')
    return img


def create_16_kb_image():
    img = Image.new('L', (127, 126))
    np_img = np.array(img)

    height, width = np_img.shape[:2]

    for i in range(int(height)):
        for j in range(width):
            np_img[i][j] = random.randint(0, 255)

    img = Image.fromarray(np_img, mode='L')
    return img


def create_4_kb_image():
    img = Image.new('L', (63, 62))
    np_img = np.array(img)

    height, width = np_img.shape[:2]

    for i in range(int(height)):
        for j in range(width):
            np_img[i][j] = random.randint(0, 255)

    img = Image.fromarray(np_img, mode='L')
    return img


if __name__ == "__main__":
    create_4_kb_image().save('4_kb.png', 'PNG')
    create_16_kb_image().save('16_kb.png', 'PNG')
    create_64_kb_image().save('64_kb.png', 'PNG')
    pass
