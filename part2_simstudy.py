import random
from simparam import SimParam
from simulation import Simulation
from matplotlib import pyplot

from counter import TimeIndependentCounter
from histogram import TimeIndependentHistogram

"""
This file should be used to keep all necessary code that is used for the simulation study in part 2 of the programming
assignment. It contains the tasks 2.7.1 and 2.7.2.

The function do_simulation_study() should be used to run the simulation routine, that is described in the assignment.
"""
sim_param = SimParam()
random.seed(sim_param.SEED)
sim = Simulation(sim_param)
ql_count = TimeIndependentCounter()
ql_hist = TimeIndependentHistogram(sim, "q")

wt_count = TimeIndependentCounter()
wt_hist = TimeIndependentHistogram(sim, "w")


def task_2_7_1():
    """
    Here, you should execute task 2.7.1 (and 2.7.2, if you want).
    """
    # TODO Task 2.7.1: Your code goes here
    return do_simulation_study(sim)


def task_2_7_2():
    """
    Here, you can execute task 2.7.2 if you want to execute it in a separate function
    """
    # TODO Task 2.7.2: Your code goes here or in the function above
    for x in range(sim.sim_param.NO_OF_RUNS):
        sim.reset()
        sim.do_simulation()
        ql_count.count(sim.counter_collection.cnt_ql.get_mean())
        wt_count.count(sim.counter_collection.cnt_wt.get_mean())
        ql_hist.count(sim.counter_collection.cnt_ql.get_mean())
        wt_hist.count(sim.counter_collection.cnt_wt.get_mean())


def do_simulation_study(sim, print_queue_length=False, print_waiting_time=True):
    """
    This simulation study is different from the one made in assignment 1. It is mainly used to gather and visualize
    statistics for different buffer sizes S instead of finding a minimal number of spaces for a desired quality.
    For every buffer size S (which ranges from 5 to 7), statistics are printed (depending on the input parameters).
    Finally, after all runs, the results are plotted in order to visualize the differences and giving the ability
    to compare them. The simulations are run first for 100s, then for 1000s. For each simulation time, two diagrams are
    shown: one for the distribution of the mean waiting times and one for the average buffer usage
    :param sim: the simulation object to do the simulation
    :param print_queue_length: print the statistics for the queue length to the console
    :param print_waiting_time: print the statistics for the waiting time to the console
    """
    # TODO Task 2.7.1: Your code goes here
    # TODO Task 2.7.2: Your code goes here

    for S in sim.sim_param.S_VALUES:
        sim.sim_param.S = S
        task_2_7_2()

        pyplot.subplot(221)
        pyplot.xlabel("Mean queue length for Simulation Time 100ms")
        pyplot.ylabel("Histogram")
        pyplot.xlim([0, 10])
        ql_hist.report()

        pyplot.subplot(222)
        pyplot.xlabel("Mean waiting time for Simulation Time 100ms")
        pyplot.ylabel("Histogram")
        pyplot.xlim([0, 5000])
        wt_hist.report()

        ql_count.reset()
        ql_hist.reset()
        wt_count.reset()
        wt_hist.reset()

        sim.sim_param.SIM_TIME = 1000000

        task_2_7_2()

        pyplot.subplot(223)
        pyplot.xlabel("Mean queue length for Simulation Time 1000ms")
        pyplot.ylabel("Histogram")
        pyplot.xlim([0, 10])
        ql_hist.report()

        pyplot.subplot(224)
        pyplot.xlabel("Mean waiting time for Simulation Time 1000ms")
        pyplot.ylabel("Histogram")
        pyplot.xlim([0, 5000])
        wt_hist.report()

    pyplot.show()


if __name__ == '__main__':
    task_2_7_1()