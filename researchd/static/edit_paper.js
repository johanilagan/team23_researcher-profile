function resetForm() {
    if (confirm('Are you sure you want to reset all changes? This will revert to the original values.')) {
        // Reload the page to reset form to original values
        window.location.reload();
    }
}

// Character counters and file preview
document.addEventListener('DOMContentLoaded', function() {
    // Abstract character counter
    const abstractTextarea = document.querySelector('textarea[name="abstract"]');
    if (abstractTextarea) {
        const maxLength = 2000;
        const counter = document.createElement('div');
        counter.className = 'form-text text-end';
        counter.textContent = `${abstractTextarea.value.length}/${maxLength}`;
        abstractTextarea.parentNode.appendChild(counter);
        
        abstractTextarea.addEventListener('input', function() {
            counter.textContent = `${this.value.length}/${maxLength}`;
            if (this.value.length > maxLength) {
                counter.classList.add('text-danger');
            } else {
                counter.classList.remove('text-danger');
            }
        });
    }
    
    // File preview
    const fileInput = document.querySelector('input[type="file"]');
    const filePreview = document.getElementById('file-preview');
    const fileName = document.getElementById('file-name');
    
    if (fileInput) {
        fileInput.addEventListener('change', function() {
            if (this.files && this.files[0]) {
                fileName.textContent = this.files[0].name;
                filePreview.style.display = 'block';
            } else {
                filePreview.style.display = 'none';
            }
        });
    }
});

