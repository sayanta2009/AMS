"""
Author: Sayanta Roychowdhury
Matriculation No: 03709791
"""
from counter import TimeIndependentCounter
from simulation import Simulation
from matplotlib import pyplot
import numpy as np
import matplotlib
matplotlib.rcParams['figure.figsize'] = (10, 30)

"""
This file should be used to keep all necessary code that is used for the simulation section in part 5
of the programming assignment. It contains tasks 5.2.1, 5.2.2, 5.2.3 and 5.2.4.
"""


def task_5_2_1():
    """
    Run task 5.2.1. Make multiple runs until the blocking probability distribution reaches
    a confidence level alpha. Simulation is performed for 100s and 1000s and for alpha = 90% and 95%.
    """
    results = [None, None, None, None]
    # TODO Task 5.2.1: Your code goes here
    conf_level = .0015
    sim = Simulation()
    sim.sim_param.RHO = 0.9
    sim.sim_param.S = 4
    i = 0
    tic = TimeIndependentCounter()

    for sim_time in [100000, 1000000]:
        sim.sim_param.SIM_TIME = sim_time
        for alpha in [0.1, 0.05]:
            tic.reset()
            count = 0
            check = False
            while not check:
                sim.reset()
                sim_result = sim.do_simulation()
                tic.count(sim_result.blocking_probability)
                count += 1
                if tic.report_confidence_interval(alpha) < conf_level:
                    check = True

            results[i] = count
            i += 1

    # print and return results
    print "SIM TIME:  100s; ALPHA: 10%; NUMBER OF RUNS: " + str(results[0]) + "; TOTAL SIMULATION TIME (SECONDS): " + str(results[0]*100)
    print "SIM TIME:  100s; ALPHA:  5%; NUMBER OF RUNS: " + str(results[1]) + "; TOTAL SIMULATION TIME (SECONDS): " + str(results[1]*100)
    print "SIM TIME: 1000s; ALPHA: 10%; NUMBER OF RUNS:  " + str(results[2]) + "; TOTAL SIMULATION TIME (SECONDS): " + str(results[2]*1000)
    print "SIM TIME: 1000s; ALPHA:  5%; NUMBER OF RUNS:  " + str(results[3]) + "; TOTAL SIMULATION TIME (SECONDS): " + str(results[3]*1000)
    return results


def task_5_2_2():
    """
    Run simulation in batches. Start the simulation with running until a customer count of n=100 or (n=1000) and
    continue to increase the number of customers by dn=n.
    Count the blocking proabability for the batch and calculate the confidence interval width of all values, that have
    been counted until now.
    Do this until the desired confidence level is reached and print out the simulation time as well as the number of
    batches.
    """
    results = [None, None, None, None]
    # TODO Task 5.2.2: Your code goes here
    conf_level = .0015
    sim = Simulation()
    sim.sim_param.RHO = 0.9
    sim.sim_param.S = 4
    i = 0
    tic = TimeIndependentCounter()

    for batch_size in [100, 1000]:
        for alpha in [0.1, 0.05]:
            tic.reset()
            check = False
            new_batch = False
            sim.reset()
            while not check:
                sim_result = sim.do_simulation_n_limit(batch_size, new_batch)
                tic.count(sim_result.blocking_probability)
                if len(tic.values) > 5 and tic.report_confidence_interval(alpha) < conf_level:
                    check = True
                else:
                    sim.sim_state.num_blocked_packets = 0
                    sim.sim_state.num_packets = 0
                    sim.sim_state.stop = False
                    sim.counter_collection.reset()
                    new_batch = True

            results[i] = sim.sim_state.now
            i += 1

    # print and return results
    print "BATCH SIZE:  100; ALPHA: 10%; TOTAL SIMULATION TIME (SECONDS): " + str(results[0]/1000)
    print "BATCH SIZE:  100; ALPHA:  5%; TOTAL SIMULATION TIME (SECONDS): " + str(results[1]/1000)
    print "BATCH SIZE: 1000; ALPHA: 10%; TOTAL SIMULATION TIME (SECONDS): " + str(results[2]/1000)
    print "BATCH SIZE: 1000; ALPHA:  5%; TOTAL SIMULATION TIME (SECONDS): " + str(results[3]/1000)
    return results


def task_5_2_4():
    """
    Plot confidence interval as described in the task description for task 5.2.4.
    We use the function plot_confidence() for the actual plotting and run our simulation several times to get the
    samples. Due to the different configurations, we receive eight plots in two figures.
    """
    # TODO Task 5.2.4: Your code goes here
    sim = Simulation()
    sim.sim_param.S = 10000
    tic_sys_util = TimeIndependentCounter()
    i = 1
    pyplot.subplots_adjust(hspace=0.6)
    for rho in [.5, .9]:
        sim.sim_param.RHO = rho
        sim.reset()
        for alpha in [.1, .05]:
            for sim_time in [100000, 1000000]:
                sim.sim_param.SIM_TIME = sim_time
                upper_bounds = []
                lower_bounds = []
                means = []

                for _ in range(100):
                    tic_sys_util.reset()
                    for _ in range(30):
                        sim.reset()
                        sim_result = sim.do_simulation()
                        tic_sys_util.count(sim_result.system_utilization)
                    conf_interval = tic_sys_util.report_confidence_interval(alpha)
                    sample_mean = tic_sys_util.get_mean()
                    lower_bounds.append(sample_mean - conf_interval)
                    upper_bounds.append(sample_mean + conf_interval)
                    means.append(sample_mean)

                pyplot.subplot(4, 2, i)
                plot_confidence(sim, range(1, 101),
                                lower_bounds, upper_bounds, np.mean(means), rho, "Sys Util", alpha)
                i += 1
    pyplot.show()


def plot_confidence(sim, x, y_min, y_max, calc_mean, act_mean, ylabel, alpha):
    """
    Plot confidence levels in batches. Inputs are given as follows:
    :param sim: simulation, the measurement object belongs to.
    :param x: defines the batch ids (should be an array).
    :param y_min: defines the corresponding lower bound of the confidence interval.
    :param y_max: defines the corresponding upper bound of the confidence interval.
    :param calc_mean: is the mean calculated from the samples.
    :param act_mean: is the analytic mean (calculated from the simulation parameters).
    :param ylabel: is the y-label of the plot
    :return:
    """
    # TODO Task 5.2.3: Your code goes here
    """
    Note: You can change the input parameters, if you prefer to.
    """
    pyplot.ylabel(ylabel)
    pyplot.xlabel("Batches")
    pyplot.hlines(act_mean, 0, len(x) - 1, colors='black', linestyles='dashed', label='Actual Mean (RHO)')
    pyplot.hlines(calc_mean, 0, len(x) - 1, colors='red', linestyles='dashed', label='Sample Mean')
    pyplot.vlines(x, y_min, y_max, colors='green', linestyles='solid')
    pyplot.xlim([1, 100])
    pyplot.title("SIM_TIME: " + str(sim.sim_param.SIM_TIME) + "ms ALPHA= " + str(alpha) + " RHO:" + str(act_mean))
    pyplot.legend(loc='lower right')


if __name__ == '__main__':
    # task_5_2_1()
    #task_5_2_2()
    task_5_2_4()