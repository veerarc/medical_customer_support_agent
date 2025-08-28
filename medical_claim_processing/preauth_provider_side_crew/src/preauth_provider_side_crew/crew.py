from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task, output_pydantic
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
from preauth_provider_side_crew.output_models.pydantic_output_models import (
    PatientInfoModel, ClinicalNotesModel, CodingModel,
    CostEstimateModel, JustificationModel, PreAuthFormModel
)

@CrewBase
class PreauthProviderSideCrew():
    """Crew for handling medical preauthorization workflow."""

    agents: List[BaseAgent]
    tasks: List[Task]

    @agent
    def patient_intake_agent(self) -> Agent:
        """Creates the patient intake agent for registration."""
        return Agent(
            config=self.agents_config['patient_intake_agent'], # type: ignore[index]
            verbose=True
        )

    @agent
    def gather_clinical_notes_agent(self) -> Agent:
        """Creates the clinical documentation specialist agent."""
        return Agent(
            config=self.agents_config['gather_clinical_notes_agent'], # type: ignore[index]
            verbose=True
        )

    @agent
    def generate_standard_codes_agent(self) -> Agent:
        """Creates the medical coding specialist agent."""
        return Agent(
            config=self.agents_config['generate_standard_codes_agent'], # type: ignore[index]
            verbose=True
        )

    @agent
    def estimate_treatment_costs_agent(self) -> Agent:
        """Creates the cost estimation analyst agent."""
        return Agent(
            config=self.agents_config['estimate_treatment_costs_agent'], # type: ignore[index]
            verbose=True
        )       
        

    @agent
    def summarize_clinical_justification_agent(self) -> Agent:
        """Creates the clinical justification writer agent."""
        return Agent(
            config=self.agents_config['summarize_clinical_justification_agent'], # type: ignore[index]
            verbose=True
        )

    @agent
    def format_preauth_form_agent(self) -> Agent:
        """Creates the preauthorization document specialist agent."""
        return Agent(
            config=self.agents_config['format_preauth_form_agent'], # type: ignore[index]
            verbose=True
        )
        
    @task
    def process_patient_registration_task(self) -> Task:
        """Task for processing patient registration."""
        return Task(
            config=self.tasks_config['process_patient_registration_task'], # type: ignore[index]
            output_pydantic=PatientInfoModel
        )

    @task
    def extract_clinical_terms_task(self) -> Task:
        """Task for processing clinical notes and documentation."""
        return Task(
            config=self.tasks_config['extract_clinical_terms_task'], # type: ignore[index]
            output_pydantic=ClinicalNotesModel
        )

    @task
    def medical_coding_task(self) -> Task:
        """Task for generating standardized medical codes."""
        return Task(
            config=self.tasks_config['medical_coding_task'], # type: ignore[index]
            output_pydantic=CodingModel
        )

    @task
    def estimate_treatment_costs_task(self) -> Task:
        """Task for estimating treatment costs."""
        return Task(
            config=self.tasks_config['estimate_treatment_costs_task'], # type: ignore[index]
            output_pydantic=CostEstimateModel
        )

    @task
    def summarize_clinical_justification_task(self) -> Task:
        """Task for creating clinical justification summary."""
        return Task(
            config=self.tasks_config['summarize_clinical_justification_task'], # type: ignore[index]
            output_pydantic=JustificationModel
        )

    @task
    def format_preauth_form_task(self) -> Task:
        """Task for formatting preauthorization submission."""
        return Task(
            config=self.tasks_config['format_preauth_form_task'], # type: ignore[index]
            output_pydantic=PreAuthFormModel
        )

    @crew
    def crew(self) -> Crew:
        """Creates the PreauthProviderSideCrew crew"""
        return Crew(
            agents=[self.agents[0], self.agents[1], self.agents[3], self.agents[4], self.agents[5]],
            tasks=[self.tasks[0], self.tasks[1], self.tasks[3], self.tasks[4], self.tasks[5]],
            process=Process.sequential,
            verbose=True,
            name="Hospital PreAuthorization Provider-Side Automation"
        )
