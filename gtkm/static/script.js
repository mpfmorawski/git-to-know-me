let githubUserData = {
  githubName: "Name",
  githubSurname: "Surname",
  githubUsername: "namesurname",
  githubAvatar: "",
  githubRepoCount: 0,
  githubStarCount: 0,
  githubForkCount: 0
};

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

let repoDataSortedByCommit = [];
let repoDataSortedByStars = [];
let repoDataSortedByContrib = [];
const dateOptions = {
  month: "long",
  day: "numeric",
  year: "numeric"
};

/**
 * Replaces current top repos panel content with top repos data with chosen sorting
 * @param {*} sortType Sorting type chosen from the dropdown
 */
const refreshReposList = function (sortType) {
  //set appropriate repo data depending on sorting type chosen in dropdown
  let sortRepoList = [];
  let sortTypeText = "";
  let sortTypeValue = 0;
  if (sortType === "most popular"){
    try {
      sortRepoList = repoDataSortedByStars;
      sortTypeText = "stars:";
      sortTypeValue = 1;
    } catch (error) {
      console.log(error);
    }   
  }
  else if (sortType === "most contributed to"){
    try {
      sortRepoList = repoDataSortedByContrib;
      sortTypeText = "contributions:";
      sortTypeValue = 2;
    } catch (error) {
      console.log(error);
    }
  }
  else{
    try {
      sortRepoList = repoDataSortedByCommit;
      sortTypeText = "last commit:";
      sortTypeValue = 0;
    } catch (error) {
      console.log(error);
    }
  }

  //flush current top repos panel content
  let repoPanel = document.getElementById("js-repos");
  repoPanel.innerHTML = "<!-- Here come repo-box divs generated by script.js -->";

  //create HTML blocks with acquired and sorted data
  for (const repo of sortRepoList){
    let sortValueText = [repo.last.toLocaleDateString("en-US", dateOptions), repo.star, repo.contrib];
    
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
      <span class="sort-title">${sortTypeText}</span><br>
      <span class="sort-value">${sortValueText[sortTypeValue]}</span>
    </div>
    `;
    if (repoPanel){
      repoPanel.appendChild(div);
    } 
  }
  return;
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
        let otherValue = 0;
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
          let otherLangMapped = sortedLangMapped.slice(4,-1);
          sortedLangMapped = sortedLangMapped.slice(0,5);
          for (const lang of otherLangMapped){
            otherValue += lang.value;
          }
        }
        let sortedLangLabels = [];
        let sortedLangValues = [];
        for (const pos of sortedLangMapped){
          sortedLangLabels.push(pos.label);
          sortedLangValues.push(pos.value.toFixed(1));
        };
        sortedLangLabels.push("Other");
        sortedLangValues.push(otherValue.toFixed(1));

        //auxilliary data for chart generation
        let colours = ['#e95211', '#c1ba1f', '#19499a', '#0b9280', '#e11024', '#797979'];
        let chartData = {
          labels: sortedLangLabels,
          datasets: [
            {
              backgroundColor: colours.slice(0,sortedLangMapped.length+1),
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
        //create a list with information for each repo
        let repoDataList = [];

        for (const repo of data){
          let repoData = new RepoData(repo.repo_url, repo.repository_name, repo.repo_owner, repo.stargaze_count, 
            repo.forks_count, repo.watchers_count, repo.contributors_count, new Date(repo.last_user_commit));
          repoDataList.push(repoData);
        }
        
        //sort the list by last commit date, sort in descending order and limit to 5 repos
        repoDataSortedByCommit = [...repoDataList.sort(function(a, b) {
          return b.last-a.last;
        })];
        if (repoDataSortedByCommit.length > 5){
          repoDataSortedByCommit = repoDataSortedByCommit.slice(0,5);
        }

        //sort the list in two another ways (most popular = stars, most contributed to = ?)
        repoDataSortedByStars = [...repoDataList.sort(function(a, b) {
          return b.star-a.star;
        })];
        if (repoDataSortedByStars.length > 5){
          repoDataSortedByStars = repoDataSortedByStars.slice(0,5);
        }

        repoDataSortedByContrib = [...repoDataList.sort(function(a, b) {
          return b.contrib-a.contrib;
        })];
        if (repoDataSortedByContrib.length > 5){
          repoDataSortedByContrib = repoDataSortedByContrib.slice(0,5);
        }
        
        //create HTML blocks with acquired and sorted data
        refreshReposList("with latest activity");
      }
    })
    .catch(error => {
      console.error('There has been a problem with fetch operation:', error);
    });
};

fetchUserData(githubUserData);
fetchLanguageData();
fetchRepoData();



// refresh top repos list on dropdown click
$('.dropdown-item').click(function() {
  let chosenSortType = $(this).text();
  console.log(chosenSortType);
  document.getElementById("js-sort-button").innerHTML = `<span class="caret"></span>${chosenSortType}`;
  refreshReposList(chosenSortType);
});


