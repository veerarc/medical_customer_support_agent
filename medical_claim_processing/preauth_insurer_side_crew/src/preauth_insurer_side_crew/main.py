#!/usr/bin/env python
import sys
import warnings

from datetime import datetime

from preauth_insurer_side_crew.crew import PreauthInsurerSideCrew

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def run(procedure_name: str, policy_id: str, patient_id: str):
    """
    Run the pre-authorization crew for a specific request.
    
    Args:
        procedure_name: Name of the medical procedure requiring pre-authorization
        policy_id: Insurance policy ID
        patient_id: Patient's unique identifier
    """
    inputs = {
        "patient_name": "Ravi Kumar",
        "age": 45,
        "diagnosis": "Severe lumbar disc herniation with radiculopathy",
        "ICD_code": "M51.26",
        "CPT_code": "63030",
        "estimated_cost": 55000,
        "insurer": "MediCover Health",
        "policy_number": "MC202501789"
    }


    
    try:
        crew = PreauthInsurerSideCrew().crew()
        results = crew.kickoff(inputs=inputs)
        
        # Process and combine results from all tasks
        medical_review = results.get('medical_review_task')
        policy_check = results.get('policy_check_task')
        cost_estimate = results.get('cost_estimation_task')
        
        # Return consolidated pre-authorization decision
        return {
            'request_id': f"PA-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            'medical_review': medical_review,
            'policy_check': policy_check,
            'cost_estimate': cost_estimate,
            'final_decision': 'APPROVED' if all([medical_review.get('approved'), 
                                              policy_check.get('approved')]) else 'DENIED'
        }
    except Exception as e:
        raise Exception(f"An error occurred while processing the pre-authorization request: {e}")


def train():
    """
    Train the crew using sample pre-authorization cases.
    """
    sample_inputs = {
        'procedure_name': 'Total Knee Replacement',
        'policy_id': 'POL123456',
        'patient_id': 'PAT789012',
        'request_date': str(datetime.now().date())
    }
    
    try:
        PreauthInsurerSideCrew().crew().train(
            n_iterations=int(sys.argv[1]),
            filename=sys.argv[2],
            inputs=sample_inputs
        )
    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")


def test():
    """
    Test the crew with various pre-authorization scenarios.
    """
    test_cases = [
        {
            'procedure_name': 'Colonoscopy',
            'policy_id': 'POL111222',
            'patient_id': 'PAT333444',
            'request_date': str(datetime.now().date())
        },
        {
            'procedure_name': 'MRI Brain',
            'policy_id': 'POL555666',
            'patient_id': 'PAT777888',
            'request_date': str(datetime.now().date())
        }
    ]
    
    try:
        for test_case in test_cases:
            PreauthInsurerSideCrew().crew().test(
                n_iterations=int(sys.argv[1]),
                eval_llm=sys.argv[2],
                inputs=test_case
            )
    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")
