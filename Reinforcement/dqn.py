import numpy as np
from PIL import Image
import cv2
import matplotlib.pyplot as plt
import pickle
from matplotlib import style
import time
import tensorflow
from tensorflow import keras
from keras import layers as ly
from collections import deque
import random

style.use('ggplot')


# ---------------------
# VARIABLES
# ---------------------






LEARNING_RATE = 0.1
DISCOUNT = 0.95
epsilon = 1.0
EPS_DECAY = 0.9998
SHOW_EVERY = 5000






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







class BlobEnv:
    SIZE = 10
    RETURN_IMAGES = True

    MOVE_PENALTY = 1
    ENEMY_PENALTY = 300
    FOOD_REWARD = 25
    ACTION_SPACE_SIZE = 9
    OBSERVATION_SPACE_VALUES = (SIZE, SIZE, 3)

    PLAYER_N = 1 # player key in dict
    FOOD_N = 2 # food key in dict
    ENEMY_N = 3 # enemy key in dict

    # the dict of colours
    d = {
        1: (255, 175, 0), # blue
        2: (0, 255, 0), # green
        3: (0, 0, 255) # red
    }

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









# ------------------------------
# MAKING DQN
# ------------------------------






REPLAY_MEMORY_SIZE = 50_000 # how many last steps to keep for model training
MIN_REPLAY_MEMORY_SIZE = 1_000 # minimum number of steps in a memory to start training
MINIBATCH_SIZE = 64  # how many steps to use for training
UPDATE_TARGET_EVERY = 5





class DQNAgent:
    def __init__(self):
        self.model = self.create_model()

        self.target_model = self.create_model()
        self.target_model.set_weights(self.model.get_weights())

        self.replay_memory = deque(maxlen=REPLAY_MEMORY_SIZE)

        # self.tensorboard = ModifiedTensorBoard(logdir=f'logs/{MODEL_NAME}-{int(time.time())}')

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
        current_q_list = self.model.predict(current_state)

        X, y = [], []

        # enumerating batches
        for index, (current_state, action, reward, new_current_state, done) in enumerate(minibatch):


















# ----------------------------
# RUN EPISODES
# ----------------------------




episode_rewards = []
for episode in range(EPISODES):
    player = Squares()
    food = Squares()
    enemy = Squares()

    if episode % SHOW_EVERY == 0:
        print(f'on episode {episode}, epsilon is {epsilon}')
        print(f'{SHOW_EVERY} ep. mean: {np.mean(episode_rewards[-SHOW_EVERY:])}')
        show = True
    else:
        show = False

    episode_reward = 0

    for i in range(200):
        obs = (player-food, player-enemy)

        if np.random.random() > epsilon:
            action = np.argmax(q_table[obs])
        else:
            action = np.random.randint(0, 4)
        
        player.action(action)

        enemy.move()
        food.move()


        # --------------
        # REWARDS
        # --------------


        if player.x == enemy.x and player.y == enemy.y:
            reward = (-ENEMY_PENALTY)
        elif player.x == food.x and player.y == food.y:
            reward = FOOD_REWARD
        else:
            reward = -MOVE_PENALTY

        new_obc = (player-food, player-enemy)
        max_futuer_q = np.max(q_table[new_obc])
        current_q = q_table[obs][action]

        if reward == FOOD_REWARD:
            new_q = FOOD_REWARD
        else:
            new_q = (1 - LEARNING_RATE) * current_q + LEARNING_RATE * \
                (reward + DISCOUNT * max_futuer_q)

        q_table[obs][action] = new_q

        if show:
            time.sleep(0.01)
            # black background
            env = np.zeros((SIZE, SIZE, 3), dtype=np.uint8) 

            # green food
            env[food.x][food.y] = d[FOOD_N]

            # blue player
            env[player.x][player.y] = d[PLAYER_N]

            # red enemy
            env[enemy.x][enemy.y] = d[ENEMY_N]

            img = Image.fromarray(env, 'RGB')
            img = img.resize((400, 400))
            cv2.imshow('game', np.array(img))

            if reward == FOOD_REWARD or reward == (-ENEMY_PENALTY):
                if cv2.waitKey(200) & 0xFF == ord('q'):
                    break
            else:
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

        episode_reward += reward
        if reward == FOOD_REWARD or reward == (-ENEMY_PENALTY):
            break
        
    # print(episode_reward)
    episode_rewards.append(episode_reward)
    epsilon *= EPS_DECAY
    
moving_avg = np.convolve(episode_rewards, np.ones((SHOW_EVERY,))/SHOW_EVERY, mode='valid')

plt.plot([i for i in range(len(moving_avg))], moving_avg)
plt.ylabel(f'Reward {SHOW_EVERY}ma')
plt.xlabel('episode #')
plt.show()

with open(f'q_table-{int(time.time())}.pickle', 'wb') as f:
    pickle.dump(q_table, f)