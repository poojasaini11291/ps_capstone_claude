from decimal import Decimal

from src.schemas import Operation


def calculate(
    first_number: Decimal,
    second_number: Decimal,
    operation: Operation,
) -> Decimal:
    if operation == "addition":
        return first_number + second_number
    if operation == "subtraction":
        return first_number - second_number
    if operation == "multiplication":
        return first_number * second_number
    if operation == "division":
        if second_number == 0:
            raise ValueError("The second number must not be zero for division.")
        return first_number / second_number
    raise ValueError("Unsupported operation.")