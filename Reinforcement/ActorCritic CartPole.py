import tensorflow as tf
import gym
import numpy as np
import matplotlib.pyplot as plt
import tqdm 


class Actor(tf.keras.models.Model):
	'''
	Actor Class: 
	Model to select an action given a state,
	
	Input :
	-> num_actions: int, number of actions in the environment
	-> num_hidden: int, number of units in the hidden layer
		
	Output:
	->action_probs: tf.Tensor,  softmax output of the actions that can be taken

	'''

	def __init__(
		self, 
		num_actions: int, 
		num_hidden: int):


		
		super(Actor, self).__init__()
		
		self.inp = tf.keras.layers.Dense(64, activation='relu')

		self.hidden1 = tf.keras.layers.Dense(num_hidden, activation='relu')

		self.out = tf.keras.layers.Dense(num_actions, activation='softmax')


	def call(
		self,
	    state: tf.Tensor ) -> tf.Tensor:


		x = self.inp(state)
		x = self.hidden1(x)
		action_probs = self.out(x)

		return action_probs



class Critic(tf.keras.models.Model):
	'''
	Critic Class: 
	Model to predict the values given a state,
	
	Input :
	-> num_hidden: int, number of units in the hidden layer
		
	Output: 
	->value: tf.Tensor,  the predicted value of that state

	'''
	def __init__(
		self, 
		num_hidden: int):


		super(Critic, self).__init__()
		
		self.inp = tf.keras.layers.Dense(num_hidden)
		self.hidden1 = tf.keras.layers.Dense(num_hidden, activation='relu')
		self.out = tf.keras.layers.Dense(1)

	def call(
		self, 
		state: tf.Tensor )-> tf.Tensor:


		x = self.inp(state)
		x = self.hidden1(x)
		value = self.out(x)
		return value




class gym_wrap:
	'''
	class gym_wrap:
	Wrap the gym environment so that it returns Tensors instead of 
	numpy ndarrays
	'''
	def __init__(self, env):
		self.env = env

	def reset(self):
		state = self.env.reset()
		state = tf.constant(state, dtype=tf.float32)
		state = tf.expand_dims(state, 0)
		return state

	def step(self, action):
		action = np.max(action)
		def temp_step(action):
			state, reward, done, _ = self.env.step(action)
			state = np.reshape(state, (1, -1))
			return (
				state.astype(np.float32),
				np.array(reward, np.int32),
				np.array(done, np.int32)
				)

		return tf.numpy_function(
			temp_step,
			[action],
			[tf.float32, tf.int32, tf.int32]
			)


def play_episode(
	actor: Actor,
	critic: Critic,
	env: gym_wrap,
    max_steps: int):


	actions_logits = tf.TensorArray(dtype=tf.float32, size=0, dynamic_size=True)
	rewards_per_timestep = tf.TensorArray(dtype=tf.int32, size=0, dynamic_size=True)
	value_preds = tf.TensorArray(dtype=tf.float32, size=0, dynamic_size=True)

	state = env.reset()

	for t in tf.range(max_steps):

		action_probs = actor(state)
		predicted_value = critic(state)

		action_to_perform = tf.random.categorical(action_probs, 1)
		actions_prob = action_probs[0, action_to_perform[0, 0]]

		actions_logits = actions_logits.write(t, actions_prob)
		value_preds = value_preds.write(t, tf.squeeze(predicted_value))

		state, reward, done = env.step(action_to_perform)

		rewards_per_timestep = rewards_per_timestep.write(t, reward)

		if tf.cast(done, tf.bool):
			break

	actions_logits = actions_logits.stack()
	rewards_per_timestep = rewards_per_timestep.stack()
	value_preds = value_preds.stack()

	return (actions_logits, rewards_per_timestep, value_preds)



def get_returns(
	gamma: float,
	rewards: tf.Tensor):

	# Reverse the rewards to calculate the returns 
	rewards = tf.cast(rewards[::-1], tf.float32)
	n = rewards.shape[0]

	returns = tf.TensorArray(dtype=tf.float32, size=n)
	G = tf.constant(0.0)

	for i in tf.range(n):
		G = rewards[i] + gamma * G

		returns = returns.write(i, G)

	# Reverse the returns to get the proper order
	returns = returns.stack()[::-1]

	return returns


def get_loss(
	action_logits: tf.Tensor,
	value_preds: tf.Tensor,
	returns: tf.Tensor ):


	advantage = returns - value_preds

	log_a = tf.math.log(action_logits)
	actor_loss = -tf.math.reduce_sum(log_a * advantage)

	critic_loss = huberloss(value_preds, returns)

	return actor_loss, critic_loss


def train_step(
	actor: Actor,
	critic: Critic,
	env: gym_wrap,
	max_steps,
	gamma ):

	with tf.GradientTape(persistent=True) as tape:
		a_logits, rewards, v_preds = play_episode(actor, critic, env, max_steps)
		returns = get_returns(gamma, rewards)
		(aloss, closs) = get_loss(a_logits, v_preds, returns)

	a_grads = tape.gradient(aloss, actor.trainable_variables)
	c_grads = tape.gradient(closs, critic.trainable_variables)

	optimizer.apply_gradients(zip(a_grads, actor.trainable_variables))
	optimizer.apply_gradients(zip(c_grads, critic.trainable_variables))

	episode_reward = tf.math.reduce_sum(rewards)
	del tape
	return episode_reward

if __name__=='__main__':

	env= gym.make("CartPole-v0")
	gamma = 0.99
	num_actions = env.action_space.n
	num_hidden = 128
	env = gym_wrap(env)

	actor = Actor(num_actions, num_hidden)
	critic = Critic(num_hidden)

	optimizer = tf.keras.optimizers.Adam(learning_rate=0.01)
	huberloss = tf.keras.losses.Huber(reduction=tf.keras.losses.Reduction.SUM)

	episodes = 500
	for i in range(episodes):
		reward = train_step(actor, critic, env, 200, gamma)
		if i%50==0:
			print(f"Episode reward = {reward}: Episode = {i}")

	print("Done")

