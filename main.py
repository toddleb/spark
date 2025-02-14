"""
Spark Project Main Entry Point
"""

import os
import asyncio
import logging
from dotenv import load_dotenv

# Explicitly import to ensure phases are registered
from core.phases.base_phase import register_phases

from ai.workflow_engine import DetailedAIWorkflowEngine
from core.registries.model_registry import ModelConfig
from core.registries.workflow_registry import WorkflowType
from core.registries.phase_registry import PhaseConfig

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("spark_project.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

async def setup_project_registry(engine):
    """Setup initial project registries"""
    try:
        # Ensure phases are registered
        register_phases()
        logger.info("Phases registered")

        # Register a GPT model
        gpt_model_config = ModelConfig(
            model_id="gpt_default",
            provider="openai",
            model_name="gpt-4-turbo",
            version="1.0.0",
            capabilities=["text_generation", "qa", "summarization"],
            parameters={
                "temperature": 0.7,
                "max_tokens": 1000
            }
        )
        await engine.model_registry.register_model(gpt_model_config)

        # Define multiple workflow types
        workflows = [
            WorkflowType(
                type_code="text_generation",
                name="Text Generation Workflow",
                description="Workflow for generating text-based content",
                phases=[
                    PhaseConfig(
                        phase_number=1,
                        phase_name="input_analysis",
                        description="Analyze input requirements",
                        required_capabilities=["text_generation"],
                        prompt_template="Analyze the following input: {input}"
                    ),
                    PhaseConfig(
                        phase_number=2,
                        phase_name="content_generation",
                        description="Generate content based on analysis",
                        required_capabilities=["text_generation"],
                        prompt_template="Generate content based on: {analysis}"
                    )
                ]
            )
        ]

        # Register workflows
        for workflow in workflows:
            await engine.workflow_registry.register_workflow(workflow)
        
        logger.info("Project registries setup complete")
    except Exception as e:
        logger.error(f"Error setting up project registries: {e}", exc_info=True)
        raise

async def main():
    """Main application entry point"""
    try:
        # Initialize workflow engine
        engine = DetailedAIWorkflowEngine()
        
        # Setup project registries
        await setup_project_registry(engine)
        
        # Project specification
        project_specs = [
            {
                "description": "Generate a technical blog post",
                "workflow_type": "text_generation",
                "input_data": {
                    "topic": "Advances in AI Workflow Automation",
                    "tone": "professional",
                    "length": "medium"
                }
            }
        ]
        
        # Execute multiple project workflows
        for spec in project_specs:
            logger.info(f"Starting project: {spec['description']}")
            
            # Identify workflow type or use a default
            workflow_type = spec.get('workflow_type') or await engine.workflow_registry.identify_workflow_type(spec['description'])
            
            # Execute project workflow
            result = await engine.execute_project({**spec, 'workflow_type': workflow_type})
            
            # Log and process results
            logger.info(f"Project Execution Complete: {spec['description']}")
            logger.info(f"Workflow Type: {result.get('workflow_type')}")
            
            # Detailed phase results
            for phase_name, phase_result in result.get('results', {}).items():
                logger.info(f"Phase {phase_name} Result: {phase_result}")
        
    except Exception as e:
        logger.error(f"Project execution failed: {e}", exc_info=True)

def cli():
    """Command-line interface to run the project"""
    import argparse

    parser = argparse.ArgumentParser(description="Spark AI Workflow Project")
    parser.add_argument('--log-level', 
                        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'], 
                        default='INFO', 
                        help='Set the logging level')
    
    args = parser.parse_args()

    # Set log level
    logging.getLogger().setLevel(getattr(logging, args.log_level))

    # Run the async main function
    asyncio.run(main())

if __name__ == "__main__":
    cli()
