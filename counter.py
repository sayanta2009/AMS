"""
Author: Sayanta Roychowdhury
Matriculation No: 03709791
"""
import math
import numpy
from collections import deque
import scipy
import scipy.stats


class Counter(object):

    """
    Counter class is an abstract class, that counts values for statistics.

    Values are added to the internal array. The class is able to generate mean value, variance and standard deviation.
    The report function prints a string with name of the counter, mean value and variance.
    All other methods have to be implemented in subclasses.
    """

    def __init__(self, name="default"):
        """
        Initialize a counter with a name.
        The name is only for better distinction between counters.
        :param name: identifier for better distinction between various counters
        """
        self.name = name
        self.values = []

    def count(self, *args):
        """
        Count values and add them to the internal array.
        Abstract method - implement in subclass.
        """
        raise NotImplementedError("Please Implement this method")

    def reset(self, *args):
        """
        Delete all values stored in internal array.
        """
        self.values = []

    def get_mean(self):
        """
        Returns the mean value of the internal array.
        Abstract method - implemented in subclass.
        """
        raise NotImplementedError("Please Implement this method")

    def get_var(self):
        """
        Returns the variance of the internal array.
        Abstract method - implemented in subclass.
        """
        raise NotImplementedError("Please Implement this method")

    def get_stddev(self):
        """
        Returns the standard deviation of the internal array.
        Abstract method - implemented in subclass.
        """
        raise NotImplementedError("Please Implement this method")

    def report(self):
        """
        Print report for this counter.
        """
        if len(self.values) != 0:
            print "Name: " + str(self.name) + ", Mean: " + str(self.get_mean()) + ", Variance: " + str(self.get_var())
        else:
            print("List for creating report is empty. Please check.")


class TimeIndependentCounter(Counter):

    """
    Counter for counting values independent of their duration.

    As an extension, the class can report a confidence interval and check if a value lies within this interval.
    """

    def __init__(self, name="default"):
        """
        Initialize the TIC object.
        """
        super(TimeIndependentCounter, self).__init__(name)

    def count(self, *args):
        """
        Add a new value to the internal array. Parameters are chosen as *args because of the inheritance to the
        correlation counters.
        :param: *args is the value that should be added to the internal array
        """
        self.values.append(args[0])

    def reset(self):
        self.values = []

    def get_mean(self):
        """
        Return the mean value of the internal array.
        """
        # TODO Task 2.3.1: Your code goes here
        return numpy.mean(self.values)

    def get_var(self):
        """
        Return the variance of the internal array.
        Note, that we take the estimated variance, not the exact variance.
        """
        # TODO Task 2.3.1: Your code goes here
        return numpy.var(self.values, ddof=1)

    def get_stddev(self):
        """
        Return the standard deviation of the internal array.
        """
        # TODO Task 2.3.1: Your code goes here
        return numpy.std(self.values, ddof=1)

    def get_values(self):
        return self.values

    def report_confidence_interval(self, alpha=0.05, print_report=True):
        """
        Report a confidence interval with given significance level.
        This is done by using the t-table provided by scipy.
        :param alpha: is the significance level (default: 5%)
        :param print_report: enables an output string
        :return: half width of confidence interval h
        """
        # TODO Task 5.1.1: Your code goes here
        n = len(self.values)
        stand_err = math.sqrt(self.get_var() / n)
        conf_int = stand_err * scipy.stats.t.ppf(1 - alpha/2.0, n - 1)
        return conf_int

    def is_in_confidence_interval(self, x, alpha=0.05):
        """
        Check if sample x is in confidence interval with given significance level.
        :param x: is the sample
        :param alpha: is the significance level
        :return: true, if sample is in confidence interval
        """
        # TODO Task 5.1.1: Your code goes here
        lower_endpoint = self.get_mean() - self.report_confidence_interval(alpha)
        upper_endpoint = self.get_mean() + self.report_confidence_interval(alpha)

        if lower_endpoint <= x <= upper_endpoint:
            return True
        else:
            return False

    def report_bootstrap_confidence_interval(self, alpha=0.05, resample_size=5000, print_report=True):
        """
        Report bootstrapping confidence interval with given significance level.
        This is done with the bootstrap method. Hint: use numpy.random.choice for resampling
        :param alpha: significance level
        :param resample_size: resampling size
        :param print_report: enables an output string
        :return: lower and upper bound of confidence interval
        """
        # TODO Task 5.1.2: Your code goes here
        n = len(self.values)
        mean_original = self.get_mean()
        x = []
        for i in range(resample_size):
            sample_set = numpy.random.choice(self.values, n)
            sample_mean = numpy.mean(sample_set)
            x.append(sample_mean - mean_original)

        lower_point = numpy.quantile(x, 1-alpha/2.0)
        upper_point = numpy.quantile(x, alpha/2.0)
        lower_endpoint = mean_original - lower_point
        upper_endpoint = mean_original - upper_point
        return lower_endpoint, upper_endpoint

    def is_in_bootstrap_confidence_interval(self, x, resample_size=5000, alpha=0.05):
        """
        Check if sample x is in bootstrap confidence interval with given resample_size and significance level.
        :param x: is the sample
        :param resample_size: resample size
        :param alpha: is the significance level
        :return: true, if sample is in confidence interval
        """
        # TODO Task 5.1.2: Your code goes here
        points = self.report_bootstrap_confidence_interval(alpha, resample_size)
        if points[0] <= x <= points[1]:
            return True
        else:
            return False


