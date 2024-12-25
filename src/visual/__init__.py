from abc import ABC, abstractmethod


class Visual(ABC):

    def __init__(self, flow):
        self.flow = flow

    @abstractmethod
    def visualize(self):
        raise NotImplementedError
