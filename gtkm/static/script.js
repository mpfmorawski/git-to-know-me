let githubUserData = {
  githubName: "Name",
  githubSurname: "Surname",
  githubUsername: "namesurname",
  githubAvatar: "",
  githubRepoCount: 0,
  githubStarCount: 0,
  githubForkCount: 0
};

/*let githubRepoData = {
  repoUrl: "",
  repoName: "",
  repoOwner: "",
  repoStarCount: 0,
  repoForkCount: 0,
  repoWatchCount: 0,
  repoContribCount: 0,
  repoLastCommit: ""
}*/

class RepoData {
  constructor(url, name, owner, star, fork, watch, contrib, last) {
    this.url = url;
    this.name = name;
    this.owner = owner;
    this.star = star;
    this.fork = fork;
    this.watch = watch;
    this.contrib = contrib;
    this.last = last;
  }
}

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

/**
 * Fetches data for top repositories panel.
 */
 const fetchRepoData = function () {
  fetch(`/api/stats/top_repos`)
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
        /*dataObject.repoUrl = data.repo_url;
        dataObject.repoName = data.repository_name;
        dataObject.repoOwner = data.repo_owner;
        dataObject.repoStarCount = data.stargaze_count;
        dataObject.repoForkCount = data.forks_count;
        dataObject.repoWatchCount = data.watchers_count;
        dataObject.repoContribCount = data.contributors_count;
        dataObject.repoLastCommit = data.last_user_commit;
        */

        //create a list with information for each repo
        let repoDataList = [];
        for (const repo of data){
          let repoData = new RepoData(repo.repo_url, repo.repository_name, repo.repo_owner, repo.stargaze_count, 
            repo.forks_count, repo.watchers_count, repo.contributors_count, new Date(repo.last_user_commit));
          repoDataList.push(repoData);
        }
        
        //sort the list by last commit date and sort in descending order
        let repoDataSortedByCommit = repoDataList.sort(function(a, b) {
          return b.last-a.last;
        });

        //sort the list in two another ways (most popular = stars, most contributed to = ?)
        
        //create HTML blocks with acquired and sorted data
        let repoPanel = document.getElementById("js-repos");
        for (const repo of repoDataSortedByCommit){
          const div = document.createElement('div');
          div.className = "repo-box";
          div.innerHTML += `
          <img src="images/prototype_screenshot 1.png" class="repo-picture" />
          <div class="repo-data">
            <img src="images/GitHub-Mark-32px.png" alt=""><span class="repo-username">${repo.owner}</span><br>
            <a href="${repo.url}" class="repo-url">${repo.name}</a>
            <div class="repo-stats">
              <div class="stats-slot">
                <img src="images/star_logo.png" class="stats-logo"><span class="stats-value">${repo.star}</span>
              </div>
              <div class="stats-slot">
                <img src="images/fork_logo.png" class="stats-logo"><span class="stats-value">${repo.fork}</span>
              </div>
              <div class="stats-slot">
                <img src="images/eye_logo.png" class="stats-logo"><span class="stats-value">${repo.watch}</span>
              </div>
              <div class="stats-slot">
                <img src="images/contrib_logo.png" class="stats-logo"><span class="stats-value">${repo.contrib}</span>
              </div>
            </div>
          </div>
          <div class="sort-data">
            <span class="sort-title">last commit:</span><br>
            <span class="sort-value">${repo.last.toString()}</span>
          </div>
          `;
          if (repoPanel){
            return repoPanel.appendChild(div);
          } 
        }
      }
    })
    .catch(error => {
      console.error('There has been a problem with fetch operation:', error);
    });
};

fetchUserData(githubUserData);
fetchLanguageData();
fetchRepoData();




