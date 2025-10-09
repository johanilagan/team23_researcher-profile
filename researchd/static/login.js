// Simple password toggle function
function togglePassword(fieldId) {
    const passwordField = document.getElementById(fieldId);
    const eye = passwordField.parentElement.querySelector('.toggle-eye');

    if (passwordField.type === "password") {
        passwordField.type = "text";
        eye.classList.remove('bx-eye-slash');
        eye.classList.add('bx-eye');
    } else {
        passwordField.type = "password";
        eye.classList.remove('bx-eye');
        eye.classList.add('bx-eye-slash');
    }
}

