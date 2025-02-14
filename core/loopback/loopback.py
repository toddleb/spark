"""
Loopback Mechanism for AI Workflow Responses
"""

import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class LoopbackManager:
    """
    Manages the loopback mechanism for routing AI workflow responses
    """
    
    def __init__(self):
        """
        Initialize the loopback manager
        """
        self._response_queue = {}
        self._callback_registry = {}
    
    async def register_callback(self, workflow_id: str, callback_fn):
        """
        Register a callback function for a specific workflow
        
        :param workflow_id: Unique identifier for the workflow
        :param callback_fn: Async callback function to process responses
        """
        self._callback_registry[workflow_id] = callback_fn
        logger.info(f"Callback registered for workflow: {workflow_id}")
    
    async def send_response(self, workflow_id: str, response: Dict[str, Any]):
        """
        Send a response back through the registered callback
        
        :param workflow_id: Unique identifier for the workflow
        :param response: Response data to be processed
        """
        try:
            # Check if a callback is registered for this workflow
            callback = self._callback_registry.get(workflow_id)
            
            if not callback:
                logger.warning(f"No callback registered for workflow: {workflow_id}")
                self._response_queue[workflow_id] = response
                return
            
            # Call the callback with the response
            await callback(response)
            logger.info(f"Response processed for workflow: {workflow_id}")
        
        except Exception as e:
            logger.error(f"Error processing response for workflow {workflow_id}: {e}")
            # Store the response in queue for potential later processing
            self._response_queue[workflow_id] = response
    
    async def retrieve_queued_response(self, workflow_id: str):
        """
        Retrieve a queued response for a specific workflow
        
        :param workflow_id: Unique identifier for the workflow
        :return: Queued response or None
        """
        return self._response_queue.pop(workflow_id, None)
    
    def clear_callback(self, workflow_id: str):
        """
        Clear the callback for a specific workflow
        
        :param workflow_id: Unique identifier for the workflow
        """
        if workflow_id in self._callback_registry:
            del self._callback_registry[workflow_id]
            logger.info(f"Callback cleared for workflow: {workflow_id}")

# Create a singleton instance of the LoopbackManager
loopback_manager = LoopbackManager()
