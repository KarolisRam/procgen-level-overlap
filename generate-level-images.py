# Generate images of levels for all envs in each difficulty for each seed between 0 and 200000.
import gym
import matplotlib.pyplot as plt
import os
from tqdm import tqdm

CENTER = True
if CENTER:
    PATH = '../seeds/'
else:
    PATH = '../seeds-center/'
ENVS = ['bigfish', 'bossfight', 'caveflyer', 'chaser', 'climber', 'coinrun', 'dodgeball', 'fruitbot', 'heist', 'jumper',
        'leaper', 'maze', 'miner', 'ninja', 'plunder', 'starpilot']
DIFFS = ['easy', 'hard']


def main():
    for DIFF in DIFFS:
        for ENV in ENVS:
            os.makedirs(os.path.join(PATH, DIFF, ENV), exist_ok=True)
            for seed in tqdm(range(200000)):
                env = gym.make(f'procgen:procgen-{ENV}-v0', start_level=seed, num_levels=1, distribution_mode=DIFF,
                               center_agent=False)
                obs = env.reset()
                plt.imsave(os.path.join(PATH, DIFF, ENV, f'seed-{seed:08}.png'), obs)
                env.close()


if __name__ == '__main__':
    main()
