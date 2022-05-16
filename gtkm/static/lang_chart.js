let colours = ['#e95211', '#c1ba1f', '#19499a', '#0b9280', '#e11024'];

const chartOptions = {
  cutoutPercentage: 0,
  plugins: {
    legend: {
      display: false, //legend to be shown in separate container(?)

      position:'right', 
      labels: {
        pointStyle:'circle',
        usePointStyle: true,
        font: {
          family: 'Lato',
          style: 'normal',
          weight: 400,
          size: 24
        }
      },
      textAlign: 'left'
    },
    tooltip: {
      enabled: false
    }
  },
  responsive: true,
  maintainAspectRatio: true
};

let chartData = {
  labels: ['Bootstrap', 'Popper', 'Other', 'Placeholder1', 'Placeholder2'],
  datasets: [
    {
      backgroundColor: colours.slice(0,5),
      borderWidth: 0,
      data: [74, 55, 40, 22, 15]
    }
  ]
};

//is asynchronous loading desirable here?
window.addEventListener('DOMContentLoaded', (event) => {
    let langChart = document.getElementById("lang-chart");
    if (langChart) {
        new Chart(langChart, {
            type: 'pie',
            data: chartData,
            options: chartOptions
        });
    }
});


