import os
import hashlib
from collections import deque
from tqdm import tqdm
import matplotlib.pyplot as plt


def compute_md5_hash(img_path):
    with open(img_path, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()


def process_images(directory):
    hashes_seen = set()
    running_avg = []
    last_1000 = deque(maxlen=1000)

    # Sort image paths alphabetically
    img_paths = sorted([os.path.join(directory, img) for img in os.listdir(directory) if
                        img.lower().endswith(('.png', '.jpg', '.jpeg'))])

    for img_path in tqdm(img_paths):
        img_hash = compute_md5_hash(img_path)

        # If duplicate, append 1 else 0
        if img_hash in hashes_seen:
            print(img_path)
            return
            last_1000.append(1)
        else:
            last_1000.append(0)
            hashes_seen.add(img_hash)

        # Compute running average and store
        running_avg.append(sum(last_1000) / len(last_1000))

    return running_avg


def plot_data(data):
    plt.plot(data)
    plt.xlabel("Image Number")
    plt.ylabel("Running Average of Duplicates (Last 1000)")
    plt.title("Running Average of Duplicates Among Images")
    plt.show()


if __name__ == "__main__":
    directory = "/home/karolis/k/procgen-level-overlap/seeds/maze"
    running_avg = process_images(directory)
    plot_data(running_avg)
