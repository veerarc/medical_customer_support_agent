from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
from tools.custom_tool import JSONValidatorTool

# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators
# Shared LLM for all agents
llm = LLM(model="ollama/deepseek-r1:8b", base_url="http://localhost:11434")

@CrewBase
class PreauthInsurerCrew():
    """PreauthInsurerCrew crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    def __init__(self):
        # Register the tool with each agent that needs it
        self.tools = [JSONValidatorTool()]

    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
    
    # If you would like to add tools to your agents, you can learn more about it here:
    # https://docs.crewai.com/concepts/agents#agent-tools
    @agent
    def intake_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['intake_agent'],  # type: ignore[index]
            tools=[JSONValidatorTool()],
            llm=llm,
            verbose=True
        )

    @agent
    def policy_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['policy_agent'],  # type: ignore[index]
            llm=llm,
            verbose=True
        )
        
    @agent
    def clinical_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['clinical_agent'],  # type: ignore[index]
            llm=llm,
            verbose=True
        )
        
    @agent
    def cost_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['cost_agent'],  # type: ignore[index]
            llm=llm,
            verbose=True
        )
        
    @agent
    def decision_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['decision_agent'],  # type: ignore[index]
            llm=llm,
            verbose=True
        )

    # To learn more about structured task outputs,
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.crewai.com/concepts/tasks#overview-of-a-task
    @task
    def ingest_request_task(self) -> Task:
        return Task(
            config=self.tasks_config['ingest_request_task'], # type: ignore[index]
        )

    @task
    def validate_request_task(self) -> Task:
        return Task(
            config=self.tasks_config['validate_request_task'],
        )
        
    @task
    def evaluate_clinical_necessity_task(self) -> Task:
        return Task(
            config=self.tasks_config['evaluate_clinical_necessity_task'], # type: ignore[index]
        )

    @task
    def estimate_risk_task(self) -> Task:
        return Task(
            config=self.tasks_config['estimate_risk_task'],
        )
        
    @task
    def aggregate_outputs_task(self) -> Task:
        return Task(
            config=self.tasks_config['aggregate_outputs_task'],
        ) 

    @crew
    def crew(self) -> Crew:
        """Creates the PreauthInsurerCrew crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge
        #tool_registry.register("json_validator_tool", json_validator_tool)

        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
        
        
        
if __name__ == "__main__":
    preauth_json = {
            "preauth_request" : {
                "patient_name": "Rajesh Kumar",
                "age": 45,
                "policy_number": "STAR-HI-20394857",
                "insurer": "Star Health Insurance.",
                "diagnosis": "Osteoarthritis",
                "ICD_code": "M17.12",
                "CPT_code": "29881",
                "estimated_cost": 65000,
                "treatment_plan": "Arthroscopy, knee, surgical; meniscectomy with 3-day hospital stay",
            },
    }
    PreauthInsurerCrew().crew().kickoff(inputs=preauth_json)

