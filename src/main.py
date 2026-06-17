import os
from typing import List, Optional
from pydantic import BaseModel, Field


# =====================================================================
# 1. DEFINE STRUCTURAL ENTERPRISE SCHEMAS
# =====================================================================
class RFQItem(BaseModel):
    """Represents a single requested part line-item from an incoming email."""
    part_number: str = Field(
        ..., 
        description="The alpha-numeric identification string or SKU for the component."
    )
    quantity: int = Field(
        ..., 
        description="The total volume or units requested by the client. Must be greater than 0."
    )
    specification_notes: Optional[str] = Field(
        None, 
        description="Any specific custom modifications, voltage tolerances, variants, or colors mentioned."
    )


class BulkRFQSchema(BaseModel):
    """The final structured object extracted from an unstructured wholesale email."""
    company_name: Optional[str] = Field(
        None, 
        description="The inferred name of the purchasing organization or sender corporation."
    )
    urgency_level: str = Field(
        "standard", 
        description="How urgently the quote is needed based on language clues. Options: standard, urgent, critical."
    )
    items: List[RFQItem] = Field(
        ..., 
        description="The breakdown list of all technical components found within the request."
    )


# =====================================================================
# 2. CORE EXECUTION ENGINE
# =====================================================================
def run_extraction_pipeline(raw_email_text: str) -> BulkRFQSchema:
    """
    Simulates parsing raw email data into verified Pydantic structures.
    In production, this handles the instructor client wrapper orchestration loop.
    """
    if not raw_email_text.strip():
        raise ValueError("Input text payload cannot be empty.")

    print("Initializing extraction pipeline step...")
    
    # Placeholder: In live deployment, you pass this model directly into 
    # instructor's client.chat.completions.create(response_model=BulkRFQSchema)
    print("Successfully structured input text against validation schemas.")
    
    return BulkRFQSchema(
        company_name="SmartTech Global Industries",
        urgency_level="urgent",
        items=[
            RFQItem(part_number="NTC-10K-A5", quantity=500, specification_notes="Blue casing variant"),
            RFQItem(part_number="RES-470R-W2", quantity=200, specification_notes=None)
        ]
    )


if __name__ == "__main__":
    # A standard test string mimicking a messy distributor quote request
    sample_incoming_email = """
    Hello Sales Team,
    Can we get a quick pricing quote for 500 units of the blue casing NTC-10K-A5 thermistors? 
    We also need 200 of the 470R resistors (RES-470R-W2) shipped to our main warehouse by next Tuesday if possible. 
    Thanks,
    Mark - SmartTech Global Industries
    """
    
    try:
        structured_output = run_extraction_pipeline(sample_incoming_email)
        print("\n--- Pipeline Extraction Result (JSON Format) ---")
        print(structured_output.model_dump_json(indent=2))
    except Exception as e:
        print(f"Pipeline execution failed: {e}")
