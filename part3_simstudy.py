"""
Author: Sayanta Roychowdhury
Matriculation No: 03709791
"""
from matplotlib import pyplot
from rng import ExponentialRNS, UniformRNS
import numpy
from simulation import Simulation
"""
This file should be used to keep all necessary code that is used for the verification section in part 3 of the
programming assignment. It contains tasks 3.2.1 and 3.2.2.
"""


def task_3_2_1():
    """
    This function plots two histograms for verification of the random distributions.
    One histogram is plotted for a uniform distribution, the other one for an exponential distribution.
    """
    # TODO Task 3.2.1: Your code goes here
    no_of_runs = 1000
    rns_exp = ExponentialRNS(5.0)
    rns_uni = UniformRNS(1, 300)
    exponential_values = []
    uniform_values = []
    weight = numpy.full(no_of_runs, 1.0 / float(no_of_runs))

    while no_of_runs != 0:
        exponential_values.append(rns_exp.next())
        uniform_values.append(rns_uni.next())
        no_of_runs -= 1

    pyplot.subplot(121)
    pyplot.title("Uniform Distribution")
    pyplot.xlabel("x")
    pyplot.ylabel("Distribution")
    pyplot.hist(uniform_values, bins=25, weights=weight)
    pyplot.subplot(122)
    pyplot.title("Exponential distribution for Lambda = 5")
    pyplot.xlabel("x")
    pyplot.ylabel("Distribution")
    pyplot.hist(exponential_values, bins=25, weights=weight)
    pyplot.show()


def task_3_2_2():
    """
    Here, we execute task 3.2.2 and print the results to the console.
    The first result string keeps the results for 100s, the second one for 1000s simulation time.
    """
    # TODO Task 3.2.2: Your code goes here
    simulation = Simulation()
    generate_sys_util(simulation)
    simulation.sim_param.SIM_TIME = 1000000
    generate_sys_util(simulation)


def generate_sys_util(simulation):
    rho_values = [0.01, 0.5, 0.8, 0.9]
    for x in rho_values:
        simulation.sim_param.RHO = x
        simulation.reset()
        simulation.do_simulation()
        print "For Simulation Time = %d secs and RHO = %f, System Utilization = %f" \
              % (simulation.sim_param.SIM_TIME, simulation.sim_param.RHO, simulation.sim_result.system_utilization)


if __name__ == '__main__':
    task_3_2_2()
    # task_3_2_2()