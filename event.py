"""
Author: Sayanta Roychowdhury
Matriculation No: 03709791
"""

from heapq import heapify, heappush, heappop


class EventChain(object):
    """
    This class contains a queue of events.

    Events can be inserted and removed from queue and are sorted by their time.
    Always the oldest event is removed.
    """

    def __init__(self):
        """
        Initialize variables and event chain
        """
        self.event_list = []

    def insert(self, e):
        """
        Inserts event e to the event chain. Event chain is sorted during insertion.
        :param: e is of type SimEvent

        """
        # TODO Task 1.2.2: Your code goes here
        heapify(self.event_list)
        heappush(self.event_list, e)

    def remove_oldest_event(self):
        """
        Remove event with smallest timestamp (if timestamps are equal then smallest priority value i.e. highest priority event) from queue
        :return: next event in event chain
        """
        # TODO Task 1.2.2: Your code goes here
        return heappop(self.event_list)


class SimEvent(object):
    """
    SimEvent represents an abstract type of simulation event.

    Contains mainly abstract methods that should be implemented in the subclasses.
    Comparison for EventChain insertion is implemented by comparing first the timestamps and then the priorities
    """

    def __init__(self, sim, timestamp):
        """
        Initialization routine, setting the timestamp of the event and the simulation it belongs to.
        """
        self.timestamp = timestamp
        self.priority = 0
        self.sim = sim

    def process(self):
        """
        General event processing routine. Should be implemented in subclass
        """
        raise NotImplementedError("Please Implement method \"process\" in subclass of SimEvent")

    def __lt__(self, other):
        """
        Comparison is made by comparing timestamps. If time stamps are equal, priorities are compared.
        """
        # TODO Task 1.2.1: Your code goes here
        return (self.timestamp, self.priority) < (other.timestamp, other.priority)


class CustomerArrival(SimEvent):
    """
    Defines a new customer arrival event (new packet comes into the system)
    """

    def __init__(self, sim, timestamp):
        """
        Create a new customer arrival event with given execution time.

        Priority of customer arrival event is set to 1 (second highest)
        """
        super(CustomerArrival, self).__init__(sim, timestamp)
        self.priority = 1

    def process(self):
        """
        Processing procedure of a customer arrival.

        Implement according to the task description.
        """
        # TODO Task 1.3.2: Your code goes here
        # time = self.sim.sim_state.now + self.sim.sim_param.IAT
        time = self.sim.sim_state.now + self.sim.rng.get_iat() * 1000
        arrival = CustomerArrival(self.sim, time)
        self.sim.event_chain.insert(arrival)
        if self.sim.system_state.add_packet_to_server():
            # ct = self.sim.sim_state.now + randint(1, 1000)
            ct = self.sim.sim_state.now + self.sim.rng.get_st() * 1000
            completion = ServiceCompletion(self.sim, ct)
            self.sim.event_chain.insert(completion)
            self.sim.sim_state.packet_accepted()
        elif self.sim.system_state.add_packet_to_queue():
            self.sim.sim_state.packet_accepted()
        else:
            self.sim.sim_state.packet_dropped()


class ServiceCompletion(SimEvent):
    """
    Defines a service completion event (highest priority in EventChain)
    """

    def __init__(self, sim, timestamp):
        """
        Create a new service completion event with given execution time.

        Priority of service completion event is set to 0 (highest).
        """
        super(ServiceCompletion, self).__init__(sim, timestamp)
        self.priority = 0

    def process(self):
        """
        Processing procedure of a service completion.

        Implement according to the task description
        """
        # TODO Task 1.3.3: Your code goes here
        self.sim.system_state.complete_service()
        if self.sim.system_state.start_service():
            # ct = self.sim.sim_state.now + randint(1, 1000)
            ct = self.sim.sim_state.now + self.sim.rng.get_st() * 1000
            completion = ServiceCompletion(self.sim, ct)
            self.sim.event_chain.insert(completion)


class SimulationTermination(SimEvent):
    """
    Defines the end of a simulation. (least priority in EventChain)
    """

    def __init__(self, sim, timestamp):
        """
        Create a new simulation termination event with given execution time.

        Priority of simulation termination event is set to 2 (lowest)
        """
        super(SimulationTermination, self).__init__(sim, timestamp)
        self.priority = 2

    def process(self):
        """
        Implement according to the task description.
        """
        # TODO Task 1.3.1: Your code goes here
        self.sim.sim_state.stop = True
