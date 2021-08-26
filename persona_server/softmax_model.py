import math
import random
import arduino_distance
import numpy as np


# Softmax algorithm
class Softmax:
    def __init__(self, tau, counts, values, reward, action, possible_actions, probs):
        self.tau = tau
        self.counts = counts  # Count represent counts of pulls for each action. For multiple actions, this will be a list of counts.
        self.values = values  # Value represent average reward for specific action. For multiple actions, this will be a list of values.
        self.reward = reward  # Value representing reward for a chosen action
        self.action = action  # Value representing a chosen facial expression
        self.possible_actions = possible_actions
        self.probs = probs
        return

    # Initialise k number of actions
    def initialize(self, n_actions):
        self.counts = [0 for col in range(n_actions)]
        self.values = [0.0 for col in range(n_actions)]
        self.reward = 0
        self.action = 0
        self.possible_actions = [i for i in range(n_actions)]
        self.probs = [1/n_actions for i in range(n_actions)]
        return

    # action selection based on Softmax probability
    def categorical_draw(self, probs):
        z = random.random()
        cum_prob = 0.0
        for i in range(len(probs)):
            prob = probs[i]
            cum_prob += prob
            if cum_prob > z:
                return i
        return len(probs) - 1

    def select_action(self):
        # Calculate Softmax probabilities based on each round
        z = sum([math.exp(v / self.tau) for v in self.values])
        self.probs = [math.exp(v / self.tau) / z for v in self.values]
        # Use categorical_draw to pick action
        self.action = self.categorical_draw(self.probs)
        return self.action

    def get_reward(self, port="/dev/tty.usbmodem1411"):
        dict_sensor_rewards = {'d40' : 3, 'd75' : 2, 'd150' : 1, 'd200' : 0, 'facing' : 0, 'backing' : 0,
                               'right' : 1, 'left' : 1}
        list_sensors = ['d40', 'd75', 'd150', 'd200', 'facing', 'backing', 'right', 'left']
        # r = int(random.uniform(0, len(list_sensors)-1))
        reaction = arduino_distance.return_arduino_distance(port)
        self.reward = dict_sensor_rewards[reaction]
        return self.reward
        # reward = actions[chosen_action].draw()

    # Choose to update chosen action and reward
    def update(self, chosen_action, reward):  # self.reward ? self.action or chosen action ?
        # update counts pulled for chosen action
        self.counts[chosen_action] = self.counts[chosen_action] + 1
        n = self.counts[chosen_action]
        # Update average/mean value/reward for chosen action
        value = self.values[chosen_action]
        #print("value =", value)
        #print(reward)
        new_value = ((n - 1) / float(n)) * value + (1 / float(n)) * reward
        self.values[chosen_action] = new_value
        return

    def get_results(self):
        return self.action

    def set_tau(self, new_tau):
        self.tau = new_tau


class Bernoulliaction():
    def __init__(self, p):
        self.p = p

    # Reward system based on Bernoulli
    def draw(self):
        if random.random() > self.p:
            return 0.0
        else:
            return 1.0


