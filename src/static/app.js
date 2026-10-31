const form = document.querySelector("#calculator-form");
const firstNumber = document.querySelector("#first-number");
const secondNumber = document.querySelector("#second-number");
const operation = document.querySelector("#operation");
const result = document.querySelector("#result");
const resultHint = document.querySelector("#result-hint");
const errorMessage = document.querySelector("#error-message");
const clearButton = document.querySelector("#clear-button");
const defaultOperation = "addition";

form.addEventListener("submit", async (event) => {
    event.preventDefault();
    errorMessage.hidden = true;
    errorMessage.textContent = "";

    try {
        const response = await fetch("/calculate", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                first_number: firstNumber.value,
                second_number: secondNumber.value,
                operation: operation.value,
            }),
        });
        const payload = await response.json();

        if (!response.ok) {
            throw new Error(payload.detail || "Unable to calculate with those values.");
        }

        result.textContent = payload.result;
        resultHint.textContent = "Calculation complete.";
    } catch (error) {
        errorMessage.textContent = error.message;
        errorMessage.hidden = false;
    }
});

clearButton.addEventListener("click", () => {
    form.reset();
    operation.value = defaultOperation;
    result.textContent = "";
    resultHint.textContent = "Your answer will appear here.";
    errorMessage.textContent = "";
    errorMessage.hidden = true;
});