class TimeDependentCounter(Counter):

    """
    Counter, that counts values considering their duration as well.

    Methods for calculating mean, variance and standard deviation are available.
    """
    def __init__(self, sim, name="default"):
        """
        Initialize TDC with the simulation it belongs to and the name.
        :param: sim is needed for getting the current simulation time.
        :param: name is an identifier for better distinction between multiple counters.
        """
        super(TimeDependentCounter, self).__init__(name)
        self.sim = sim
        self.first_timestamp = 0
        self.last_timestamp = 0
        self.square_values = []

    def count(self, value):
        """
        Adds new value to internal array.
        Duration from last to current value is considered.
        """
        # TODO Task 2.3.2: Your code goes here
        x = self.sim.sim_state.now - self.last_timestamp
        self.values.append(value * x)
        self.square_values.append(value * value * x)
        self.last_timestamp = self.sim.sim_state.now

    def get_mean(self):
        """
        Return the mean value of the counter, normalized by the total duration of the simulation.
        """
        # TODO Task 2.3.2: Your code goes here
        return float(math.fsum(self.values))/float((self.last_timestamp - self.first_timestamp))

    def get_var(self):
        """
        Return the variance of the TDC.
        """
        # TODO Task 2.3.2: Your code goes
        x = float((self.last_timestamp - self.first_timestamp))
        return float(math.fsum(self.square_values))/x - self.get_mean() ** 2

    def get_stddev(self):
        """
        Return the standard deviation of the TDC.
        """
        # TODO Task 2.3.2: Your code goes here
        return math.sqrt(self.get_var())

    def reset(self):
        """
        Reset the counter to its initial state.
        """
        self.first_timestamp = self.sim.sim_state.now
        self.last_timestamp = self.sim.sim_state.now
        Counter.reset(self)


