#!/usr/bin/env python3

from numpy import random

class RandomWalker:
    values = []

    config = {
        "skew": 0,
        "volatility": 0.01,
        "minimum": 0.01,
        "target_price": 10
    }

    def __init__(self, initial_value = 10, initial_datapoints = 100):
        for _ in range(initial_datapoints):
            self.values.append(initial_value)
        for _ in range(initial_datapoints):
            self.next()

    def get_config(self):
        '''
        Gets a copy of the config. Editing this copy won't change the original config.
        '''
        return self.config.copy()

    def set_config(self, new_config):
        '''
        Updates the config in a thread safe fashion.
        '''
        config = self.get_config()
        config.update(new_config)
        self.config = config

    def get_values(self):
        '''
        Gets a copy of the values. Editing this copy won't change the original values.
        '''
        return self.values.copy()

    def next(self):
        '''
        Step the random walk forward by one.
        '''
        config = self.config.copy()
        skew = config["skew"]
        volatility = config["volatility"]
        minimum = config["minimum"]

        # Value changes are based on a multiplier.
        multiplier = 1 + random.normal(skew, volatility)

        # Sanity check: max value change up or down is 90%.
        # This is to prevent the value from going negative.
        multiplier = max(0.1, multiplier)
        multiplier = min(multiplier, 1.9)

        # Update the value and enforce the minimum
        next_value = max(minimum, self.values[-1] * multiplier)
        new_values = self.values.copy()
        new_values.pop(0)
        new_values.append(next_value)
        self.values = new_values