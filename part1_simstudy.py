"""
Author: Sayanta Roychowdhury
Matriculation No: 03709791
"""
from simparam import SimParam
from simulation import Simulation
import random

"""
This file should be used to keep all necessary code that is used for the simulation study in part 1 of the programming
assignment. It contains the tasks 1.7.1, 1.7.2 and 1.7.3.

The function do_simulation_study() should be used to run the simulation routine, that is described in the assignment.
"""

def task_1_7_1():
    """
    Execute task 1.7.1 and perform a simulation study according to the task assignment.
    :return: Minimum number of buffer spaces to meet requirements.
    """
    sim_param = SimParam()
    random.seed(sim_param.SEED)
    sim = Simulation(sim_param)
    return do_simulation_study(sim)


def task_1_7_2():
    """
    Execute task 1.7.2 and perform a simulation study according to the task assignment.
    :return: Minimum number of buffer spaces to meet requirements.
    """
    sim_param = SimParam()
    random.seed(sim_param.SEED)
    sim_param.SIM_TIME = 1000000
    sim_param.MAX_DROPPED = 100
    sim_param.NO_OF_RUNS = 100
    sim = Simulation(sim_param)
    return do_simulation_study(sim)

def task_1_7_3():
    """
    Execute task 1.7.3.
    """
    # TODO Task 1.7.3: Your code goes here (if necessary)
    pass


def do_simulation_study(sim):
    """
    Implement according to task description.3
    """
    # TODO Task 1.7.1: Your code goes here
    check = True

    while check:
        success = 0
        for x in range(sim.sim_param.NO_OF_RUNS):  # 1000
            sim.reset()
            if sim.do_simulation().packets_dropped < sim.sim_param.MAX_DROPPED:  # 10
                success += 1
        if float(success)/float(sim.sim_param.NO_OF_RUNS) >= .8:
            check = False
        if float(success)/float(sim.sim_param.NO_OF_RUNS) < .8:
            check = True
            sim.sim_param.S += 1

    for i in range(1, 6):
        success = 0
        for x in range(sim.sim_param.NO_OF_RUNS):  # 1000
            sim.reset()
            if sim.do_simulation().packets_dropped < sim.sim_param.MAX_DROPPED:  # 10
                success += 1

        print "Success Rate: "+str(float(success)/float(sim.sim_param.NO_OF_RUNS))
        print "Buffer Size: "+str(sim.sim_param.S)

    return sim.sim_param.S


if __name__ == '__main__':
    #task_1_7_1()
    task_1_7_2()
    #task_1_7_3()

