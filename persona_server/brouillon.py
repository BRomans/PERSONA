"""
def test_algorithm(algo, actions, num_sims, horizon, port="/dev/tty.usbmodem1411"):
    # Initialise variables for duration of accumulated simulation (num_sims * horizon_per_simulation)
    #chosen_actions = [0.0 for i in range(num_sims * horizon)]
    #rewards = [0.0 for i in range(num_sims * horizon)]
    #cumulative_rewards = [0 for i in range(num_sims * horizon)]
    #sim_nums = [0.0 for i in range(num_sims * horizon)]
    #times = [0.0 for i in range(num_sims * horizon)]

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
            reward = algo.get_reward() # or algo.reward ?
            rewards[index] = reward
            chosen_actions[index] = chosen_action
            # HERE, SELECTION OF ACTIONS GENERATE A SET OF PARAMETERS FOR THE ASSOCIATED FACIAL EXPRESSION
            # REWARDS IS THE RESULT OF INPUT PARAMETERS, DISTANCE, EYE GAZE, FACIAL EXPRESSION
            # WITH ONLINE TRAINING, NO NEED FOR THE 2 BERNOUILLI LINES BELOW
            # Engage chosen Bernoulli action and obtain reward info
            # index of the simulation == 0+1 i.e. first trial
            if t == 1:
                cumulative_rewards[index] = reward
            else:
                cumulative_rewards[index] = cumulative_rewards[index - 1] + reward # bc if algo.get_reward is called once more it might give a different reward
            algo.update(chosen_action, reward)
    return [sim_nums, times, chosen_actions, rewards, cumulative_rewards]
"""


"""
    def run_simulation():
        # AUTOMATIC SIMULATION #
        random.seed(1)
        # out of 5 actions, 1 action is clearly the best
        means = [0.1, 0.1, 0.1, 0.1, 0.1] # THIS IS ONLY USEFUL FOR AN AUTOMATIC SIMULATION
        n_actions = len(means) # REPLACE BY THE NUMBER OF POSSIBLE FACIAL EXPRESSIONS
        # Shuffling actions
        random.shuffle(means) # THIS IS ONLY USEFUL FOR AN AUTOMATIC SIMULATION
        # Create list of Bernoulli actions with Reward Information
        actions = list(map(lambda mu: Bernoulliaction(mu), means)) # THIS IS ONLY USEFUL FOR AN AUTOMATIC SIMULATION
        # f = open("standard_results_soft.tsv", "w+")
        # Create simulations for each tau/temperature value
        for tau in [0.05, 0.1, 0.2, 0.3, 0.4, 0.5]:
            algo = Softmax(tau, [], [])
            algo.initialize(n_actions)
            n_trials_per_sim = 10 # INCREASE THE NUMBER OF SIMULATIONS
            results = (algo, [], [], [], [])
            # results[0] = nb of simulations so 1 as there is only 1 simulation here
            # with a horizon of n_trials_per_sim trials.
            last_trials_with_results = [n_trials_per_sim - 3, n_trials_per_sim - 2, n_trials_per_sim - 1]
            for i in last_trials_with_results:
                print("Best action is " + str(np.argmax(means)))
                print(str(tau) + "\t")
                print("\t".join([str(results[j][i]) for j in range(len(results))]) + "\n")
                # results = [sim_nums, times, chosen_arms, rewards, cumulative_rewards]
        # END OF SIMULATION #

run_simulation()
"""