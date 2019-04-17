import os
import time
import shutil

from PIL import Image

from create_images_for_benchmark import *

if __name__ == "__main__":
    img = create_4_kb_image()

    root_path = 'f:/test_fs'
    test_num = 8 * 1000

    write_test_start = time.time()
    for i in range(test_num):
        sub_dir_idx = int(i / 1000)
        sub_dir = f'{root_path}/{sub_dir_idx}'

        if not os.path.exists(sub_dir):
            os.makedirs(sub_dir)

        img_path = f'{sub_dir}/{i}.png'

        img.save(img_path, 'PNG')

    write_test_time = time.time() - write_test_start
    avg_time = write_test_time/test_num
    print(f"WRITE_TEST_END: {write_test_time:.8f}s")
    print(f'IMG_NUM: {test_num}')
    print(f'AVG: {avg_time:.8f}s')

    est_time = avg_time * (10**6)
    est_time_str = time.strftime('%H:%M:%S', time.gmtime(est_time))
    print(f'ESTIMATE FOR 1 million files: {est_time_str}')
    print('='*32)

    delete_test_start = time.time()
    shutil.rmtree(root_path)
    delete_test_time = time.time() - delete_test_start
    print(f"DELETE_TEST_END: {delete_test_time:.8f}s")
    print(f'IMG_NUM: {test_num}')
    print(f'AVG: {delete_test_time/test_num:.8f}s')
    print('='*32)