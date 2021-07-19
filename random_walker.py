#!/usr/bin/env python3

from typing import Dict
from numpy.random import normal
from rx.subject.subject import Subject

class RandomWalker:

    new_config = Subject()

    new_values = Subject()

    _values = []

    _config = {
        "skew": 0,
        "volatility": 0.01,
        "minimum": 0.01
    }

    def __init__(self, initial_value = 10, initial_datapoints = 100):
        self._values = [initial_value] * initial_datapoints
        for _ in range(initial_datapoints):
            self.next()

    def get_config(self):
        '''
        Get a copy of the config.
        
        Create a copy of the config and return it.
        Editing this copy won't change the original config.
        Any changes to the original config wont reflect in the copy.
        '''

        return self._config.copy()

    def set_config(self, new_config: Dict):
        '''
        Updates the config in a thread safe fashion.
        '''

        config = self.get_config()
        config.update(new_config)
        self._config = config
        self.new_config.on_next(config)

    def get_values(self):
        '''
        Get a copy of the values.
        
        Create a copy of the list of values and return it.
        Editing this copy won't change the original value list.
        Any changes in the original value list wont reflect in the copy.
        '''

        return self._values.copy()

    def next(self):
        '''
        Step the random walk forward by one.

        Do some calculations.
        Triggers some observers after the calculations have finished.
        '''

        config = self.get_config()
        values = self.get_values()
        skew = config["skew"]
        volatility = config["volatility"]
        minimum = config["minimum"]
        current_value = values[-1]

        # Value changes are based on a multiplier.
        multiplier = 1 + normal(skew, volatility)

        # Sanity check: max value change up or down is 90%.
        # This is to prevent the value from going negative.
        multiplier = max(0.1, multiplier)
        multiplier = min(multiplier, 1.9)

        # Update the value and enforce the minimum
        next_value = max(minimum, current_value * multiplier)
        values.pop(0)
        values.append(next_value)
        self._values = values
        self.new_values.on_next(values)
