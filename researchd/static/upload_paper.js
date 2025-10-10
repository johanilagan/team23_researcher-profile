function resetForm() {
    if (confirm('Are you sure you want to reset all changes? This will clear all form fields.')) {
        document.querySelector('form').reset();
        document.getElementById('file-preview').style.display = 'none';
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
    
   // --- File preview ---
        const fileInput = document.querySelector('input[type="file"]');
        const filePreview = document.getElementById('file-preview');
        const fileName = document.getElementById('file-name');
        const extractBtn = document.getElementById('extract-keywords-btn');
        const keywordsInput = document.getElementById('keywords-input');
        const status = document.getElementById('keyword-status');

        if (fileInput) {
            fileInput.addEventListener('change', function() {
                if (this.files && this.files[0]) {
                    fileName.textContent = this.files[0].name;
                    filePreview.style.display = 'block';
                    if (extractBtn) extractBtn.disabled = false;
                } else {
                    filePreview.style.display = 'none';
                    if (extractBtn) extractBtn.disabled = true;
                }
            });
        }

        // --- Extract Keywords ---
        if (extractBtn) {
            extractBtn.addEventListener('click', async function() {
                if (!fileInput.files.length) {
                    alert("Please upload a PDF first.");
                    return;
                }

                status.textContent = "Extracting keywords... please wait ⏳";
                const formData = new FormData();
                formData.append('pdf', fileInput.files[0]);

                try {
                    const response = await fetch('/extract_keywords', { method: 'POST', body: formData });
                    const data = await response.json();

                    if (data.success) {
                        keywordsInput.value = data.keywords.join(', ');
                        status.textContent = "✅ Keywords extracted successfully.";
                    } else {
                        status.textContent = "⚠️ Could not extract keywords.";
                    }
                } catch (err) {
                    console.error(err);
                    status.textContent = "❌ Error extracting keywords.";
                }
            });
        }

        // --- Set default year ---
        const yearInput = document.querySelector('input[name="year"]');
        if (yearInput && !yearInput.value) {
            yearInput.value = new Date().getFullYear();
        }
    });

