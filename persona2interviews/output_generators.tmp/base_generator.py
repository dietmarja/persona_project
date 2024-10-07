# File: output_generators/base_generator.py

from abc import ABC, abstractmethod

class BaseOutputGenerator(ABC):
    @abstractmethod
    def generate(self, input_data, persona):
        pass