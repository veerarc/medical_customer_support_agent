#!/usr/bin/env python
from random import randint

from pydantic import BaseModel

from crewai.flow import Flow, listen, start
from crews.preauth_insurer_crew.preauth_insurer_crew import PreauthInsurerCrew

class DecisionState(BaseModel):
    sentence_count: int = 1
    output_json: str = ""


class PreauthInsurerFlow(Flow[DecisionState]):

    @start()
    def generate_sentence_count(self):
        print("Generating sentence count")
        self.state.sentence_count = randint(1, 5)

    @listen(generate_sentence_count)
    def generate_decision(self):
        print("Generating poem")
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
        result = (
            PreauthInsurerCrew()
            .crew()
            .kickoff(inputs=preauth_json)
        )

        print("Poem generated", result.raw)
        self.state.output_json = result.raw

    @listen(generate_decision)
    def save_decision(self):
        print("Saving decision")
        with open("result.txt", "w") as f:
            f.write(self.state.output_json)


def kickoff():
    poem_flow = PreauthInsurerFlow()
    poem_flow.kickoff()


def plot():
    poem_flow = PreauthInsurerFlow()
    poem_flow.plot()


if __name__ == "__main__":
    kickoff()
