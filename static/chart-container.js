const gridColor = "#33ccff";
const tickColor = "#66ff99";
const tickFontSize = 18;
const lineColor = "#fa8072";

class ChartContainer {
    config = {
        type: "scatter",
        data: {
            datasets: [
                {
                    borderColor: lineColor,
                    backgroundColor: lineColor,
                    showLine: true,
                    pointRadius: 0
                }
            ]
        },
        options: {
            responsive: true,
            animation: {
                duration: 0
            },
            plugins: {
                legend: {
                    display: false
                },
                title: {
                    display: false,
                }
            },
            scales: {
                y: {
                    grid: {
                        color: gridColor
                    },
                    ticks: {
                        color: tickColor,
                        callback: x => `$${x.toFixed(2)}`,
                        font: {
                            size: tickFontSize
                        }
                    }
                },
                x: {
                    grid: {
                        color: gridColor
                    },
                    ticks: {
                        color: tickColor,
                        display: false
                    }
                }
            }
        },
    }

    constructor(context) {
        this.chart = new Chart(context, this.config);
    }

    setValues(data) {
        const values = data
        .map((value, index) => ({
            x: index,
            y: value
        }))
        this.chart.data.datasets[0].data = values;
        this.chart.update();
    }

    addValue(value) {

    }
}