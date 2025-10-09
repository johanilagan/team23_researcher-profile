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

// Password requirements functionality
document.addEventListener('DOMContentLoaded', function() {
    const passwordField = document.getElementById('password');
    const passwordRequirements = document.getElementById('password-requirements');

    // Password requirements validation
    function checkPasswordRequirements(password) {
        const requirements = {
            length: password.length >= 6,
            uppercase: /[A-Z]/.test(password),
            number: /\d/.test(password),
            special: /[!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]/.test(password)
        };

        return requirements;
    }

    function updatePasswordRequirements(password) {
        const requirements = checkPasswordRequirements(password);
        
        // Update each requirement indicator
        document.getElementById('req-length').innerHTML = 
            `<i class='bx ${requirements.length ? 'bx-check' : 'bx-x'}'></i><span>Minimum 6 characters</span>`;
        
        document.getElementById('req-uppercase').innerHTML = 
            `<i class='bx ${requirements.uppercase ? 'bx-check' : 'bx-x'}'></i><span>At least 1 uppercase letter</span>`;
        
        document.getElementById('req-number').innerHTML = 
            `<i class='bx ${requirements.number ? 'bx-check' : 'bx-x'}'></i><span>At least 1 number</span>`;
        
        document.getElementById('req-special').innerHTML = 
            `<i class='bx ${requirements.special ? 'bx-check' : 'bx-x'}'></i><span>At least 1 special character</span>`;
    }

    // Show/hide password requirements based on focus
    passwordField.addEventListener('focus', function() {
        passwordRequirements.style.display = 'block';
    });

    passwordField.addEventListener('blur', function() {
        // Keep requirements visible if password has content
        if (this.value.length === 0) {
            passwordRequirements.style.display = 'none';
        }
    });

    // Real-time password validation
    passwordField.addEventListener('input', function() {
        updatePasswordRequirements(this.value);
    });
});

