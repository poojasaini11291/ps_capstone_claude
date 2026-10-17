from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, ConfigDict


Operation = Literal["addition", "subtraction", "multiplication", "division"]


class CalculationRequest(BaseModel):
    first_number: Decimal
    second_number: Decimal
    operation: Operation


class CalculationResponse(BaseModel):
    result: str
