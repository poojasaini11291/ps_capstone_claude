from fastapi import APIRouter, HTTPException

from src.calculator import calculate
from src.schemas import CalculationRequest, CalculationResponse

router = APIRouter()


@router.post("/calculate", response_model=CalculationResponse)
def calculate_numbers(request: CalculationRequest) -> CalculationResponse:
    try:
        result = calculate(
            request.first_number,
            request.second_number,
            request.operation,
        )
    except ValueError as error:
        raise HTTPException(status_code=422, detail=str(error)) from error

    return CalculationResponse(result=format(result.normalize(), "f"))