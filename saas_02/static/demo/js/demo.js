document.addEventListener("submit", (e) => {
   // Spinner-show
   document.querySelector('.main-spinner').setAttribute('style','display: block' )

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

  // Post data using the Fetch API
  fetch("/api/upload/", data)
    .then((res) => res.json())
    .then((final) => {
      console.log(final.errors);
      showMessage(final["message"]);
      showResults(final["result"]);
    })
    .then(( ()=> {
       // Spinner-hide
    document.querySelector('.main-spinner').setAttribute('style','display: none' )
    }));
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
// later on: to add loader graphics when uploading the data
