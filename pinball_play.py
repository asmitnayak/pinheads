import gym
import random
import matplotlib.pyplot as plt
import numpy as np
from stable_baselines3 import PPO
from Pinball_bot import PinBallBot
from math import inf
# from stable_baselines3.common.env_util import make_atari_env
from stable_baselines3.common.vec_env import VecFrameStack
from stable_baselines3 import A2C
from my_env_util import make_my_atari_env


class BoxToBoxWrapper(gym.ObservationWrapper):
    def __init__(self, env):
        env.reward_range = (-inf, inf)
        super().__init__(env)

        # plt.imshow(self.observation_space.high[:, :, 0], cmap='gray')
        # plt.savefig("image_test.png", dpi=300)

        high = np.array(self.observation_space.high)    # [150:210, 60:100, :]
        low = np.array(self.observation_space.low)      # [150:210, 60:100, :]
        self.observation_space = gym.spaces.Box(low, high, high.shape)

    def observation(self, obs):
        new_obs = obs[150:210, 60:100, :]
        return new_obs


env = make_my_atari_env('VideoPinball-v0', seed=0)
env.reset()
model = A2C('CnnPolicy', env, verbose=1)
print(env.observation_space.shape)
# env = make_atari_env('VideoPinball-v0', seed=0)
