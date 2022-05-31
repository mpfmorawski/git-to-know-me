let githubUserData = {
  githubName: "Name",
  githubSurname: "Surname",
  githubUsername: "namesurname",
  githubAvatar: "",
  githubRepoCount: 0,
  githubStarCount: 0,
  githubForkCount: 0
};

let githubLanguageData = {
  languagesList: []
};

let langLabels = [];
let langValues = [];

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
          dataObject.githubRepoCount = data.repos_count;
          dataObject.githubStarCount = data.stargaze_count;
          dataObject.githubForkCount = data.forks_count;

          let nameLabelList = document.querySelectorAll(".profile-name");
          let usernameLabelList = document.querySelectorAll(".profile-username");

          for (const element of nameLabelList){
              element.textContent = dataObject.githubName + " " + dataObject.githubSurname;
          }

          for (const element of usernameLabelList){
              element.textContent = dataObject.githubUsername;
          }

          document.getElementById("repo-count").textContent = dataObject.githubRepoCount;
          document.getElementById("star-count").textContent = dataObject.githubStarCount;
          document.getElementById("fork-count").textContent = dataObject.githubForkCount;
        } 
      })
      .catch(error => {
        console.error('There has been a problem with fetch operation:', error);
      });
};

const fetchLanguageData = function (dataObject) {
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
        let languagesList = data;
        //console.log(languagesList[0]['repo_languages'][0]['C']);
        let langRepoCount = languagesList.length;
        for (const repo of languagesList){
          for (const lang of repo['repo_languages']){
            let langName = "";
            if (Object.keys(lang).length > 0){
              langName = Object.keys(lang)[0];
              //console.log(langName);
              //console.log(lang[langName]);
              if (langLabels.includes(langName)){
                langValues[langLabels.indexOf(langName)] += Number(lang[langName] / Number(langRepoCount));
              }
              else{
                langLabels.push(langName);
                langValues.push(Number(lang[langName]) / Number(langRepoCount));
              }
            }   
          }
        }

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
          sortedLangValues.push(pos.value);
        };
        
        console.log(sortedLangLabels);
        console.log(sortedLangValues);

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

      } 
    })
    .catch(error => {
      console.error('There has been a problem with fetch operation:', error);
    });
};

export function importLanguageLabels(){
  return langLabels;
}

export function importLanguageValues(){
  return langValues;
}

fetchUserData(githubUserData);
fetchLanguageData(githubLanguageData);




