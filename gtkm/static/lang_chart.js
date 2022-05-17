let colours = ['#e95211', '#c1ba1f', '#19499a', '#0b9280', '#e11024'];

let chartData = {
  labels: ['C++', 'HTML', 'Java', 'Python', 'CSS'],
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
  var chartBox = document.getElementById("lang-chart");
  var chartLegendBox = document.getElementById("js-legend");
  if (chartBox) {
    var chart = new Chart(chartBox, {
      type: 'pie',
      data: chartData,
      options: {
        cutoutPercentage: 0,
        plugins: {
          legend: {
            display: false, //legend to be shown in separate container(?)
          },
          tooltip: {
            enabled: false
          }
        },
        responsive: true,
        maintainAspectRatio: true,
      },
      plugins: [{
        beforeInit: function(chart, args, options) {
          // Make sure we're applying the legend to the right chart
          if (chart.canvas.id === "lang-chart") {
            const ul = document.createElement('ul');
            chart.data.labels.forEach((label, i) => {
              ul.innerHTML += `
                <li class="label-${ label.toLowerCase().replaceAll(" ", "") }">
                  <span style="background-color: ${ chart.data.datasets[0].backgroundColor[i] }">${ chart.data.datasets[0].data[i] }</span><br>
                  ${ label }
                </li>
              `;
            });
            if (chartLegendBox){
              return chartLegendBox.appendChild(ul);
            } 
          }
          return;
        }
      }]  
    });    
  }
});


