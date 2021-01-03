from abc import ABC, abstractmethod


class LedGrid(ABC):
    @abstractmethod
    def set_led(self, x, y, value=True):
        pass

    @abstractmethod
    def clear(self):
        pass

    @abstractmethod
    def fade_out(self):
        pass

    @abstractmethod
    def fade_in(self):
        pass

