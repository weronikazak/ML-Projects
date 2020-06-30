import gym
import universe

env = gym.make('flashgames.NeonRace-v0')
env.configure(remotes=1)

observation_n = env.reset()

while True:
	action_n = [[("KeyEvent", "ArrowUp", True)] for ob in observation_n]
	observation_n, reward_n, done_n, inf = env.step(action_n)
	# observatin - observations of the env
	# reward_n   - +1/ -1, depending whether the action was beneficial
	# done_n     - game over? yes/no
	# info       - addiction info, performance and latency, not important

	env.render()

	
