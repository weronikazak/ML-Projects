import numpy as np
from PIL import Image
import cv2
import matplotlib.pyplot as plt
import pickle
from matplotlib import style
import time

style.use('ggplot')











# ---------------------
# VARIABLES
# ---------------------












SIZE = 20

EPISODES = 50000

MOVE_PENALTY = 1
ENEMY_PENALTY = 300
FOOD_REWARD = 25
epsilon = 1.0
EPS_DECAY = 0.9998
SHOW_EVERY = 5000

start_q_table = None

LEARNING_RATE = 0.1
DISCOUNT = 0.95

PLAYER_N = 1 # player key in dict
FOOD_N = 2 # food key in dict
ENEMY_N = 3 # enemy key in dict

# the dict of colours
d = {
    1: (255, 175, 0), # blue
    2: (0, 255, 0), # green
    3: (0, 0, 255) # red
}










# ---------------------------
# MAKE CLASS OF CHARACTERS
# ---------------------------












class Squares:
    def __init__(self):
        self.x = np.random.randint(0, SIZE)
        self.y = np.random.randint(0, SIZE)
    
    # debugging purposes
    def __str__(self):
        return f"{self.x}, {self.y}"

    # substractiong two squares from each other
    def __sub__(self, other):
        return (self.x - other.x, self.y - other.y)

    def action(self, choice):
        # movement options: (0, 1, 2, 3)

        if choice == 0:
            self.move(x=1, y=1)
        elif choice == 1:
            self.move(x=-1, y=-1)
        elif choice == 2:
            self.move(x=-1, y=1)
        elif choice == 3:
            self.move(x=1, y=-1)

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
        elif self.x > SIZE - 1:
            self.x = SIZE-1
        if self.y < 0:
            self.y = 0
        elif self.y > SIZE-1:
            self.y = SIZE-1


"""

player = Squares()
food = Squares()
enemy = Squares()

print(player)
print(food)
print(player - food)
print(enemy)
player.move()
print(player - food)
player.action(2)
print(player - food)
"""












# ------------------------------
# MAKING OR READING Q_TABLE
# ------------------------------









if start_q_table is None:
    # init q_table
    q_table = {}
    for i in range(-SIZE+1,SIZE):
        for ii in range(-SIZE+1, SIZE):
            for iii in range(-SIZE+1, SIZE):
                for iiii in range(-SIZE+1, SIZE):
                    q_table[((i, ii), (iii, iiii))] = [np.random.uniform(-5, 0) for i in range(4)]
else:
    with open(start_q_table, "rb") as f:
        q_table = pickle.load(f)



# print(q_table[((-9, 2), (3, 9))])







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