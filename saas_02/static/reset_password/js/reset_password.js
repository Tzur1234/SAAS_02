window.addEventListener('load', ()=>{
    

    const currentPasswordInput = document.getElementById("id_oldpassword");
    const Password1Input = document.getElementById("id_password1");
    const Password2Input = document.getElementById("id_password2");
    const btnReset = document.getElementById("btnReset");

    btnReset.addEventListener('click', resetPassword)


    async function resetPassword(){

        passwordsDic = {
            current_password:currentPasswordInput.value,
            password1: Password1Input.value,
            password2: Password2Input.value
        }
      
        
        // send password
        data = {
          method: "POST",
          headers: {
            Authorization: `Token ${localStorage.getItem("token")}`,
            "content-type": "application/json",
          },
          body: JSON.stringify(passwordsDic),
        };

        spinnerUI('block')
        const res = await fetch("/api/password-reset/", data);
        const final = await res.json();
        spinnerUI('none')
        

        if(res.status !== 200){
            showAlert(final["Response message"]);
        }else{
          // Password successfully changed.
          showSuccessAlert("Password successfully changed.");
          document.getElementById("id_oldpassword").value = ''
          document.getElementById("id_password1").value = ''
          document.getElementById("id_password2").value = ''
        
          
        }
        
    }
    
    function showAlert(final){
        const alert = document.getElementById("message");
        alert.innerHTML = `
              <div
            class="alert alert-dismissible alert-error"
          >
            ${final}
            <button
              type="button"
              class="btn-close"
              data-bs-dismiss="alert"
              aria-label="Close"
            ></button>
          </div>            
            `
    }
    function showSuccessAlert(message){
        const alert = document.getElementById("message");
        alert.innerHTML = `
             <div class="alert alert-dismissible alert-success">
          ${message}
          <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        </div>`
    }

    function spinnerUI(status){
      document.querySelector('.main-spinner').setAttribute('style',`display: ${status}` )
    }





});


