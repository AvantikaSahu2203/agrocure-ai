from abc import ABC, abstractmethod
from typing import Any, Dict

class BaseAgent(ABC):
    """
    Abstract base class for all AI Agents.
    """
    
    @abstractmethod
    def execute(self, input_data: Any) -> Dict[str, Any]:
        """
        Execute the agent's specific task.
        
        Args:
            input_data: The input data required for the agent.
            
        Returns:
            A dictionary containing the agent's output.
        """
        pass
