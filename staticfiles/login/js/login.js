window.addEventListener("DOMContentLoaded", function () {
  console.log("Hello World!");

  const usernameInput = document.getElementById("id_login");
  const passwordInput = document.getElementById("id_password");
  
 
    // add event 
    const btnSubmit = document.getElementById("submitBtn");
    btnSubmit.addEventListener('click', (e) => {
        e.preventDefault()

        if(usernameInput.value != "" && passwordInput.value != ""){
            getAndSetToken(usernameInput.value, passwordInput.value);
            
        }
        
    })
 
 
  // fethc a token
//   if the user exists - add the token to localStorage
//   anyway the form will be submmited
  async function getAndSetToken(username, password) {
    data = {
      method: "POST",
      headers: {
        "content-type": "application/json",
      },
      body: JSON.stringify({ username, password }),
    };

    try{
        const res = await fetch("/auth-token/", data);

        if(res.status != 200){
            throw new Error('the username or password are not authenticated!')
        }

        const final = await res.json();
        console.log(" the token of the admin ", final.token);
        localStorage.setItem("token", final.token);
    }
    catch(error){
        console.log('Error: ', error)
        console.log("token wasn't added !");
    }
   
    
    // submit the form
    console.log("token was added !")
    document.querySelector("form").submit()

  }

//   function addTokenToStorage(token) {
//     // check if token exist
//     if (localStorage.getItem("token") != null) {
//       // delete token
//       localStorage.removeItem("token");
//     }
//     // add the token to localStorage
//     console.log(token)
//     localStorage.setItem("token", token);
//   }
});
