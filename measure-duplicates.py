import os
import hashlib

PATH = '/home/karolis/k/procgen-level-overlap/seeds/'
# PATH = '/home/karolis/k/procgen-level-overlap/seeds-center/'
ENVS = ['bigfish', 'bossfight', 'caveflyer', 'chaser', 'climber', 'coinrun', 'dodgeball', 'fruitbot', 'heist', 'jumper',
        'leaper', 'maze', 'miner', 'ninja', 'plunder', 'starpilot']
DIFFS = ['easy', 'hard']


def compute_md5_hash(img_path):
    with open(img_path, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()


def count_overlaps(directory, first_x=100000):
    hashes_seen = set()

    # Sort image paths alphabetically
    img_paths = sorted([os.path.join(directory, img) for img in os.listdir(directory) if
                        img.lower().endswith(('.png', '.jpg', '.jpeg'))])

    if len(img_paths) != 200000:
        raise ValueError("Expected 200,000 images but found {}".format(len(img_paths)))

    first_half = img_paths[:first_x]
    second_half = img_paths[100000:]

    # Compute hashes for the first half
    for img_path in first_half:
        img_hash = compute_md5_hash(img_path)
        hashes_seen.add(img_hash)

    # Check overlaps in the second half
    overlaps = 0
    for img_path in second_half:
        img_hash = compute_md5_hash(img_path)
        if img_hash in hashes_seen:
            overlaps += 1

    return overlaps


if __name__ == "__main__":
    for DIFF in DIFFS:
        for ENV in ENVS:
            # for first_x in [1, 10, 100, 1000, 10000, 100000]:
            for first_x in [100000]:
                directory = os.path.join(PATH, DIFF, ENV)
                overlaps = count_overlaps(directory, first_x=first_x)
                print(f"Overlapping images {DIFF}-{ENV}, {first_x} training levels: {overlaps/100000*100:.2f}%")
