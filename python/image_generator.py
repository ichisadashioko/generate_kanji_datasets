# encoding=utf-8
from __future__ import print_function
import os
import re
import time
import traceback

from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageChops

import numpy as np
import cv2
import matplotlib.pyplot as plt

# import configurations
from kanji_and_fonts import KANJI_LIST, FONT_DIRS, FONT_RATIOS


def normalize_filename(filename):
    return re.sub(r"[\\\/\.\#\%\$\!\@\(\)\[\]\s]+", "_", filename)


def pre_fetch_fonts(FONT_DIRS, FONT_RATIOS, IMAGE_SIZE=160):
    retval = []
    for font_dir in FONT_DIRS:
        font_files = os.listdir(font_dir)
        for font_file in font_files:
            # font_path = os.path.join(font_dir, font_file)
            font_path = f"{font_dir}/{font_file}"

            for r in FONT_RATIOS:
                font_size = int(r * IMAGE_SIZE)
                font = ImageFont.truetype(font_path, font_size)
                font_name = '_'.join(font.getname())
                font_dict = dict()
                font_dict['font'] = font
                font_dict['font_size'] = font_size
                font_dict['font_name'] = normalize_filename(font_name)

                retval.append(font_dict)

        #     break  # fonts loop
        # break  # FONT_DIRS loop

    return retval


def draw_kanji(kanji_text, font_dicts, save_dir, side_length=160, background_color=0, text_color=255, VERBOSE=0, overwrite=False, invalid_sample=None):

    draw_start = time.time()
    total_io_time = 0
    img_count = 0

    for font_dict in font_dicts:

        # create a image 2 times larger then the final image
        pad_side_length = int(side_length * 2)
        canvas = Image.new('L', (pad_side_length, pad_side_length), color=0)
        ctx = ImageDraw.Draw(canvas)
        font = font_dict['font']
        font_size = font_dict['font_size']
        font_name = font_dict['font_name']

        # find the offset to draw the image
        pad_offset = (pad_side_length - font_size) / 2
        ctx.text((pad_offset, pad_offset), kanji_text,
                 fill=text_color, font=font)

        # rotate the character
        for rotate_degree in range(-10, 15, 10):

            center_x = canvas.width / 2
            center_y = canvas.height / 2
            rotate_img = canvas.rotate(
                rotate_degree,
                center=(center_x, center_y)
            )

            np_img = np.array(rotate_img)
            kanji_idx = np_img.nonzero()

            # If the font does not support this character,
            # it will draw either none or a square
            # The try ... except block below is to deal with blank image
            try:
                max_x = kanji_idx[1][np.argmax(kanji_idx[1])]
                min_x = kanji_idx[1][np.argmin(kanji_idx[1])]

                max_y = kanji_idx[0][np.argmax(kanji_idx[0])]
                min_y = kanji_idx[0][np.argmin(kanji_idx[0])]
            except:
                break

            actual_width = max_x - min_x
            actual_height = max_y - min_y

            x_padding = (side_length - actual_width) / 2
            y_padding = (side_length - actual_height) / 2

            offset_x = min_x - x_padding
            offset_y = min_y - y_padding

            semi_final_img = rotate_img.crop((
                offset_x, offset_y, offset_x + side_length,
                offset_y + side_length
            ))

            if invalid_sample is not None:
                diff = ImageChops.difference(invalid_sample, semi_final_img)
                np_diff = np.array(diff)
                if np.sum(np_diff) < 255:
                    return

            base_img = np.array(semi_final_img)

            # transform vectors
            
            square_box_padding = min(x_padding, y_padding)

            x_transform_vectors = [0]
            y_transform_vectors = [0]

            STRIDE = side_length / 10

            idx = 1
            while True:
                t_vector = STRIDE * idx

                if (square_box_padding - t_vector) < 0:
                    break

                x_transform_vectors.append(t_vector)
                x_transform_vectors.append(-t_vector)
                y_transform_vectors.append(t_vector)
                y_transform_vectors.append(-t_vector)

                idx += 1

            for x_vector in x_transform_vectors:
                for y_vector in y_transform_vectors:

                    transform_matrix = np.float32([
                        [1, 0, x_vector],
                        [0, 1, y_vector]
                    ])

                    final_img = cv2.warpAffine(
                        base_img,
                        transform_matrix,
                        base_img.shape[:2]
                    )

                    # convert back to pillow image
                    final_img = Image.fromarray(final_img, 'L')

                    save_start = time.time()

                    # separate files by font to prevent large file directory
                    img_font_dir = f"{save_dir}/{font_name}"

                    if not os.path.exists(img_font_dir):
                        os.makedirs(img_font_dir)

                    base_filename = '_'.join([
                        kanji_text,
                        'size', str(font_size),
                        'rotate', str(rotate_degree),
                        'x', str(x_vector),
                        'y', str(y_vector),
                        # font_dict['font_name']
                    ])

                    base_filename = normalize_filename(base_filename)

                    filename = base_filename + '.png'
                    img_path = f"{img_font_dir}/{filename}"
                    if (not os.path.exists(img_path)) or overwrite:
                        final_img.save(img_path, 'PNG')

                        img_count += 1

                    inv_filename = 'inv_' + base_filename
                    inv_filename += '.png'
                    inv_path = f"{img_font_dir}/{inv_filename}"
                    if (not os.path.exists(inv_path)) or overwrite:
                        inv_img = ImageOps.invert(final_img)
                        inv_img.save(inv_path, 'PNG')

                        img_count += 1

                    save_time = time.time() - save_start
                    total_io_time += save_time

                # break  # x_vectors loop
            # break  # rotate loop
        # break  # fonts loop
        print('-', end='', flush=True)  # progress bar
    print()

    total_time = time.time() - draw_start

    io_ratio = total_io_time / total_time
    p_time = total_time - total_io_time

    print(f'{kanji_text} takes {total_time:.4f}s')
    print(f'PROCESSING_TIME={p_time:.4f}s {(1-io_ratio)*100:.2f}%')
    print(f'IO_TIME={total_io_time:.4f}s {io_ratio*100:.2f}%')
    print(f'AVG_IO_TIME={total_io_time/img_count:.4f}s')
    print(f'IMAGE_COUNT={img_count}')
    print('='*32)


