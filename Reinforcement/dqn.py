import numpy as np
from PIL import Image
import cv2
import matplotlib.pyplot as plt
import pickle
from matplotlib import style
import time
import tensorflow as tf
from tensorflow import keras
from keras import layers as ly
from collections import deque
from tqdm import tqdm
import random
import os



style.use('ggplot')


# ---------------------
# VARIABLES
# ---------------------




SHOW_PREVIEW = False

LEARNING_RATE = 0.1
DISCOUNT = 0.95

epsilon = 1.0
EPS_DECAY = 0.99975
MIN_EPSILON = 0.001

SHOW_EVERY = 5000
EPISODES = 20_000

MEMORY_FRACTION = 0.2
REPLAY_MEMORY_SIZE = 50_000 # how many last steps to keep for model training
MIN_REPLAY_MEMORY_SIZE = 1_000 # minimum number of steps in a memory to start training
MINIBATCH_SIZE = 64  # how many steps to use for training
UPDATE_TARGET_EVERY = 5

MODEL_NAME = '2x256'
MIN_REWARD = -200


AGGREGATE_STATS_EVERY = 50



# ---------------------------
# MAKE CLASS OF CHARACTERS
# ---------------------------






class Squares:
    def __init__(self, size):
        self.size = size
        self.x = np.random.randint(0, size)
        self.y = np.random.randint(0, size)
    
    # debugging purposes
    def __str__(self):
        return f"Blob ({self.x}, {self.y})"

    # substractiong two squares from each other
    def __sub__(self, other):
        return (self.x - other.x, self.y - other.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def action(self, choice):
        # movement options: (0, 1, 2, 3, 4, 5, 6, 7, 8)

        if choice == 0:
            self.move(x=1, y=1)
        elif choice == 1:
            self.move(x=-1, y=-1)
        elif choice == 2:
            self.move(x=-1, y=1)
        elif choice == 3:
            self.move(x=1, y=-1)

        elif choice == 4:
            self.move(x=1, y=0)
        elif choice == 5:
            self.move(x=-1, y=0)
        
        elif choice == 6:
            self.move(x=0, y=1)
        elif choice == 7:
            self.move(x=0, y=-1)
        
        elif choice == 8:
            self.move(x=0, y=0)


    def move(self, x=False, y=False):
        # if no value for x, move randomly

        if not x:
            self.x += np.random.randint(-1, 2)
        else: self.x += x

        # if no value for y, move randomly
        if not y:
            self.y += np.random.randint(-1, 2)
        else:
            self.y += y

        
        # if out of bonds, fix
        if self.x < 0:
            self.x = 0
        elif self.x > self.size - 1:
            self.x = self.size-1
        if self.y < 0:
            self.y = 0
        elif self.y > self.size-1:
            self.y = self.size-1







class SquaresEnv:
    SIZE = 10
    RETURN_IMAGES = True
    MOVE_PENALTY = 1
    ENEMY_PENALTY = 300
    FOOD_REWARD = 25
    OBSERVATION_SPACE_VALUES = (SIZE, SIZE, 3)
    ACTION_SPACE_SIZE = 9
    PLAYER_N = 1
    FOOD_N = 2
    ENEMY_N = 3

    d = {1: (255, 175, 0),
         2: (0, 255, 0),
         3: (0, 0, 255)}


    def reset(self):
        self.player = Squares(self.SIZE)
        self.food = Squares(self.SIZE)
        while self.food == self.player:
            self.food = Squares(self.SIZE)

        self.enemy = Squares(self.SIZE)
        while self.enemy == self.player or self.enemy == self.food:
            self.enemy = Squares(self.SIZE)

        self.episode_step = 0

        if self.RETURN_IMAGES:
            observation = np.array(self.get_image())
        else:
            observation = (self.player - self.food) + (self.player - self.enemy)
        return observation

    def step(self, action):
        self.episode_step += 1
        self.player.action(action)


        # enemy.move()
        # food.move()


        if self.RETURN_IMAGES:
            new_observation = np.array(self.get_image())
        else:
            new_observation = (self.player - self.food) + (self.player - self.enemy)

        
        if self.player == self.enemy:
            reward = -self.ENEMY_PENALTY
        elif self.player == self.food:
            reward = self.FOOD_REWARD
        else:
            reward = -self.MOVE_PENALTY

        done = False
        if reward == self.FOOD_REWARD or reward == -self.ENEMY_PENALTY or self.episode_step >=200:
            done = True

        return new_observation, reward, done

    def render(self):
        img = self.get_image()
        img = img.resize((300, 300))
        cv2.imshow('image', np.array(img))
        cv2.waitKey(1)

    # FOR CNN
    def get_image(self):
        env = np.zeros((self.SIZE, self.SIZE, 3), dtype=np.uint8)
        env[self.player.x][self.player.y] = self.d[self.PLAYER_N]
        env[self.food.x][self.food.y] = self.d[self.FOOD_N]
        env[self.enemy.x][self.enemy.y] = self.d[self.ENEMY_N]
        img = Image.fromarray(env, 'RGB')
        return img









# --------------------------
# TENSORBOARD CLASS
# --------------------------


# Own Tensorboard class
class ModifiedTensorBoard(TensorBoard):

    # Overriding init to set initial step and writer (we want one log file for all .fit() calls)
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.step = 1
        self.writer = tf.summary.FileWriter(self.log_dir)

    # Overriding this method to stop creating default log writer
    def set_model(self, model):
        pass

    # Overrided, saves logs with our step number
    # (otherwise every .fit() will start writing from 0th step)
    def on_epoch_end(self, epoch, logs=None):
        self.update_stats(**logs)

    # Overrided
    # We train for one batch only, no need to save anything at epoch end
    def on_batch_end(self, batch, logs=None):
        pass

    # Overrided, so won't close writer
    def on_train_end(self, _):
        pass

    # Custom method for saving own metrics
    # Creates writer, writes custom metrics and closes writer
    def update_stats(self, **stats):
        self._write_logs(stats, self.step)












# ------------------------------
# MAKING DQN
# ------------------------------








class DQNAgent:
    def __init__(self):
        self.model = self.create_model()

        self.target_model = self.create_model()
        self.target_model.set_weights(self.model.get_weights())

        self.replay_memory = deque(maxlen=REPLAY_MEMORY_SIZE)

        self.tensorboard = ModifiedTensorBoard(logdir=f'logs/{MODEL_NAME}-{int(time.time())}')

        self.target_update_counter = 0

    def create_model(self):
        model = keras.models.Sequential()

        model.add(ly.Conv2D(256, (3, 3), input_shape=env.shape))
        model.add(ly.Activation('relu'))
        model.add(ly.MaxPooling2D(pool_size=(2,2)))
        model.add(ly.Dropout(0.2))

        model.add(ly.Conv2D(256, (3, 3)))
        model.add(ly.Activation('relu'))
        model.add(ly.MaxPooling2D(pool_size=(2,2)))
        model.add(ly.Dropout(0.2))

        model.add(ly.Flatten())
        model.add(ly.Dense(64))

        # ACTION_SPACE_SIZE = how_many_choices (9)
        model.add(ly.Dense(env.ACTION_SPACE_SIZE, activation='linear')) 
        model.compile(loss='mse', optimizer='adam', metrics=['accuracy'])
        return model

    def update_replay_memory(self, transition):
        self.replay_memory.append(transition)

    def get_qs(self, state, step):
        return self.model.predict(np.array(state).reshape(-1, *state.shape)/255)[0]

    def train(self, terminal_state, step):
        if len(self.replay_memory) < MIN_REPLAY_MEMORY_SIZE:
            return

        # get a minibatch of rndom samples from memory table
        minibatch = random.sample(self.replay_memory, MINIBATCH_SIZE)

        # get future states from minibatch, then query NN model for Q values
        # when using target networdk, query it, otherwise main network should be queried
        current_state = np.array([transition[0] for transition in minibatch])/255
        current_qs_list = self.model.predict(current_state)

        new_current_state = np.array([transition[0] for transition in minibatch])/255
        future_qs_list = self.model.predict(new_current_state)


        X, y = [], []

        # enumerating batches
        for index, (current_state, action, reward, new_current_state, done) in enumerate(minibatch):
            if not done:
                max_future_q = np.max(future_qs_list[index])
                new_q = reward + DISCOUNT * max_future_q
            else:
                new_q = reward

            # update q value for given state
            current_qs = current_qs_list[index]
            current_qs[action] = new_q

            # appending to trainnig data
            X.append(current_state)
            y.append(current_qs)

        self.model.fit(np.array(X)/255, np.array(y), batch_size=MINIBATCH_SIZE,
                        verbose=0, shuffle=False, callbacks=[self.tensorboard] if terminal_state else None)

        # update target network counter every episode
        if terminal_state:
            self.target_update_counter += 1

        if self.target_update_counter > UPDATE_TARGET_EVERY:
            self.target_model.set_weights(self.model.get_weights())
            self.target_update_counter = 0

    def get_qs(self, state):
        return self.model.predict(np.array(state).reshape(-1, *state.shape)/255)[0]











# ----------------------------
# RUN EPISODES
# ----------------------------







env = SquaresEnv()

ep_rewards = [-200]

random.seed(1)
np.random.seed(1)
tf.set_random_seed(1)

if not os.path.isdir('models'):
    os.makedirs('models')


agent = DQNAgent()

for episode in tqdm(range(1, EPISODES + 1), ascii=True, unit='episodes'):

    # update tensorboard step every episode
    agent.tensorboard.step = episode

    # restarting episode
    episode_reward = 0
    step = 1

    # reset environment and get initial state
    current_state = env.reset()

    done = False

    while not done:
        if np.random.random() > epsilon:
            action = np.argmax(agent.get_qs(current_state))
        else:
            action = np.random.randint(0, env.ACTION_SPACE_SIZE)

    new_state, reward, done = env.step(action)
    episode_reward += reward

    if SHOW_PREVIEW and not episode % AGGREGATE_STATS_EVERY:
        env.render()

    agent.update_replay_memory((current_state, action, reward, new_state, done))
    agent.train(done, step)

    current_state = new_state
    step += 1

    ep_rewards.append(episode_reward)
    if not episode % AGGREGATE_STATS_EVERY or episode == 1:
        average_reward = sum(ep_rewards[-AGGREGATE_STATS_EVERY:])/len(ep_rewards[-AGGREGATE_STATS_EVERY:])
        min_reward = min(ep_rewards[-AGGREGATE_STATS_EVERY:])
        max_reward = max(ep_rewards[-AGGREGATE_STATS_EVERY:])
        agent.tensorboard.update_stats(reward_avg=average_reward, reward_min=min_reward, reward_max=max_reward, epsilon=epsilon)

        # save model, but oonly when reward is greater or equal a set value
        if min_reward >= MIN_REWARD:
            agent.model.save(f'models/{MODEL_NAME}__{max_reward:_>7.2f}max_{average_reward:_>7.2f}avg_{min_reward:_>7.2f}min__{int(time.time())}.model')
        
    if epsilon > MIN_EPSILON:
        epsilon *= EPS_DECAY
        epsilon = max(MIN_EPSILON, epsilon)