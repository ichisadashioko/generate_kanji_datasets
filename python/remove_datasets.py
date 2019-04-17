# encoding=utf-8
from __future__ import print_function
import os
import time
import shutil

def remove_datasets(root_path):
    file_lists = os.listdir(root_path)

    avg_time = None

    for idx, f in enumerate(file_lists):
        file_path = f'{root_path}/{f}'
        print(f"{idx}/{len(file_lists)} Removing {file_path}")

        start_time = time.time()
        shutil.rmtree(file_path)
        end = time.time() - start_time

        if avg_time is None:
            avg_time = end
        else:
            avg_time = (avg_time + end) / 2

        est_time = (len(file_lists) - idx - 1) * avg_time

        est_str = time.strftime('%H:%M:%S', time.gmtime(est_time))

        print(f"{idx}/{len(file_lists)} {f} takes {end:.2f}s")
        print(f'AVG: {avg_time:.2f}s')
        print(f"Remaining time: {est_str}")

if __name__ == "__main__":
    dataset_root = 'E:/kanji_images'
    remove_datasets(dataset_root)
    