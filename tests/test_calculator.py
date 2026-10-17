from decimal import Decimal

import pytest


@pytest.mark.parametrize(
    ("first_number", "second_number", "operation", "expected"),
    [
        ("10", "5", "addition", "15"),
        ("10", "5", "subtraction", "5"),
        ("10", "5", "multiplication", "50"),
        ("10", "5", "division", "2"),
        ("2.5", "1.5", "addition", "4"),
    ],
)
def test_calculate_operations(
    client,
    first_number: str,
    second_number: str,
    operation: str,
    expected: str,
):
    response = client.post(
        "/calculate",
        json={
            "first_number": first_number,
            "second_number": second_number,
            "operation": operation,
        },
    )

    assert response.status_code == 200
    assert Decimal(response.json()["result"]) == Decimal(expected)


def test_division_by_zero_is_rejected(client):
    response = client.post(
        "/calculate",
        json={
            "first_number": "10",
            "second_number": "0",
            "operation": "division",
        },
    )

    assert response.status_code == 422


def test_calculator_page_and_assets_are_served(client):
    page = client.get("/")

    assert page.status_code == 200
    assert "Quick Arithmetic" in page.text
    assert client.get("/static/style.css").status_code == 200
    assert client.get("/static/app.js").status_code == 200