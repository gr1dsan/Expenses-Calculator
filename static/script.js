document.addEventListener("DOMContentLoaded", function () {
    const ctx = document.getElementById("expensesPieChart").getContext("2d");

    const data = {
        labels: [
            "Groceries",
            "Restaurants & Cafés",
            "Pharmacy & Health Products",
            "Public Transport",
            "Others"
        ],
        datasets: [{
            label: "Expenses Breakdown",
            data: [
                parseFloat("{{ grocery_percent }}"),
                parseFloat("{{ restourants_percent }}"),
                parseFloat("{{ pharmacy_percent }}"),
                parseFloat("{{ public_transport_percent }}"),
                parseFloat("{{ other_percent }}")
            ],
            backgroundColor: [
                "#FFB347", // Groceries
                "#FF6961", // Restaurants
                "#77DD77", // Pharmacy
                "#779ECB", // Public Transport
                "#CFCFC4"  // Others
            ],
            borderWidth: 1
        }]
    };

    new Chart(ctx, {
        type: "pie",
        data: data,
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: "bottom"
                }
            }
        }
    });
});