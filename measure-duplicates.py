import hashlib
import os
import shutil
from tqdm import tqdm

PATHS = ['../seeds/',
         '../seeds-uncenter/']
ENVS = ['bigfish', 'bossfight', 'caveflyer', 'chaser', 'climber', 'coinrun', 'dodgeball', 'fruitbot', 'heist', 'jumper',
        'leaper', 'maze', 'miner', 'ninja', 'plunder', 'starpilot']
DIFFS = ['easy', 'hard']
TQDM = False
SAVE_DUPES = 100  # How many overlapping images to save. 0 to disable


def compute_md5_hash(img_path):
    with open(img_path, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()


def count_overlaps(directory, first_x=100000, save_dupes=100):
    hashes_seen = set()

    # Sort image paths alphabetically
    img_paths = sorted([os.path.join(directory, img) for img in os.listdir(directory) if
                        img.lower().endswith(('.png', '.jpg', '.jpeg'))])

    if len(img_paths) != 200000:
        raise ValueError("Expected 200,000 images but found {}".format(len(img_paths)))

    first_half = img_paths[:first_x]
    second_half = img_paths[100000:]

    # Compute hashes for the first half
    for img_path in tqdm(first_half, disable=not TQDM):
        img_hash = compute_md5_hash(img_path)
        hashes_seen.add(img_hash)

    # Check overlaps in the second half
    overlaps = 0
    out_dir = os.path.join('../dupes', directory[3:])
    if save_dupes > 0:
        os.makedirs(out_dir, exist_ok=True)

    for img_path in tqdm(second_half, disable=not TQDM):
        img_hash = compute_md5_hash(img_path)
        if img_hash in hashes_seen:
            if overlaps < save_dupes:
                fname = img_path.split('/')[-1]
                out_path = os.path.join(out_dir, fname)
                shutil.copy(img_path, out_path)
            overlaps += 1

    return overlaps


if __name__ == "__main__":
    for PATH in PATHS:
        print(PATH)
        for first_x in [100000]:
        # for first_x in [1, 10, 100, 1000, 10000, 100000]:
            for DIFF in DIFFS:
                for ENV in ENVS:
                    directory = os.path.join(PATH, DIFF, ENV)
                    overlaps = count_overlaps(directory, first_x=first_x, save_dupes=SAVE_DUPES)
                    print(f"Overlapping images {DIFF}-{ENV}, {first_x} training levels: {overlaps/100000*100:.10f}%")
        print()
