window.addEventListener("load", () => {

  getUserBillingDetail()
    .then((final) => {
      // show window
        showSection(final["membershipType"]);
        return final;
    })
    .then((final) => {
      // show data
      switch (final["membershipType"]) {
        case "free_trial":
          freeTrail(final);
          break;
        case "member":
          isMember(final);
          break;
        case "not_member":
          notMember(final);
          break;
      }
    });
  

});

// fetch API
async function getUserBillingDetail() {
   // send password
   data = {
     method: "GET",
     headers: {
       Authorization: `Token ${localStorage.getItem("token")}`,
       "content-type": "application/json",
     },
   };

   const res = await fetch("/api/billing-detail/", data);
   const final = await res.json();
   console.log(final)
   return final
 }

//  update the section view
function showSection(type) {
  const free_trial = document.getElementById("free_trial");
  const is_member = document.getElementById("is_member");
  const not_member = document.getElementById("not_member");
  const fetch_error = document.getElementById("fetch_error");
  switch (type) {
    case "free_trial":
      free_trial.setAttribute("style", "display: block;");
      is_member.setAttribute("style", "display: none;");
      not_member.setAttribute("style", "display: none;");
      fetch_error.setAttribute("style", "display: none;");
      break;
    case "member":
      free_trial.setAttribute("style", "display: none;");
      is_member.setAttribute("style", "display: block;");
      not_member.setAttribute("style", "display: none;");
      fetch_error.setAttribute("style", "display: none;");
      break;
    case "not_member":
      free_trial.setAttribute("style", "display: none;");
      is_member.setAttribute("style", "display: none;");
      not_member.setAttribute("style", "display: block;");
      fetch_error.setAttribute("style", "display: none;");
      break;
    default:
      console.log('fire default')
      free_trial.setAttribute("style", "display: none;");
      is_member.setAttribute("style", "display: none;");
      not_member.setAttribute("style", "display: none;");
      fetch_error.setAttribute("style", "display: block;");
      break;
  }
}

// insert data
function freeTrail(final) {
  document.getElementById("free_trial_end_date").innerHTML =
    new Date(final["free_trial_end_date"]).toDateString();
  document.getElementById("api_request_count_free").innerHTML =
    final["api_request_count"];
  document.getElementById("amount_due_free").innerHTML =
    final["amount_due"] + "$";
}
// insert data
function isMember(final) {
  document.getElementById("next_billing_date").innerHTML =
    new Date(final["next_billing_date"]).toDateString();
  document.getElementById("api_request_count_member").innerHTML =
    final["api_request_count"];
  document.getElementById("amount_due_member").innerHTML =
    final["amount_due"] + " $";
}
// insert data
function notMember(final) {

}


// Subscribe event
document.querySelectorAll('.subscribe').forEach(element => {
  element.addEventListener("click", () => {
    fetchCheckoutSessionUrl().then((checkout_session_url) => {
      // if the a checkout_session url was returned back
      if (checkout_session_url.checkout_session_url) {
        window.location.replace(checkout_session_url.checkout_session_url);
      }
    });
  });

})





// fetch API
async function fetchCheckoutSessionUrl() {
   // send password
   data = {
     method: "POST",
     headers: {
       Authorization: `Token ${localStorage.getItem("token")}`,
       "content-type": "application/json",
     },
   };

   const res = await fetch("/api/create-checkout-session/", data);
   const checkout_session_url = await res.json();
   console.log("checkout_session_url: ", checkout_session_url);
   return checkout_session_url;
 }


// Cancel subscription event
document.getElementById("cancel-subscription").addEventListener('click', () => {

  sendCancelReq()
    .then(message => {
    console.log(message)
  })
    
})

// send post requst to cancel subscription

async function sendCancelReq() {
      // fetch email of the user
    data = {
      method: "POST",
      headers: {
        Authorization: `Token ${localStorage.getItem("token")}`,
        "content-type": "application/json",
      },
    };

    const res = await fetch("/api/cancel-subscription/", data);
    const final = await res.json();
    return final.message
  }
