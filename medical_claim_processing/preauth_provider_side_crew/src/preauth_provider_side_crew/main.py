#!/usr/bin/env python
import sys
import warnings

from datetime import datetime


from preauth_provider_side_crew.crew import PreauthProviderSideCrew

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def run():
    """
    Run the crew.
    """
    inputs = {
        "patient_info": {
            "first_name": "Rajesh",
            "last_name": "Kumar",
            "dob": "1980-05-12",
            "gender": "Male",
            "contact": {
                "phone": "+91-9876543210",
                "email": "rajesh.kumar@example.com"
            },
            "address": "Hyderabad, Telangana, India",
            "ehr_id": "EHR-998877",
            "physician": {
                "name": "Dr. Anjali Mehta",
                "department": "Orthopedics",
                "npi": "1234567890"
            }
        },
        "insurance_card": {
            "insurer_name": "Star Health Insurance",
            "policy_number": "STAR-HI-20394857",
            "group_number": "GRP-112233",
            "valid_from": "2024-01-01",
            "valid_to": "2025-12-31",
            "network_affiliation": "In-Network"
        },
        "clinical_notes": """
                The patient presents with chronic left knee pain for over 6 months, worsening with movement. 
                X-ray confirms osteoarthritis. Recommended Arthroscopic Knee Surgery intervention with pre/post rehab. 
                No known drug allergies. Pre-op evaluation needed.
            """
        ,
        "pricing_data": {
            "procedure_name": "Arthroscopic Knee Surgery",
            "procedure_code": "29881",
            "procedure_cost": 48000,
            "estimated_length_of_stay": "2 days",
            "pre_post_care_cost": 7500,
            "consumables": 3200,
            "total_estimate": 58700
        },
        "coding_reference": {
            "icd_codes": {
                "M17.12":"Unilateral primary osteoarthritis, left knee",
                "M17.11":"Unilateral primary osteoarthritis, right knee",
                "M17.10":"Unilateral primary osteoarthritis, unspecified knee"
                
            },
            "cpt_codes": {
                "29881": "Arthroscopy, knee, surgical; with meniscectomy (medial OR lateral including any meniscal shaving)",
                "29880": "Arthroscopy, knee, surgical; with removal of loose body or foreign body",
                "29882": "Arthroscopy, knee, surgical; with repair of meniscus (medial OR lateral)"
            }
        }
    }
    
    try:
        PreauthProviderSideCrew().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")


def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        "topic": "AI LLMs",
        'current_year': str(datetime.now().year)
    }
    try:
        PreauthProviderSideCrew().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        PreauthProviderSideCrew().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        "topic": "AI LLMs",
        "current_year": str(datetime.now().year)
    }
    
    try:
        PreauthProviderSideCrew().crew().test(n_iterations=int(sys.argv[1]), eval_llm=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")