class Algo_trials:
    def __init__(self, algo, chosen_actions, rewards, times, cumulative_rewards,  sim_nums, num_sims = 1, horizon = 6, port="/dev/tty.usbmodem1411"):
        self.algo = algo
        self.num_sims = num_sims
        self.horizon = horizon
        self.chosen_actions = [0 for i in range(self.num_sims * self.horizon)]
        self.rewards = [0.0 for i in range(self.num_sims * self.horizon)]
        self.port = port
        self.cumulative_rewards = [0.0 for i in range(self.num_sims * self.horizon)]
        self.times = [0.0 for i in range(self.num_sims * self.horizon)]
        self.sim_nums = [0.0 for i in range(self.num_sims * self.horizon)]
        self.times = [0.0 for i in range(self.num_sims * self.horizon)]

    def initialize(self):
        self.num_sims = 1
        self.chosen_actions = [0 for i in range(self.num_sims * self.horizon)]
        self.rewards = [0.0 for i in range(self.num_sims * self.horizon)]
        self.cumulative_rewards = [0.0 for i in range(self.num_sims * self.horizon)]
        self.times = [0.0 for i in range(self.num_sims * self.horizon)]
        self.sim_nums = [0.0 for i in range(self.num_sims * self.horizon)]
        return

    def performing_trials(self):
        for sim in range(self.num_sims):
            sim = sim + 1
            #print("horizon =", self.horizon)
            #print("num_sims =", self.num_sims)
            #print("len sim_nums =", len(self.sim_nums), self.sim_nums)
            self.algo.initialize(len(self.algo.possible_actions))


            for t in range(self.horizon):
                t = t + 1
                index = (sim - 1) * self.horizon + t - 1
                # print("sim =", sim, "index = ", index, "len sim_nums =", len(self.sim_nums))
                self.sim_nums[index] = sim
                self.times[index] = t

                # Selection of best action and engaging it
                chosen_action = self.algo.select_action()
                reward = self.algo.get_reward()  # or algo.reward ?
                # print("reward =", reward)
                self.rewards[index] = reward
                self.cumulative_rewards[index] += reward
                self.chosen_actions[index] = chosen_action
                # HERE, SELECTION OF ACTIONS GENERATE A SET OF PARAMETERS FOR THE ASSOCIATED FACIAL EXPRESSION
                # REWARDS IS THE RESULT OF INPUT PARAMETERS, DISTANCE, EYE GAZE, FACIAL EXPRESSION
                # WITH ONLINE TRAINING, NO NEED FOR THE 2 BERNOUILLI LINES BELOW
                # Engage chosen Bernoulli action and obtain reward info
                # index of the simulation == 0+1 i.e. first trial
                if t == 1 :
                    self.cumulative_rewards[index] = reward
                else :
                    self.cumulative_rewards[index] = self.cumulative_rewards[index - 1] + reward  # bc if algo.get_reward is called once more it might give a different reward
                self.algo.update(chosen_action, reward)
        return self.sim_nums, self.times, self.chosen_actions, self.rewards, self.cumulative_rewards


class Simulation_run:
    def __init__(self):
        self.dict_tau_properties = {}
        return

    def initialize(self):
        self.dict_tau_properties = {}
        return

    def run_simulation(self):
        # AUTOMATIC SIMULATION #
        random.seed(1)
        # out of 5 actions, 1 action is clearly the best
        means = [0.1, 0.1, 0.1, 0.2, 0.1] # THIS IS ONLY USEFUL FOR AN AUTOMATIC SIMULATION
        n_actions = len(means) # REPLACE BY THE NUMBER OF POSSIBLE FACIAL EXPRESSIONS
        # Shuffling actions
        random.shuffle(means) # THIS IS ONLY USEFUL FOR AN AUTOMATIC SIMULATION
        # Create list of Bernoulli actions with Reward Information
        actions = list(map(lambda mu: Bernoulliaction(mu), means)) # THIS IS ONLY USEFUL FOR AN AUTOMATIC SIMULATION
        # f = open("standard_results_soft.tsv", "w+")
        # Create simulations for each tau/temperature value
        for tau in [0.05, 0.1, 0.2, 0.3, 0.4, 0.5]:
            algo = Softmax(tau, [], [], 0, 0, [], [])
            algo.initialize(n_actions)
            trials = Algo_trials(algo, [], [], [], [], [])
            results = trials.performing_trials()
            # results[0] = nb of simulations so 1 as there is only 1 simulation here
            # with a horizon of n_trials_per_sim trials.
            last_trials_with_results = [trials.horizon - 3, trials.horizon - 2, trials.horizon - 1]
            for i in last_trials_with_results:
                print("Best action is " + str(np.argmax(means)))
                print(str(tau) + "\t")
                print("\t".join([str(results[j][i]) for j in range(len(results))]) + "\n")
                # results = [sim_nums, times, chosen_arms, rewards, cumulative_rewards]
            self.dict_tau_properties[tau] = [algo.probs, trials.cumulative_rewards]
        return self.dict_tau_properties

if __name__ == '__main__':
    sim = Simulation_run()
    dic = sim.run_simulation()
    print("dict_tau_properties =", dic)