"""
Author: Sayanta Roychowdhury
Matriculation No: 03709791
"""
from counter import TimeIndependentAutocorrelationCounter
from simulation import Simulation
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams['figure.figsize'] = (10, 30)

"""
This file should be used to keep all necessary code that is used for the verification and simulation section in part 4
of the programming assignment. It contains tasks 4.2.1, 4.3.1 and 4.3.2.
"""


def task_4_2_1():
    """
    Execute exercise 4.2.1, which is basically just a test for the auto correlation.
    """
    # TODO Task 4.2.1: Your code goes here
    counter = TimeIndependentAutocorrelationCounter(name="Demo Auto Correlation Counter", max_lag=4)
    for i in range(1000):
        if i % 2 == 0:
            counter.count(1)
        else:
            counter.count(-1)
    print "---First sequence----"
    counter.report()

    counter.reset()
    for i in range(1000):
        counter.count(1)
        counter.count(1)
        counter.count(-1)

    print "---Second sequence----"
    counter.report()


def task_4_3_1():
    """
    Run the correlation tests for given rho for all correlation counters in counter collection.
    After each simulation, print report results.
    SIM_TIME is set higher in order to avoid a large influence of startup effects
    """
    # TODO Task 4.3.1: Your code goes here
    sim = Simulation()
    sim.sim_param.S = 10000
    sim.sim_param.SIM_TIME = 10000000

    for rho in [0.01, 0.5, 0.8, 0.95]:
        print"--------Simulation with Rho:" + str(rho) + "--------"
        sim.sim_param.RHO = rho
        sim.reset()
        sim.do_simulation()
        sim.counter_collection.report()


def task_4_3_2():
    """
    Exercise to plot the scatter plot of (a) IAT and serving time, (b) serving time and system time
    The scatter plot helps to better understand the meaning of bit/small covariance/correlation.
    For every rho, two scatter plots are needed.
    The simulation parameters are the same as in task_4_3_1()
    """
    # TODO Task 4.3.2: Your code goes here
    sim = Simulation()
    counter_one = sim.counter_collection.cnt_iat_st
    counter_two = sim.counter_collection.cnt_st_syst
    sim.sim_param.S = 10000
    sim.sim_param.SIM_TIME = 10000000

    sim.sim_param.RHO = 0.01
    sim.do_simulation()
    plt.subplots_adjust(hspace=0.6)

    plt.subplot(4, 2, 1)
    plt.plot(counter_one.valueX.get_values(), counter_one.valueY.get_values(), 'o')
    plt.title("RHO: 0.01 -- IAT VS Service Time")

    plt.subplot(4, 2, 2)
    plt.plot(counter_two.valueX.get_values(), counter_two.valueY.get_values(), 'o')
    plt.title("RHO: 0.01 -- Service Time VS System Time")

    sim.reset()
    counter_one = sim.counter_collection.cnt_iat_st
    counter_two = sim.counter_collection.cnt_st_syst
    sim.sim_param.RHO = 0.5
    sim.do_simulation()

    plt.subplot(4, 2, 3)
    plt.plot(counter_one.valueX.get_values(), counter_one.valueY.get_values(), 'o')
    plt.title("RHO: 0.5 -- IAT VS Service Time")

    plt.subplot(4, 2, 4)
    plt.plot(counter_two.valueX.get_values(), counter_two.valueY.get_values(), 'o')
    plt.title("RHO: 0.5 -- Service Time VS System Time")

    sim.reset()
    counter_one = sim.counter_collection.cnt_iat_st
    counter_two = sim.counter_collection.cnt_st_syst
    sim.sim_param.RHO = 0.8
    sim.do_simulation()

    plt.subplot(4, 2, 5)
    plt.plot(counter_one.valueX.get_values(), counter_one.valueY.get_values(), 'o')
    plt.title("RHO: 0.8 -- IAT VS Service Time")

    plt.subplot(4, 2, 6)
    plt.plot(counter_two.valueX.get_values(), counter_two.valueY.get_values(), 'o')
    plt.title("RHO: 0.8 -- Service Time VS System Time")

    sim.reset()
    counter_one = sim.counter_collection.cnt_iat_st
    counter_two = sim.counter_collection.cnt_st_syst
    sim.sim_param.RHO = 0.95
    sim.do_simulation()

    plt.subplot(4, 2, 7)
    plt.plot(counter_one.valueX.get_values(), counter_one.valueY.get_values(), 'o')
    plt.title("RHO: 0.95 -- IAT VS Service Time")

    plt.subplot(4, 2, 8)
    plt.plot(counter_two.valueX.get_values(), counter_two.valueY.get_values(), 'o')
    plt.title("RHO: 0.95 -- Service Time VS System Time")

    plt.show()


def task_4_3_3():
    """
    Exercise to plot auto correlation depending on lags. Run simulation until 10000 (or 100) packets are served.
    For the different rho values, simulation is run and the waiting time is auto correlated.
    Results are plotted for each N value in a different diagram.
    Note, that for some seeds with rho=0.01 and N=100, the variance of the auto covariance is 0 and returns an error.
    """
    # TODO Task 4.3.3: Your code goes here
    sim = Simulation()
    sim.sim_param.S = 10000
    run_simulation(sim, 100, 1)
    run_simulation(sim, 10000, 2)
    plt.show()


def run_simulation(sim, n, plot_section):
    for rho in [0.01, 0.5, 0.8, 0.95]:
        sim.sim_param.RHO = rho
        sim.reset()
        sim.do_simulation_n_limit(100)

        aut_cor_list = []
        lag_list = range(1, 21)

        for lag in lag_list:
            aut_cor_list.append(sim.counter_collection.acnt_wt.get_auto_cor(lag))

        plt.subplot(2, 1, plot_section)
        plt.plot(lag_list, aut_cor_list, label="Rho: " + str(rho))

    title = "Auto-correlation vs Lag size :: For " + str(n) + " simulation runs"
    plt.title(title)
    plt.xlabel("Lag")
    plt.ylabel("Auto-correlation")
    plt.legend(loc='upper right')


if __name__ == '__main__':
    #task_4_2_1()
    # task_4_3_1()
    # task_4_3_2()
    task_4_3_3()