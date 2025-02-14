"""
Base Phase Implementation for Workflow Phases
"""

import os
import logging
from typing import Dict, Any

from core.registries.phase_registry import BasePhase, PhaseRegistry, PhaseConfig
from core.loopback.loopback import loopback_manager
from langchain_openai import ChatOpenAI

logger = logging.getLogger(__name__)

class InputAnalysisPhase(BasePhase):
    """Phase for analyzing input requirements"""
    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze input requirements for the workflow
        
        :param input_data: Input data for the workflow
        :return: Analysis results
        """
        # Initialize OpenAI model
        try:
            model = ChatOpenAI(
                model_name="gpt-4-turbo",
                temperature=0.7,
                api_key=os.getenv("OPENAI_API_KEY")
            )

            # Prepare prompt for input analysis
            prompt = f"""Provide a comprehensive analysis of the following input requirements:
            Description: {input_data.get('description', '')}
            Topic: {input_data.get('input_data', {}).get('topic', '')}
            Tone: {input_data.get('input_data', {}).get('tone', 'professional')}
            Length: {input_data.get('input_data', {}).get('length', 'medium')}

            Break down the requirements, provide context, and outline key considerations for content creation."""
            
            # Invoke the model
            response = model.invoke(prompt)
            
            analysis_result = {
                "analysis": response.content,
                "input_data": input_data
            }
            
            # Optional: Use loopback to send analysis to next phase
            await loopback_manager.send_response("workflow_analysis", analysis_result)
            
            return analysis_result
        except Exception as e:
            logger.error(f"Input analysis failed: {e}")
            return {
                "error": f"Analysis failed: {str(e)}",
                "input_data": input_data
            }

class ContentGenerationPhase(BasePhase):
    """Phase for generating content based on analysis"""
    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate content based on previous phase analysis
        
        :param input_data: Input data from previous phase
        :return: Generated content
        """
        try:
            # Initialize OpenAI model
            model = ChatOpenAI(
                model_name="gpt-4-turbo",
                temperature=0.7,
                api_key=os.getenv("OPENAI_API_KEY")
            )

            # Extract analysis and original input data
            analysis = input_data.get('analysis', '')
            original_input = input_data.get('input_data', {})
            
            # Prepare prompt for content generation
            prompt = f"""Based on the following comprehensive analysis, generate a technical blog post:

            Analysis Background:
            {analysis}

            Content Requirements:
            - Topic: {original_input.get('topic', '')}
            - Tone: {original_input.get('tone', 'professional')}
            - Length: {original_input.get('length', 'medium')}

            Guidelines:
            - Maintain a professional and technical tone
            - Provide in-depth insights into the topic
            - Ensure the content is informative and engaging
            - Structure the post with a clear introduction, body, and conclusion
            - Include relevant technical details and examples

            Generate the blog post content:"""
            
            # Invoke the model
            response = model.invoke(prompt)
            
            content_result = {
                "generated_content": response.content,
                "input_data": input_data
            }
            
            # Optional: Use loopback to send content to next phase or for further processing
            await loopback_manager.send_response("workflow_content", content_result)
            
            return content_result
        except Exception as e:
            logger.error(f"Content generation failed: {e}")
            return {
                "error": f"Content generation failed: {str(e)}",
                "input_data": input_data
            }

def register_phases():
    """Register available phases with the phase registry"""
    PhaseRegistry.register("input_analysis", InputAnalysisPhase)
    PhaseRegistry.register("content_generation", ContentGenerationPhase)
    logger.info("Phases registered successfully")

# Register phases when module is imported
register_phases()
