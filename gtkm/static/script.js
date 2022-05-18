let githubUserData = {
  githubName: "Name",
  githubSurname: "Surname",
  githubUsername: "namesurname",
  githubAvatar: "",
  githubRepoCount: 0,
  githubStarCount: 0,
  githubForkCount: 0
};

const fetchUserData = function (dataObject) {
    fetch(`/github/stats/general_user`)
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
  
fetchUserData(githubUserData);





