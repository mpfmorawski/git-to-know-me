let githubUserData = {
  githubName: "Name",
  githubSurname: "Surname",
  githubUsername: "namesurname",
};

const getUserData = function (userName, dataObject) {
    fetch(`http://127.0.0.1:8000/github/stats/general_user`)
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

          let nameLabelList = document.querySelectorAll(".profile-name");
          let usernameLabelList = document.querySelectorAll(".profile-username");

          for (const element of nameLabelList){
              element.textContent = dataObject.githubName + " " + dataObject.githubSurname;
          }

          for (const element of usernameLabelList){
              element.textContent = dataObject.githubUsername;
          }
        } 
      })
      .catch(error => {
        console.error('There has been a problem with fetch operation:', error);
      });
  };
  
const user = `kamilwil`;
getUserData(user, githubUserData);





