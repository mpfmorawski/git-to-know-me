let githubUserData = {
  githubName: "Name",
  githubSurname: "Surname",
  githubUsername: "namesurname",
  githubAvatar: "",
  githubRepoCount: 0,
  githubStarCount: 0,
  githubForkCount: 0
};

/**
 * Fetches data for profile and general statistics panels.
 * @param {*} dataObject
 */
const fetchUserData = function (dataObject) {
    fetch(`/api/stats/general_user`)
      .then((response) => {
        if (!response.ok){
          throw new Error('HTTP response NOT OK');
        }
        return response.json();
      })
      .then((data) => {
        if (!data){
          throw new Error('Data is undefined');
        }
        else{
          dataObject.githubName = data.name;
          dataObject.githubSurname = data.surname;
          dataObject.githubUsername = data.user_name;
          dataObject.githubAvatar = data.avatar_url;
          dataObject.githubRepoCount = data.repos_count;
          dataObject.githubStarCount = data.stargaze_count;
          dataObject.githubForkCount = data.forks_count;

          let nameLabelList = document.querySelectorAll(".profile-name");
          let usernameLabelList = document.querySelectorAll(".profile-username");
          let avatarList = document.querySelectorAll(".profile-picture");

          //update profile panel
          for (const element of nameLabelList){
              element.textContent = dataObject.githubName + " " + dataObject.githubSurname;
          }
          for (const element of usernameLabelList){
              element.textContent = dataObject.githubUsername;
          }
          for (const element of avatarList){
              element.src = dataObject.githubAvatar;
          }


          //update general statistics panel
          document.getElementById("repo-count").textContent = dataObject.githubRepoCount;
          document.getElementById("star-count").textContent = dataObject.githubStarCount;
          document.getElementById("fork-count").textContent = dataObject.githubForkCount;
        } 
      })
      .catch(error => {
        console.error('There has been a problem with fetch operation:', error);
      });
};

/**
 * Fetches data for programming languages chart.
 */
const fetchLanguageData = function () {
  fetch(`/api/stats/languages`)
    .then((response) => {
      if (!response.ok){
        throw new Error('HTTP response NOT OK');
      }
      return response.json();
    })
    .then((data) => {
      if (!data){
        throw new Error('Data is undefined');
      }
      else{
        let langLabels = [];
        let langValues = [];
        let langRepoCount = data.length;
        
        //create languages list and calculate percentages
        for (const repo of data){
          for (const lang of repo['repo_languages']){
            let langName = "";
            if (Object.keys(lang).length > 0){
              langName = Object.keys(lang)[0];
              if (langLabels.includes(langName)){
                langValues[langLabels.indexOf(langName)] += Number(lang[langName]) / Number(langRepoCount) * 100;
              }
              else{
                langLabels.push(langName);
                langValues.push(Number(lang[langName]) / Number(langRepoCount) * 100);
              }
            }   
          }
        }

        //sort obtained data in descending order, limit to 5 items and 1 decimal place
        let langMapped = langLabels.map(function(d, i) {
          return {
            label: d,
            value: langValues[i] || 0
          };
        });
        let sortedLangMapped = langMapped.sort(function(a, b) {
          return b.value-a.value;
        });
        if (sortedLangMapped.length > 5){
          sortedLangMapped.slice(0,5);
        }
        let sortedLangLabels = [];
        let sortedLangValues = [];
        for (const pos of sortedLangMapped){
          sortedLangLabels.push(pos.label);
          sortedLangValues.push(pos.value.toFixed(1));
        };

        //auxilliary data for chart generation
        let colours = ['#e95211', '#c1ba1f', '#19499a', '#0b9280', '#e11024'];
        let chartData = {
          labels: sortedLangLabels,
          datasets: [
            {
              backgroundColor: colours.slice(0,langRepoCount+1),
              borderWidth: 0,
              data: sortedLangValues
            }
          ]
        };
        
        //generate chart and pretty-print its legend
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
                  display: false, //legend to be shown in separate container
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
                if (chart.canvas.id === "lang-chart") { //to make sure legend is applied to the right chart
                  const ul = document.createElement('ul');
                  chart.data.labels.forEach((label, i) => {
                    ul.innerHTML += `
                      <li class="label-${ label.toLowerCase().replaceAll(" ", "") }">
                        <span style="height: 24px; width: 24px; background-color: ${ chart.data.datasets[0].backgroundColor[i] };
                          border-radius: 50%; display: inline-block;"></span>
                        <span class="legend-label">${ label }</span><br>
                        <span class="legend-value">${ chart.data.datasets[0].data[i] }%</span>
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
      } 
    })
    .catch(error => {
      console.error('There has been a problem with fetch operation:', error);
    });
};

fetchUserData(githubUserData);
fetchLanguageData();




