import math
from random import Random


class RNG(object):

    """
    Class RNG contains two random number streams, one for IAT and one for ST.

    Both RNS can be set during initialization or separately. The next random numbers are generated by the functions
    get_iat() or get_st().
    """

    def __init__(self, rns1, rns2):
        """
        Initialize a RNG object with two RNS given.
        :param rns1: represents the RNS for the inter-arrival times.
        :param rns2: represents the RNS for the service times.
        """
        self.iat_rns = rns1
        self.st_rns = rns2

    def set_iat_rns(self, rns1):
        """
        Set a new RNS for the inter-arrival times.
        """
        self.iat_rns = rns1

    def set_st_rns(self, rns2):
        """
        Set a new RNS for the service times.
        """
        self.st_rns = rns2

    def get_iat(self):
        """
        Return a new sample of the IAT RNS
        """
        return self.iat_rns.next()

    def get_st(self):
        """
        Return a new sample of the ST RNS
        """
        return self.st_rns.next()


class RNS(object):

    """
    Basic abstract class for random number streams.

    To be implemented in subclass.
    Contains a Random class r in order to allow different seeds for different RNS
    """

    def __init__(self, the_seed=None):
        """
        Initialize the general RNS with an optional seed.
        All further initialization is done in subclass.
        """
        self.r = Random(the_seed)

    def set_parameters(self, *args):
        NotImplementedError("Implement in subclass")

    def next(self):
        """
        Method should be overwritten in subclass.
        """
        return 0


class ExponentialRNS(RNS):

    """
    Class to provide exponentially distributed random numbers. After initialization, new numbers can be generated
    using next(). Initialization with given parameters and optional seed.
    :param the_seed: optional seed for the random number stream
    """

    def __init__(self, arrival_rate, the_seed=None):
        """
        Initialize Exponential RNS and set the parameters.
        """
        super(ExponentialRNS, self).__init__(the_seed)
        # TODO Task 3.1.1: Your code goes here
        """
        Also modify the list of input parameters according to the needs of this distribution.
        """
        self.arrival_rate = 0
        self.set_parameters(arrival_rate)

    def set_parameters(self, arrival_rate):
        """
        Set parameters of the distribution.
        """
        # TODO Task 3.1.1: Your code goes here
        """
        Also modify the list of input parameters according to the needs of this distribution.
        """
        self.arrival_rate = arrival_rate

    def next(self):
        """
        Generate the next random number using the inverse transform method.
        """
        # TODO Task 3.1.1: Your code goes here
        return -math.log(self.r.uniform(0, 1)) * (1.0 / float(self.arrival_rate))


class UniformRNS(RNS):

    """
    Class to provide exponentially distributed random numbers. After initialization, new numbers can be generated
    using next(). Initialization with given parameters and optional seed.
    :param the_seed: optional seed for the random number stream
    """

    def __init__(self, lower_limit, upper_limit, the_seed=None):
        """
        Initialize Uniform RNS and set the parameters.
        """
        super(UniformRNS, self).__init__(the_seed)
        # TODO Task 3.1.1: Your code goes here
        """
        Also modify the list of input parameters according to the needs of this distribution.
        """
        self.lower_limit = 0
        self.upper_limit = 0
        self.set_parameters(lower_limit, upper_limit)

    def set_parameters(self, lower_limit, upper_limit):
        """
        Set parameters.
        """
        # TODO Task 3.1.1: Your code goes here
        """
        Also modify the list of input parameters according to the needs of this distribution.
        """
        self.lower_limit = lower_limit
        self.upper_limit = upper_limit

    def next(self):
        """
        Generate the next random number using the inverse transform method.
        """
        # TODO Task 3.1.1: Your code goes here
        return self.lower_limit + self.r.uniform(0, 1) * (self.upper_limit - self.lower_limit)