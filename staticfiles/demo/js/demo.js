document.addEventListener("submit", (e) => {
  
  // Prevent the default form submit
  e.preventDefault();
  
  // Check file size
  const fileInput = document.getElementById("fileInput");
  const fileSize = fileInput.files[0].size;
  const maxSize = 1024 * 1024 * 5; // 5MB

  if (fileSize > maxSize) {
    alert("File size must be less than 5MB (!)");
    return ; // exit the function
  }
  
  // Store reference to form to make later code easier to read
  const form = e.target;
  console.log
  
  data = {
    method: "POST",
    headers: {
      Authorization: `Token ${localStorage.getItem("token")}`,
    },
    body: new FormData(form)
  };


  // Spinner-show
  spinnerUI('block')

  // Post data using the Fetch API
  fetch("/api/upload/", data)
    .then((res) => {
      if(res.status != 200){
        showMessage('A problem has occured. Try again', 'danger');
        // Spinner-hide
        spinnerUI('none')
        return;
      }
      return res.json()})

    .then((final) => {
      showMessage(final["message"], 'success')
      showResults(final['result'])
      // hide spinner
      spinnerUI('none')
      })

});

function spinnerUI(status){
  document.querySelector('.main-spinner').setAttribute('style',`display: ${status}` )
}

function showMessage(msg, type) {
  document.getElementById("message").outerHTML = `
  <div id="message"> 
        <div
          class="alert alert-dismissible alert-${type}"
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
    document.getElementById("results").innerHTML = JSON.stringify(
      results,
      null,
      10
    );
  }
  console.log("results: ", results);
}

function checkFile() {
  const fileInput = document.getElementById("fileInput");
  const fileSize = fileInput.files[0].size;
  const maxSize = 1024 * 1024 * 5; // 5MB

  if (fileSize > maxSize) {
    alert("File size must be less than 5MB");
  } else {
    // Upload the file
  }
}



function preview() {
  frame.src = URL.createObjectURL(event.target.files[0]);
}