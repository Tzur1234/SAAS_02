window.addEventListener('load', () => {
    
    getUserBillingDetail();
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

    }



});