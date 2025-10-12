function resetForm() {
    if (confirm('Are you sure you want to reset all changes? This will restore the original values.')) {
        document.querySelector('form').reset();
        // Reset profile picture preview
        const preview = document.getElementById('profile-pic-preview');
        if (preview && preview.dataset.originalSrc) {
            preview.src = preview.dataset.originalSrc;
        }
    }
}

// Profile picture preview
function previewProfilePicture(input) {
    if (input.files && input.files[0]) {
        const reader = new FileReader();
        const preview = document.getElementById('profile-pic-preview');
        
        // Store original src for reset
        if (!preview.dataset.originalSrc) {
            preview.dataset.originalSrc = preview.src;
        }
        
        reader.onload = function(e) {
            preview.src = e.target.result;
        };
        
        reader.readAsDataURL(input.files[0]);
    }
}

// Character counter for bio
document.addEventListener('DOMContentLoaded', function() {
    const bioTextarea = document.querySelector('textarea[name="bio"]');
    if (bioTextarea) {
        const maxLength = 1000;
        const counter = document.createElement('div');
        counter.className = 'form-text text-end';
        counter.textContent = `${bioTextarea.value.length}/${maxLength}`;
        bioTextarea.parentNode.appendChild(counter);
        
        bioTextarea.addEventListener('input', function() {
            counter.textContent = `${this.value.length}/${maxLength}`;
            if (this.value.length > maxLength) {
                counter.classList.add('text-danger');
            } else {
                counter.classList.remove('text-danger');
            }
        });
    }
    
    // Institution dropdown handler - show/hide other institution field
    const institutionSelect = document.getElementById('institution-select-edit');
    const otherInstitutionRow = document.getElementById('other-institution-row-edit');
    
    if (institutionSelect && otherInstitutionRow) {
        institutionSelect.addEventListener('change', function() {
            if (this.value === 'Other') {
                otherInstitutionRow.style.display = 'block';
            } else {
                otherInstitutionRow.style.display = 'none';
            }
        });
        
        // Check initial state on page load
        if (institutionSelect.value === 'Other') {
            otherInstitutionRow.style.display = 'block';
        }
    }
});

