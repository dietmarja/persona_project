# File: input_processors/base_processor.py

from abc import ABC, abstractmethod

class BaseInputProcessor(ABC):
    @abstractmethod
    def process(self):
        pass