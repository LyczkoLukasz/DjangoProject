// checking if the password and confirm password are same or not
document.getElementById('credentials').addEventListener('submit', function(event) {
    var password1 = document.getElementById('password1').value;
    var password2 = document.getElementById('password2').value;
    /*
    if (password1 !== password2) {
        event.preventDefault();
        document.getElementById('message').textContent = 'Passwords do not match!';
    }
    else {
        document.getElementById('message').textContent = '';
    }*/
});
