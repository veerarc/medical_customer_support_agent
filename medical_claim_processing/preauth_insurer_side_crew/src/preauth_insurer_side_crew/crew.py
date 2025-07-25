from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
from .tools.custom_tool import (
    FetchPatientHistoryTool,
    VerifyPolicyTool,
    CalculateCostsTool
)

@CrewBase
class PreauthInsurerSideCrew():
    """PreauthInsurerSideCrew crew for processing pre-authorization requests"""

    agents: List[BaseAgent]
    tasks: List[Task]

    def __init__(self):
        self.patient_history_tool = FetchPatientHistoryTool()
        self.policy_tool = VerifyPolicyTool()
        self.cost_tool = CalculateCostsTool()


    @agent
    def intake_agent(self):
        return YamlAgent(path=os.path.join(CONFIG_PATH, 'agents.yaml'), agent_name='intake_agent')

    @agent
    def policy_agent(self):
        return YamlAgent(path=os.path.join(CONFIG_PATH, 'agents.yaml'), agent_name='policy_agent')

    @agent
    def clinical_agent(self):
        return YamlAgent(path=os.path.join(CONFIG_PATH, 'agents.yaml'), agent_name='clinical_agent')

    @agent
    def cost_agent(self):
        return YamlAgent(path=os.path.join(CONFIG_PATH, 'agents.yaml'), agent_name='cost_agent')

    @agent
    def decision_agent(self):
        return YamlAgent(path=os.path.join(CONFIG_PATH, 'agents.yaml'), agent_name='decision_agent')

    @task
    def task1(self):
        return YamlTask(path=os.path.join(CONFIG_PATH, 'tasks.yaml'), task_name='task1')

    @task
    def task2(self):
        return YamlTask(path=os.path.join(CONFIG_PATH, 'tasks.yaml'), task_name='task2')

    @task
    def task3(self):
        return YamlTask(path=os.path.join(CONFIG_PATH, 'tasks.yaml'), task_name='task3')

    @task
    def task4(self):
        return YamlTask(path=os.path.join(CONFIG_PATH, 'tasks.yaml'), task_name='task4')

    @task
    def task5(self):
        return YamlTask(path=os.path.join(CONFIG_PATH, 'tasks.yaml'), task_name='task5')

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
