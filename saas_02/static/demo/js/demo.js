// window.addEventListener("load", () => {
//   const input = document.getElementById("fileinput");
//   const uploadBtn = document.getElementById("upload-btn");


//   //   2
//   const onSelectFile = () => upload(input.files[0]);

//   // 3
//   showLoading()
//   setTimeout(hideLoading,3000);

   //   1
// uploadBtn.addEventListener("click", onSelectFile);
// });

// function showLoading(){
//     document.querySelector('#loading').setAttribute('style', "display: block")
//   }
  
// function hideLoading() {
//   document.querySelector('#loading').setAttribute('style', "display: none")
// }





document.addEventListener("submit", (e) => {
  // Store reference to form to make later code easier to read
  const form = e.target;

  data = {
    method: 'POST',
    body: new FormData(form),
  };

  // Post data using the Fetch API
  fetch('/api/demo/', data)
    .then(res => res.json())
    .then(final => {
      console.log(final)
      showMessage(final['message'])
      showResults(final['result'])
    })

  // Prevent the default form submit
  e.preventDefault();
});

function showMessage(msg) {
  document.getElementById("message").outerHTML = `
  <div id="message"> 
        <div
          class="alert alert-dismissible alert-warning"
        >
          ${msg}
          <button
            type="button"
            class="btn-close"
            data-bs-dismiss="alert"
            aria-label="Close"
          ></button>
        </div>
      </div>  
  `;
}

function showResults(results) {
  if (results != null) {
    document.getElementById('results').innerHTML = JSON.stringify(results, null, 10)
  }
  console.log('results: ', results)
}

// later on: to add loader graphics when uploading the data