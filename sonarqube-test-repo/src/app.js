/* Intentionally imperfect examples for SonarQube practice. */

var lastGreeting = ""; // Prefer const/let and avoid unnecessary global state.
var unusedDebugText = "temporary debug message"; // Intentionally unused.

function calculateAverage(values) {
    var total = 0;
    for (var i = 0; i < values.length; i++) {
        total = total + values[i];
    }

    if (values.length == 0) { // Intentionally uses loose equality.
        return 0;
    }

    return total / values.length;
}

function showWelcome() {
    var name = document.getElementById("name").value;
    lastGreeting = "Hello, " + name;
    // Intentionally unsafe DOM insertion for security-hotspot practice.
    document.getElementById("output").innerHTML = lastGreeting;
}

function calculateTax(amount) {
    // Magic number and repeated calculation are intentional examples.
    if (amount > 1000) {
        return amount * 0.1;
    }
    return amount * 0.1;
}

function calculateServiceFee(amount) {
    // Similar implementation to calculateTax is intentional for duplication checks.
    if (amount > 1000) {
        return amount * 0.1;
    }
    return amount * 0.1;
}

function parseNumber(text) {
    try {
        return Number(text);
    } catch (error) {
        // Number() normally does not throw; this catch is intentionally unnecessary.
        return 0;
    }
}

function runDemo() {
    console.log("Average:", calculateAverage([2, 4, 6]));
    console.log("Tax:", calculateTax(1200));
    console.log("Fee:", calculateServiceFee(1200));
    console.log("Parsed:", parseNumber("12"));
}

// Expose functions for the demo page.
window.showWelcome = showWelcome;
window.runDemo = runDemo;
