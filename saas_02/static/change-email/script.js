window.addEventListener("DOMContentLoaded", () => {
  const btn = document.getElementById("submitBtn");
  const alert = document.getElementById("message");

  const email1 = document.getElementById("newEmail");
  const email2 = document.getElementById("confirmNewEmail");

  btn.addEventListener("click", validation);

  // validation
  function validation(e) {
    e.preventDefault();

    email1Value = email1.value;
    email2Value = email2.value;

    if (email1Value == "" || email2Value == "") {
      console.log("input is empty !");
      // show alert !

      alert.innerHTML = `
              <div
            class="alert alert-dismissible alert-error"
          >
            You must fill both input !
            <button
              type="button"
              class="btn-close"
              data-bs-dismiss="alert"
              aria-label="Close"
            ></button>
          </div>            
            `;
    }

    // check if the values are different
    else if (email1Value != email2Value) {
      console.log("not the same !");
      // show alert !

      alert.innerHTML = `
              <div
            class="alert alert-dismissible alert-error"
          >
            You must keep the passwords the same !
            <button
              type="button"
              class="btn-close"
              data-bs-dismiss="alert"
              aria-label="Close"
            ></button>
          </div>            
            `;
    } else {
      // update changes in the backed
      send(email1Value)
      .then(() => {
        updateEmailUI();
      });

    }
  }

  // send email
  async function send(email) {
    // cleare emails from inputs

    data = {
      method: "POST",
      headers: {
        Authorization: `Token ${localStorage.getItem("token")}`,
        "content-type": "application/json",
      },
      body: JSON.stringify({ email: email }),
    };

    const res = await fetch("/api/change-email/", data);
    const final = await res.json();
    console.log(final);
  }

  // ask for the new updated email in the backend
  async function updateEmailUI() {
    // fetch email of the user
    data = {
      method: "GET",
      headers: {
        Authorization: `Token ${localStorage.getItem("token")}`,
        "content-type": "application/json",
      },
    };

    const res = await fetch("/api/get-email/", data);
    const final = await res.json();
    console.log("the new email from backend: ", final.email);

    // update UI
    document.getElementById("staticEmail").setAttribute("value", final.email);

    document.getElementById("newEmail").setAttribute("value", "");
    document.getElementById("confirmNewEmail").setAttribute("value", "");
  }
});
