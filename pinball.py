import gym
import random
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten, Convolution2D
from tensorflow.keras.optimizers import Adam
from stable_baselines3 import PPO
from Pinball_bot import PinBallBot
import pydirectinput
import pyautogui
import pygetwindow as gw

env = gym.make('VideoPinball-v0', difficulty=1)
height, width, channels = env.observation_space.shape
actions = env.action_space.n

unwrapped = env.env.unwrapped

env.unwrapped.get_action_meanings()

episodes = 1
p = None
for episode in range(1, episodes + 1):
    state = env.reset()
    done = False
    score = 0
    rendered = None
    while not done:
        env.render()
        rendered = env.env.viewer.window
        rendered = gw.getWindowsWithTitle(rendered.caption)
        rendered = rendered[len(rendered) - 1]
        if p is None:
            p = PinBallBot(rendered)
            p.main()

        action = random.choice([0, 1, 2, 3, 4, 5])
        n_state, reward, done, info = env.step(action)
        score += reward
    print('Episode:{} Score:{}'.format(episode, score))
env.close()