class TimeIndependentCrosscorrelationCounter(TimeIndependentCounter):

    """
    Counter that is able to calculate cross correlation (and covariance).
    """

    def __init__(self, name="default"):
        """
        Crosscorrelation counter contains three internal counters containing the variables
        :param name: is a string for better distinction between counters.
        """
        super(TimeIndependentCrosscorrelationCounter, self).__init__(name)
        # TODO Task 4.1.1: Your code goes here
        self.valueX = TimeIndependentCounter()
        self.valueY = TimeIndependentCounter()
        self.meanX = 0
        self.meanY = 0
        self.value_xy = TimeIndependentCounter()

    def reset(self):
        """
        Reset the TICCC to its initial state.
        """
        TimeIndependentCounter.reset(self)
        # TODO Task 4.1.1: Your code goes here
        self.valueX = TimeIndependentCounter()
        self.valueY = TimeIndependentCounter()
        self.value_xy = TimeIndependentCounter()

    def count(self, x, y):
        """
        Count two values for the correlation between them. They are added to the two internal arrays.
        """
        # TODO Task 4.1.1: Your code goes here
        self.valueX.count(x)
        self.valueY.count(y)
        self.value_xy.count(x*y)

    def get_cov(self):
        """
        Calculate the covariance between the two internal arrays x and y.
        :return: cross covariance
        """
        # TODO Task 4.1.1: Your code goes here
        self.meanX = self.valueX.get_mean()
        self.meanY = self.valueY.get_mean()
        return self.value_xy.get_mean() - self.meanX * self.meanY

    def get_cor(self):
        """
        Calculate the correlation between the two internal arrays x and y.
        :return: cross correlation
        """
        # TODO Task 4.1.1: Your code goes here
        return self.get_cov() / math.sqrt(self.valueX.get_var()
                                          * self.valueY.get_var())

    def report(self):
        """
        Print a report string for the TICCC.

        """
        print "Name: " + self.name + "; covariance = " + str(self.get_cov()) + "; correlation = " + str(self.get_cor())


class TimeIndependentAutocorrelationCounter(TimeIndependentCounter):

    """
    Counter, that is able to calculate auto correlation with given lag.
    """

    def __init__(self, name="default", max_lag=10):
        """
        Create a new auto correlation counter object.
        :param name: string for better distinction between multiple counters
        :param max_lag: maximum available lag (defaults to 10)
        """
        super(TimeIndependentAutocorrelationCounter, self).__init__(name)
        # TODO Task 4.1.2: Your code goes here
        self.value = TimeIndependentCounter()
        self.value_shifted = TimeIndependentCounter()
        self.product = TimeIndependentCounter()
        self.max_lag = 0
        self.set_max_lag(max_lag)

    def reset(self):
        """
        Reset the counter to its original state.
        """
        TimeIndependentCounter.reset(self)
        # TODO Task 4.1.2: Your code goes here
        self.value = TimeIndependentCounter()
        self.value_shifted = TimeIndependentCounter()
        self.product = TimeIndependentCounter()

    def count(self, x):
        """
        Add new element x to counter.
        """
        # TODO Task 4.1.2: Your code goes here
        self.value.count(x)

    def get_auto_cov(self, lag):
        """
        Calculate the auto covariance for a given lag.
        :return: auto covariance
        """
        # TODO Task 4.1.2: Your code goes here
        x = self.value.get_values()
        y = deque(x)
        y.rotate(lag)
        self.value_shifted.reset()
        self.product.reset()
        for i in range(len(y)):
            self.value_shifted.count(y[i])
            self.product.count(x[i] * y[i])

        return self.product.get_mean() - self.value.get_mean() * self.value_shifted.get_mean()

    def get_auto_cor(self, lag):
        """
        Calculate the auto correlation for a given lag.
        :return: auto correlation
        """
        # TODO Task 4.1.2: Your code goes here
        return self.get_auto_cov(lag) / math.sqrt(self.value.get_var()
                                                  * self.value_shifted.get_var())

    def set_max_lag(self, max_lag):
        """
        Change maximum lag. Cycle length is set to max_lag + 1.
        """
        # TODO Task 4.1.2: Your code goes here
        self.max_lag = max_lag

    def report(self):
        """
        Print report for auto correlation counter.
        """
        print "Name: " + self.name
        print self.max_lag
        for i in range(0, self.max_lag+1):
            print "Lag = " + str(i) + "; covariance = " + str(self.get_auto_cov(i)) + "; correlation = " \
                  + str(self.get_auto_cor(i))