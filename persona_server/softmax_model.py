import math
import random
import arduino_distance
import numpy as np


# action selection based on Softmax probability
def categorical_draw(probs):
    z = random.random()
    cum_prob = 0.0

    for i in range(len(probs)):
        prob = probs[i]
        cum_prob += prob
        if cum_prob > z:
            return i
    return len(probs) - 1


# Softmax algorithm
class Softmax:
    def __init__(self, tau, counts, values):
        self.tau = tau
        self.counts = counts  # Count represent counts of pulls for each action. For multiple actions, this will be a list of counts.
        self.values = values  # Value represent average reward for specific action. For multiple actions, this will be a list of values.
        return

    # Initialise k number of actions
    def initialize(self, n_actions):
        self.counts = [0 for col in range(n_actions)]
        self.values = [0.0 for col in range(n_actions)]
        return

    def select_action(self):
        # Calculate Softmax probabilities based on each round
        z = sum([math.exp(v / self.tau) for v in self.values])
        probs = [math.exp(v / self.tau) / z for v in self.values]

        # Use categorical_draw to pick action
        return categorical_draw(probs)

    # Choose to update chosen action and reward
    def update(self, chosen_action, reward):
        # update counts pulled for chosen action
        self.counts[chosen_action] = self.counts[chosen_action] + 1
        n = self.counts[chosen_action]

        # Update average/mean value/reward for chosen action
        value = self.values[chosen_action]
        new_value = ((n - 1) / float(n)) * value + (1 / float(n)) * reward
        self.values[chosen_action] = new_value
        return

    def start_computation(self):
        # start running
        print("fix me")

    def get_results(self):
        return self.results

class Bernoulliaction():
    def __init__(self, p):
        self.p = p

    # Reward system based on Bernoulli
    def draw(self):
        if random.random() > self.p:
            return 0.0
        else:
            return 1.0


def test_algorithm(algo, actions, num_sims, horizon, port="/dev/tty.usbmodem1411"):
    # Initialise variables for duration of accumulated simulation (num_sims * horizon_per_simulation)
    chosen_actions = [0.0 for i in range(num_sims * horizon)]
    rewards = [0.0 for i in range(num_sims * horizon)]
    cumulative_rewards = [0 for i in range(num_sims * horizon)]
    sim_nums = [0.0 for i in range(num_sims * horizon)]
    times = [0.0 for i in range(num_sims * horizon)]

    for sim in range(num_sims):
        sim = sim + 1
        algo.initialize(len(actions))

        for t in range(horizon):
            t = t + 1
            index = (sim - 1) * horizon + t - 1
            sim_nums[index] = sim
            times[index] = t

            # Selection of best action and engaging it
            chosen_action = algo.select_action()
            chosen_actions[index] = chosen_action

            # HERE, SELECTION OF ACTIONS GENERATE A SET OF PARAMETERS FOR THE ASSOCIATED FACIAL EXPRESSION
            # REWARDS IS THE RESULT OF INPUT PARAMETERS, DISTANCE, EYE GAZE, FACIAL EXPRESSION
            # WITH ONLINE TRAINING, NO NEED FOR THE 2 BERNOUILLI LINES BELOW

            # Engage chosen Bernoulli action and obtain reward info
            dict_sensor_rewards = {'d40': 3, 'd75': 2, 'd150': 1, 'd200': 0, 'facing': 0, 'backing': 0, 'right': 1,
                                   'left': 1}
            list_sensors = ['d40', 'd75', 'd150', 'd200', 'facing', 'backing', 'right', 'left']
            # r = int(random.uniform(0, len(list_sensors)-1))
            reaction = arduino_distance.return_arduino_distance(port)
            reward = dict_sensor_rewards[reaction]
            # reward = actions[chosen_action].draw() # TO REPLACE WITH REWARDS FORMED OF TRANSLATED INPUTS (DISTANCE...)
            rewards[index] = reward

            # index of the simulation == 0+1 i.e. first trial
            if t == 1:
                cumulative_rewards[index] = reward
            else:
                cumulative_rewards[index] = cumulative_rewards[index - 1] + reward

            algo.update(chosen_action, reward)

    return [sim_nums, times, chosen_actions, rewards, cumulative_rewards]


def run_simulation():
    # AUTOMATIC SIMULATION #
    random.seed(1)
    # out of 5 actions, 1 action is clearly the best
    means = [0.1, 0.1, 0.1, 0.1, 0.1]
    n_actions = len(means)
    # Shuffling actions
    random.shuffle(means)
    # Create list of Bernoulli actions with Reward Information
    actions = list(map(lambda mu: Bernoulliaction(mu), means))
    print("Best action is " + str(np.argmax(means)))
    # f = open("standard_results_soft.tsv", "w+")
    # Create simulations for each tau/temperature value
    for tau in [0.05, 0.1, 0.2, 0.3, 0.4, 0.5]:
        algo = Softmax(tau, [], [])
        algo.initialize(n_actions)
        n_trials_per_sim = 10
        results = test_algorithm(algo, actions, 1, n_trials_per_sim)

        # Store data
        # len(results[0]) = 250 simulations, results[0] = nb of simulations so 1 as there is only 1 simulation here
        # with a horizon of 250 trials/times.
        last_trials_with_results = [n_trials_per_sim - 3, n_trials_per_sim - 2, n_trials_per_sim - 1]
        for i in last_trials_with_results:
            print("Best action is " + str(np.argmax(means)))
            print(str(tau) + "\t")
            print("\t".join([str(results[j][i]) for j in range(len(results))]) + "\n")
            # results = [sim_nums, times, chosen_arms, rewards, cumulative_rewards]

    """
        for i in range(len(results[0])) :
            f.write(str(epsilon) + "\t")
            f.write("\t".join([str(results[j][i]) for j in range(len(results))]) + "\n")
    f.close()
    """
    # END OF SIMULATION #


run_simulation()