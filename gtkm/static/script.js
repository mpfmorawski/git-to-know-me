  document.addEventListener("DOMContentLoaded", () => {  
    let nameLabelList = document.querySelectorAll(".profile-name");
    let usernameLabelList = document.querySelectorAll(".profile-username");

    for (const element of nameLabelList){
        element.textContent = "Zmiana Profilu";
    }

    for (const element of usernameLabelList){
        element.textContent = "zmianaprofilu";
    }
  });

/*  const getUserData = function (user_name) {
    fetch(`http://127.0.0.1/github/stats/${user_name}`)
      .then((response) => {
        response.json();
      })
      .then((data) => {
        console.log(data);
      });
  };

  */