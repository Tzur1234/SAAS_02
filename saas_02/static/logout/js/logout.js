window.addEventListener("DOMContentLoaded", function () {
    
    const btn = document.getElementById("submitBtn");
    btn.addEventListener('click', (e) => {
        e.preventDefault()
        
        // delete the token
        localStorage.removeItem('token')
        console.log( 'know the token:' ,localStorage.getItem('token'))

        // submit btn
        document.querySelector('form').submit()
    })
})