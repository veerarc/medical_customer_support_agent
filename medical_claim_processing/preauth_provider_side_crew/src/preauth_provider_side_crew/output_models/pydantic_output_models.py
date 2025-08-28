from pydantic import BaseModel
from typing import List, Optional, Dict

# ---------- Pydantic Models ----------
class ContactModel(BaseModel):
    phone: str
    email: str

class PhysicianModel(BaseModel):
    name: str
    department: str
    npi: str

class InsuranceModel(BaseModel):
    insurer_name: str
    policy_number: str      
    group_number: str
    valid_from: str
    valid_to: str
    network_affiliation: str
    
class PatientInfoModel(BaseModel):
    first_name: str
    last_name: str
    dob: str
    gender: str
    contact: ContactModel
    address: str
    ehr_id: str
    physician: PhysicianModel
    insurance: InsuranceModel


class ClinicalNotesModel(BaseModel):
    symptoms: List[str]
    diagnosis: str
    procedure: str
    risk_factors: List[str]

class CodingModel(BaseModel):
    icd_codes: Dict[str, str]  # code: description
    cpt_codes: Dict[str, str]  # code: description
    assigned_codes: Dict[str, str]  # type: code

class CostEstimateModel(BaseModel):
    procedure_name: str
    procedure_code: str
    procedure_cost: float
    estimated_length_of_stay: str
    pre_post_care_cost: float
    consumables: float
    total_estimate: float
    consumables: float
    total_estimate: float

class JustificationModel(BaseModel):
    clinical_summary: str
    guideline_references: List[str]
    supporting_evidence: str


class PreAuthFormModel(BaseModel):
    patient_info: PatientInfoModel
    insurance_info: InsuranceModel
    clinical_notes: ClinicalNotesModel
    coding: CodingModel
    cost_estimate: CostEstimateModel
    justification: JustificationModel
    formatted_document: Optional[str]

