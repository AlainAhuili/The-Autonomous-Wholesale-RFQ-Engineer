import pytest
from pydantic import ValidationError
from src.main import RFQItem, BulkRFQSchema, run_extraction_pipeline

def test_rfq_item_validation():
    """Ensure the line-item schema correctly enforces valid inputs."""
    # This should pass cleanly
    item = RFQItem(part_number="NTC-10K", quantity=100, specification_notes="High temp")
    assert item.part_number == "NTC-10K"
    assert item.quantity == 100

    # This should fail because quantity cannot be a string that isn't a digit
    with pytest.raises(ValidationError):
        RFQItem(part_number="NTC-10K", quantity="invalid_volume")


def test_extraction_pipeline_output():
    """Ensure the mock execution pipeline outputs data matching our corporate schema."""
    sample_text = "Need 500 units of SKU-100"
    result = run_extraction_pipeline(sample_text)
    
    assert isinstance(result, BulkRFQSchema)
    assert len(result.items) > 0
    assert result.items[0].quantity == 500


def test_empty_pipeline_payload():
    """Ensure the pipeline throws an explicit error if empty payloads pass through."""
    with pytest.raises(ValueError, match="Input text payload cannot be empty."):
        run_extraction_pipeline("   ")
