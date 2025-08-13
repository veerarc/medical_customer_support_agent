from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
from .tools.custom_tool import (
    JSONValidatorTool
)

@CrewBase
class PreauthInsurerSideCrew():
    """PreauthInsurerSideCrew crew for processing pre-authorization requests"""

    agents: List[BaseAgent]
    tasks: List[Task]

    def __init__(self):
        self.llm=LLM(model="ollama/deepseek-r1:8b", base_url="http://localhost:11434")
        # self.patient_history_tool = FetchPatientHistoryTool()
        # self.policy_tool = VerifyPolicyTool()
        # self.cost_tool = CalculateCostsTool()

    @agent
    def intake_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['intake_agent'], # type: ignore[index]
            llm=self.llm,
            tools=[JSONValidatorTool()]
        ) 

    @agent
    def policy_agent(self):
        return Agent(
            config=self.agents_config['policy_agent'],  # type: ignore[index]
            llm=self.llm
        )

    @agent
    def clinical_agent(self):
        return Agent(
            config=self.agents_config['clinical_agent'],  # type: ignore[index]
            llm=self.llm    
        )

    @agent
    def cost_agent(self):
        return Agent(
            config=self.agents_config['cost_agent'],  # type: ignore[index]
            llm=self.llm
        )

    @agent
    def decision_agent(self):
        return Agent(
            config=self.agents_config['decision_agent'],  # type: ignore[index]
            llm=self.llm
        )

    @task
    def intake_validation_task(self):
        return  Task(config=self.tasks_config['intake_validation_task']) # type: ignore[index]

    @task
    def coverage_verification_task(self):
        return  Task(config=self.tasks_config['coverage_verification_task']) # type: ignore[index]

    @task
    def clinical_review_task(self):
        return  Task(config=self.tasks_config['clinical_review_task']) # type: ignore[index]

    @task
    def financial_analysis_task(self):
        return  Task(config=self.tasks_config['financial_analysis_task']) # type: ignore[index]

    @task
    def final_determination_task(self):
        return Task( config=self.tasks_config['final_determination_task']) # type: ignore[index]

    @crew
    def crew(self) -> Crew:
        """Creates the PreauthInsurerSideCrew crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
