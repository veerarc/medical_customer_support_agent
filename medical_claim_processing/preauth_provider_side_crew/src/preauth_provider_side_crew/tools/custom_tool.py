from crewai.tools import BaseTool
from typing import Type, Dict, Any, List
from pydantic import BaseModel, Field


class CodeLookupInput(BaseModel):
    concept: str = Field(..., description="Clinical concept to map, e.g., 'left knee osteoarthritis'")
    code_type: str = Field(..., description="One of: ICD-10, CPT, DRG")


class CodeLookupTool(BaseTool):
    name: str = "code_lookup"
    description: str = (
        "Deterministic code lookup tool. Performs exact, rule-based, and fallback fuzzy matches against a provided coding reference."
    )
    args_schema: Type[BaseModel] = CodeLookupInput

    def _run(self, concept: str, code_type: str, coding_reference: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Return candidate codes for a concept from a local coding_reference dict."""
        concept_norm = concept.lower().strip()
        results: List[Dict[str, Any]] = []

        if code_type.upper() == "ICD-10":
            for code, desc in coding_reference.get("icd_codes", {}).items():
                if concept_norm == desc.lower() or concept_norm in desc.lower():
                    results.append({"code_type": "ICD-10", "code": code, "description": desc, "confidence": 0.95, "mapping_reason": "exact or substring match"})

        if code_type.upper() == "CPT":
            for code, desc in coding_reference.get("cpt_codes", {}).items():
                if concept_norm == desc.lower() or concept_norm in desc.lower():
                    results.append({"code_type": "CPT", "code": code, "description": desc, "confidence": 0.95, "mapping_reason": "exact or substring match"})

        # simple deterministic fuzzy: token overlap
        if not results:
            tokens = set(concept_norm.split())
            pool = coding_reference.get("icd_codes", {}) if code_type.upper() == "ICD-10" else coding_reference.get("cpt_codes", {})
            for code, desc in pool.items():
                overlap = len(tokens.intersection(set(desc.lower().split())))
                score = overlap / max(1, len(tokens))
                if score >= 0.5:
                    results.append({"code_type": code_type.upper(), "code": code, "description": desc, "confidence": 0.6 + 0.3 * score, "mapping_reason": "token overlap fallback"})

        return results


class SubmitToolInput(BaseModel):
    payload: Dict[str, Any] = Field(..., description="Preauth payload to submit")


class SubmitTool(BaseTool):
    name: str = "submit_preauth"
    description: str = "Simulate submission to insurer portal and return a reference id"
    args_schema: Type[BaseModel] = SubmitToolInput

    def _run(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        ref = hash(str(payload)) % 100000
        return {"status": "submitted", "reference_id": f"REF-{ref}"}

