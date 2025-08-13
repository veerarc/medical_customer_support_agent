from typing import Type

from crewai.tools import BaseTool
from pydantic import BaseModel, Field


class MyCustomToolInput(BaseModel):
    """Input schema for MyCustomTool."""

    argument: str = Field(..., description="Description of the argument.")


class MyCustomTool(BaseTool):
    name: str = "Name of my tool"
    description: str = (
        "Clear description for what this tool is useful for, your agent will need this information to use it."
    )
    args_schema: Type[BaseModel] = MyCustomToolInput

    def _run(self, argument: str) -> str:
        # Implementation goes here
        return "this is an example of a tool output, ignore it and move along."
    
class JSONValidatorToolInput(BaseModel):
    """Input schema for JSONValidatorTool."""
    argument: dict = Field(..., description="JSON data to validate against required fields.")

class JSONValidatorTool(BaseTool):
    name: str = "JSONValidatorTool"
    description: str  = "Validates the structure of a JSON object to ensure it contains all required fields for medical claim processing. This tool checks for the presence of specific fields in the JSON data."
    
    REQUIRED_FIELDS: list = ["patient_name", "age", "diagnosis", "ICD_code", "CPT_code", "estimated_cost", "insurer", "policy_number"]
    args_schema: Type[BaseModel] = JSONValidatorToolInput

    def _run(self, argument: dict) -> str:
        missing = [field for field in self.REQUIRED_FIELDS if field not in argument or argument[field] in (None, "")]
        if missing:
            return f"Missing or empty fields: {', '.join(missing)}"
        return "All required fields are present and valid."
    
    
# json_validator_tool = JSONValidatorTool()
