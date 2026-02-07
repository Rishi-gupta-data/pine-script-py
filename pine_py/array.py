import numpy as np


class Array:
    def __init__(self, data=None):
        if data is None:
            self.data = []
        elif isinstance(data, list):
            self.data = data
        elif isinstance(data, np.ndarray):
            self.data = data.tolist()
        else:
            self.data = [data]

    def size(self):
        return len(self.data)

    def clear(self):
        self.data.clear()

    def get(self, index):
        return self.data[index]

    def set(self, index, value):
        self.data[index] = value

    def push(self, value):
        self.data.append(value)

    def pop(self):
        return self.data.pop()


# Factory helpers

def new_float(size=0, initial_value=0.0):
    return Array([float(initial_value)] * size)


def new_int(size=0, initial_value=0):
    return Array([int(initial_value)] * size)


def new_bool(size=0, initial_value=False):
    return Array([bool(initial_value)] * size)


def new_string(size=0, initial_value=""):
    return Array([str(initial_value)] * size)
