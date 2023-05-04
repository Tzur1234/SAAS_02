window.addEventListener("load", () => {
  const input = document.getElementById("fileinput");
  const uploadBtn = document.getElementById("upload-btn");


  //   2
  const onSelectFile = () => upload(input.files[0]);

  // 3
  showLoading()
  setTimeout(hideLoading,3000);

  //   1
  uploadBtn.addEventListener("click", onSelectFile);
});

function showLoading(){
    document.querySelector('#loading').setAttribute('style', "display: block")
  }
  
  function hideLoading(){
    document.querySelector('#loading').setAttribute('style', "display: none")
}


async function upload(file) {
  const token = getToken("admin", "1234");
  data = {
    method: "POST",
    headers: {
      "content-type": "application/json",
      "X-CSRFToken": `${token}`,
    },
    body: JSON.stringify({ file: file }),
  };

  const res = await fetch("/api/demo/", data);
  const final = await res.json();
  hideLoading()
    
}


function showJsonResult(fial)

// return user's token
async function getToken(username, password) {
  data = {
    method: "POST",
    headers: {
      "content-type": "application/json",
    },
    body: JSON.stringify({ username, password }),
  };

  const res = await fetch("/auth-token/", data);
  const final = await res.json();
  console.log(" the token of the admin ", final);
  return final.token;
}
