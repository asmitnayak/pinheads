import random
import cv2
import gym
from matplotlib import pyplot as plt
from tqdm import tqdm


def preprocess(env: gym.Env):
    first_frame = None
    env.reset()
    # y_lim, x_lim, channels = env.observation_space
    y_lim = 210
    x_lim = 160
    xs = []
    ys = []
    for i in tqdm(range(1000)):
        frame = env.render(mode='rgb_array')
        if i == 0 or i == 1:
            plt.imshow(frame)
            plt.show()
        # action = random.choice([0, 1, 2, 3, 4, 5, 6, 7, 8])
        action = random.choice([3, 4])
        n_state, reward, done, info = env.step(action)
        greyscale_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gaussian_frame = cv2.GaussianBlur(greyscale_frame, (21, 21), 0)
        blur_frame = cv2.blur(gaussian_frame, (5, 5))
        greyscale_image = blur_frame
        if i == 0 or i == 1:
            plt.imshow(greyscale_frame)
            plt.show()
            plt.imshow(gaussian_frame)
            plt.show()
            plt.imshow(blur_frame)
            plt.show()
        if first_frame is None:
            first_frame = greyscale_image
        else:
            pass
        frame_delta = cv2.absdiff(first_frame, greyscale_image)
        if i == 1:
            plt.imshow(frame_delta)
            plt.show()
        thresh = cv2.threshold(frame_delta, 30, 255, cv2.THRESH_BINARY)[1]
        if i == 1:
            plt.imshow(thresh)
            plt.show()
        dilate_image = cv2.dilate(thresh, None, iterations=2)
        if i == 1:
            plt.imshow(dilate_image)
            plt.show()
        contours = cv2.findContours(dilate_image.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
        if contours is not None:
            for c in contours:
                if cv2.contourArea(c) > 10:
                    (x, y, w, h) = cv2.boundingRect(c)
                    xs.append(x)
                    xs.append(x + w)
                    ys.append(y)
                    ys.append(y + h)
                else:
                    pass
    env.close()
    y_start = max([min(xs) - int(0.1 * x_lim), 0])
    y_end = min([max(xs) + int(0.1 * x_lim), x_lim])
    x_start = max([min(ys) - int(0.1 * y_lim), 0])
    x_end = max([max(ys) + int(0.1 * y_lim), y_lim])

    return x_start, x_end, y_start, y_end
