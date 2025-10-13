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
        
        // Clear error message if present
        const passwordContainer = passwordField.closest('.password-container');
        const inputDiv = passwordContainer.parentElement;
        const errorMessage = inputDiv.querySelector('.password-error');
        
        if (errorMessage) {
            const requirements = checkPasswordRequirements(this.value);
            const allRequirementsMet = requirements.length && 
                                      requirements.uppercase && 
                                      requirements.number && 
                                      requirements.special;
            if (allRequirementsMet) {
                errorMessage.remove();
            }
        }
    });
    
    // Form submission validation
    const registerForm = document.getElementById('register-form');
    if (registerForm) {
        registerForm.addEventListener('submit', function(e) {
            const password = passwordField.value;
            const requirements = checkPasswordRequirements(password);
            
            // Check if all requirements are met
            const allRequirementsMet = requirements.length && 
                                      requirements.uppercase && 
                                      requirements.number && 
                                      requirements.special;
            
            if (!allRequirementsMet) {
                e.preventDefault();
                
                // Show password requirements
                passwordRequirements.style.display = 'block';
                
                // Show error message (insert after password-container, not inside it)
                const passwordContainer = passwordField.closest('.password-container');
                const inputDiv = passwordContainer.parentElement;
                let errorMessage = inputDiv.querySelector('.password-error');
                
                if (!errorMessage) {
                    errorMessage = document.createElement('div');
                    errorMessage.className = 'text-danger password-error mt-2';
                    // Insert after the password-container div
                    passwordContainer.parentNode.insertBefore(errorMessage, passwordContainer.nextSibling);
                }
                errorMessage.textContent = 'Password does not meet all requirements. Please check the requirements above.';
                
                // Scroll to password field
                passwordField.focus();
                passwordField.scrollIntoView({ behavior: 'smooth', block: 'center' });
                
                return false;
            }
        });
    }
    
    // Institution dropdown handler - show/hide other institution field
    const institutionSelect = document.getElementById('institution-select');
    const otherInstitutionDiv = document.getElementById('other-institution-div');
    
    if (institutionSelect && otherInstitutionDiv) {
        institutionSelect.addEventListener('change', function() {
            if (this.value === 'Other') {
                otherInstitutionDiv.style.display = 'block';
            } else {
                otherInstitutionDiv.style.display = 'none';
            }
        });
        
        // Check initial state on page load
        if (institutionSelect.value === 'Other') {
            otherInstitutionDiv.style.display = 'block';
        }
    }
    
    // Position dropdown handler - show/hide other position field
    const positionSelect = document.getElementById('position-select');
    const otherPositionDiv = document.getElementById('other-position-div');
    
    if (positionSelect && otherPositionDiv) {
        positionSelect.addEventListener('change', function() {
            if (this.value === 'Other') {
                otherPositionDiv.style.display = 'block';
            } else {
                otherPositionDiv.style.display = 'none';
            }
        });
        
        // Check initial state on page load
        if (positionSelect.value === 'Other') {
            otherPositionDiv.style.display = 'block';
        }
    }
});

