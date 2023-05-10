window.addEventListener('load', () => {
    if (localStorage.getItem("token") != null) {
        console.log('Token: ', localStorage.getItem("token"));
        document.getElementById("api-key").innerHTML =  localStorage.getItem("token");
    }
    else {
        document.getElementById("api-key").innerHTML =  'You must to subscribe';
    }
})