import gymnasium as gym
import numpy as np

# Env init
env = gym.make("ALE/Boxing-v5", render_mode='human')
observation, info = env.reset()

# Q-Learning Parameters
learning_rate = 0.1
discount_rate = 0.99
exploration_rate = 1
max_exploration_rate = 1
min_exploration_rate = 0.01
exploration_decay_rate = 0.001

# Q-Table Parameters
x_states = 160
y_states = 210
n_actions = env.action_space.n
q_table = np.zeros((x_states * y_states, n_actions))

# Training Parameters
total_epochs = 100
max_steps_per_epoch = 2500

# Q-Learning Algorithm
for epoch in range(total_epochs):
    print('Epoch:', epoch)
    state, _ = env.reset()
    done = False
    step = 0

    while step < max_steps_per_epoch and not done:
        # Exploration-Exploitation Trade-Off
        exploration_rate_threshold = np.random.uniform(0, 1)

        if exploration_rate_threshold > exploration_rate:
            action = np.argmax(q_table[state, :])
        else:
            action = env.action_space.sample()

        # Take action
        new_state, reward, done, _, info = env.step(action)

        # Update Q-Table
        q_table[state, action] = q_table[state, action] + learning_rate * \
            (reward + discount_rate *
             np.max(q_table[new_state, :]) - q_table[state, action])

        # Transition to next state
        state = new_state

        # Increment step count
        step += 1

    # Exploration rate decay
    exploration_rate = min_exploration_rate + \
        (max_exploration_rate - min_exploration_rate) * \
        np.exp(-exploration_decay_rate * epoch)

env.close()
