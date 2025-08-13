
from email.mime import image
from PIL import Image
import pytesseract
import uuid
import json
from crewai.tools import BaseTool

class OCRTool(BaseTool):
    name: str = "OCRTool"
    description: str = "Extracts text from images using Optical Character Recognition (OCR). This tool is useful for reading text from scanned documents or images."
    def _run(self, image_path: str) -> str:
        image = Image.open(image_path)
        raw_text = pytesseract.image_to_string(image, config='--psm 6')
        return raw_text 


class JSONValidatorTool(BaseTool):
    name: str = "JSONValidatorTool"
    description: str  = "Validates the structure of a JSON object to ensure it contains all required fields for medical claim processing. This tool checks for the presence of specific fields in the JSON data."
    
    REQUIRED_FIELDS: list = ["patient_name", "age", "diagnosis", "ICD_code", "CPT_code", "estimated_cost", "insurer", "policy_number"]

    def _run(self, data: dict) -> str:
        missing = [field for field in self.REQUIRED_FIELDS if field not in data or data[field] in (None, "")]
        if missing:
            return f"Missing or empty fields: {', '.join(missing)}"
        return "All required fields are present and valid."


class CreateUUIDTool(BaseTool):
    name: str = "CreateUUIDTool"
    description: str = "Generates a new universally unique identifier (UUIDv4) when called."

    def _run(self) -> str:
        """Return a new UUID as a string."""
        return str(uuid.uuid4())
    
class FHIRParserTool(BaseTool):
    name: str = "FHIRParserTool"
    description: str = "Parses FHIR (Fast Healthcare Interoperability Resources) data to extract relevant patient information for medical claim processing."    
    def _run(self, fhir_data: dict) -> dict:
        return {
            "patient_name": fhir_data.get("name", "Unknown"),
            "age": fhir_data.get("age", "Unknown"),
            "diagnosis": fhir_data.get("diagnosis", "Unknown"),
            "ICD_code": fhir_data.get("ICD_code", "Unknown"),
            "CPT_code": fhir_data.get("CPT_code", "Unknown"),
            "estimated_cost": fhir_data.get("estimated_cost", "Unknown"),
            "insurer": fhir_data.get("insurer", "Unknown"),
            "policy_number": fhir_data.get("policy_number", "Unknown")
        }


class CostEstimatorTool(BaseTool):
    name: str = "CostEstimatorTool"
    description: str = "Estimates the cost of medical procedures based on CPT codes and insurer policies. This tool provides a cost estimate for a given CPT code and checks if escalation is required based"
    def _run(self, CPT_code: str, policy_id: str = None) -> dict:
        base_cost = {
            "99213": 100000,
            "99214": 150000,
            "99215": 200000
        }
        cost = base_cost.get(CPT_code, 100000)  # Default cost if CPT code not listed
        return {
            "CPT_code": CPT_code,
            "estimated_cost": cost,
            "escalation_required": cost > 250000
        }


