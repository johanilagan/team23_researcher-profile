function resetForm() {
    if (confirm('Are you sure you want to reset all changes? This will restore the original values.')) {
        document.querySelector('form').reset();
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
});

