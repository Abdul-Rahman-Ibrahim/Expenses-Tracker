document.addEventListener("DOMContentLoaded", function () {
    const chartCanvas = document.getElementById('expenseChart').getContext('2d');
    let expenseChart;

    function fetchAndRenderChart(numMonths) {
        fetch("/expense_category_summary/", {
            method: 'POST',
            headers: {
                'X-CSRFToken': '{{ csrf_token }}',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ num_months: numMonths })
        })
            .then(response => response.json())
            .then(data => {
                const expenseData = data.expense_category_data;
                const labels = Object.keys(expenseData);
                const values = Object.values(expenseData);

                if (expenseChart) expenseChart.destroy();

                expenseChart = new Chart(chartCanvas, {
                    type: 'doughnut',
                    data: {
                        labels: labels,
                        datasets: [{
                            label: 'Expenses',
                            data: values,
                            backgroundColor: [
                                '#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0',
                                '#9966FF', '#FF9F40', '#E7E9ED'
                            ],
                            borderWidth: 1
                        }]
                    },
                    options: {
                        responsive: true,
                        plugins: {
                            legend: { position: 'bottom' }
                        },
                        title: {
                            display: true,
                            text: 'Expense per category',
                        },
                    }
                });

                document.querySelector('h2').textContent = `Expenses by Category (Last ${numMonths} Months)`;
            });
    }

    const selectElement = document.getElementById('numMonths');
    selectElement.addEventListener('change', () => {
        const selectedMonths = selectElement.value;
        fetchAndRenderChart(selectedMonths);
    });

    // Load initial chart (default to 6 months)
    fetchAndRenderChart(6);
});