def generate_datasets_pipeline(KANJI_LIST, font_dicts, side_length=160, save_dir='kanji_images', log_dir='kanji_images_log', overwrite=False, VERBOSE=0, invalid_sample=None):
    print(f"Creating images at {save_dir}")
    if VERBOSE < 2:
        start_time = time.time()
        avg_time = None

    for idx, kanji_text in enumerate(KANJI_LIST):
        if VERBOSE < 2:
            kanji_start = time.time()

        kanji_log = f"{log_dir}/{kanji_text}"
        kanji_dir = f"{save_dir}/{kanji_text}"

        if os.path.exists(kanji_log) and not overwrite:
            continue
        elif not os.path.exists(kanji_dir):
            os.makedirs(kanji_dir)

        try:
            draw_kanji(
                kanji_text=kanji_text,
                font_dicts=font_dicts,
                save_dir=kanji_dir,
                side_length=side_length,
                VERBOSE=VERBOSE,
                overwrite=overwrite,
                invalid_sample=invalid_sample,
            )
        except:
            print(f"Error at {kanji_text}!")
            traceback.print_exc()
            return

        if VERBOSE < 2:
            kanji_time = (time.time() - kanji_start)
            if avg_time is None:
                avg_time = kanji_time
            else:
                avg_time = (avg_time + kanji_time) / 2

            estime = avg_time * (len(KANJI_LIST) - idx - 1)
            est_str = time.strftime('%H:%M:%S', time.gmtime(estime))

            a_time = time.strftime(
                '%H:%M:%S', time.gmtime(time.time() - start_time))

            print(f"Active time: {a_time}")
            print(f"{kanji_text}: {idx+1}/{len(KANJI_LIST)} takes {kanji_time:.2f}s")
            print(f"AVG: {avg_time:.2f}s, Remaining time: {est_str}")

        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        open(kanji_log, 'w').close()
        break  # kanji loop


if __name__ == "__main__":

    # pre-fetch some IO tasks to improve performance
    invalid_sample = Image.open('invalid_image.png')
    font_dicts = pre_fetch_fonts(FONT_DIRS, FONT_RATIOS)

    generate_datasets_pipeline(
        KANJI_LIST[0:600],
        font_dicts=font_dicts,
        # overwrite=True,
        VERBOSE=1,
        invalid_sample=invalid_sample,
        save_dir='F:/kanji_images',
        log_dir='F:/kanji_images_log',
    )
