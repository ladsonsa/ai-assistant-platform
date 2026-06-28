from abc import ABC, abstractmethod


class BaseLLMProvider(ABC):

    @abstractmethod
    def generate_response(
        self,
        messages: list[dict[str, str]],
    ) -> str:
        """
        Generate a response using the configured provider.
        """
        raise NotImplementedError
