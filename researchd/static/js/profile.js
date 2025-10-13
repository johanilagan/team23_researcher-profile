// Profile Page JavaScript Functions

// CSRF Token Management
function getCSRFToken() {
    return document.querySelector('meta[name="csrf-token"]').getAttribute('content');
}

function makeCSRFRequest(url, options = {}) {
    const defaultOptions = {
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken()
        }
    };
    
    return fetch(url, { ...defaultOptions, ...options });
}

// Section Management Functions
function addSection(sect) {
    const section = document.querySelector(`[data-section="${sect}"]`);
    if (section) {
        section.classList.remove('d-none');
        toggleSectionButtons(sect, true);
        saveSectionOrder();
    } else {
        console.error("Section not found:", sect);
    }
}

function deleteSection(sect) {
    const section = document.querySelector(`[data-section="${sect}"]`);
    if (section) {
        section.classList.add('d-none');
        toggleSectionButtons(sect, false);
        saveSectionOrder();
    }
}

function toggleSectionButtons(sectionName, isVisible) {
    const btn = document.querySelector(`[data-section-btn="${sectionName}"]`);
    if (!btn) return;

    if (isVisible) {
        btn.innerHTML = `<i class="fas fa-trash me-1"></i>Delete ${formatSectionName(sectionName)}`;
        btn.setAttribute("onclick", `deleteSection('${sectionName}')`);
    } else {
        btn.innerHTML = `<i class="fas fa-plus me-1"></i>Add ${formatSectionName(sectionName)}`;
        btn.setAttribute("onclick", `addSection('${sectionName}')`);
    }
}

function formatSectionName(section) {
    switch (section) {
        case 'papers-section': return 'Papers Section';
        case 'interests-section': return 'Interests Section';
        default: return 'Section';
    }
}

function saveSectionOrder() {
    let order = [];
    document.querySelectorAll('#profile-sections [data-section]').forEach(function(section) {
        order.push({
            section: section.getAttribute('data-section'),
            visible: !section.classList.contains('d-none')
        });
    });
    console.log('Saving section order:', order);
    makeCSRFRequest('/save-section-order', {
        method: 'POST',
        body: JSON.stringify({order: order})
    })
    .then(response => response.json())
    .then(data => console.log("Saved section order:", data))
    .catch(err => console.error("Error saving section order:", err));
}

// Toggle Functions
function toggleExternalRoles() {
    const externalSection = document.getElementById('external-roles-section');
    const toggleBtn = document.getElementById('toggle-external-roles-btn');

    externalSection.classList.toggle('d-none');
    
    if (externalSection.classList.contains('d-none')) {
        toggleBtn.innerHTML = '<i class="fas fa-users me-1"></i> External Roles';
        toggleBtn.classList.remove('btn-outline-secondary');
        toggleBtn.classList.add('btn-outline-primary');
    } else {
        toggleBtn.innerHTML = '<i class="fas fa-eye-slash me-1"></i> Hide External Roles';
        toggleBtn.classList.remove('btn-outline-primary');
        toggleBtn.classList.add('btn-outline-secondary');
    }

    saveSectionOrder();
}

function toggleAchievements() {
    const achievementSection = document.getElementById('achievements-section');
    const toggleBtn = document.getElementById('toggle-achievements-btn');

    achievementSection.classList.toggle('d-none');

    if (achievementSection.classList.contains('d-none')) {
        toggleBtn.innerHTML = '<i class="fas fa-trophy me-1"></i> Achievements';
        toggleBtn.classList.remove('btn-outline-secondary');
        toggleBtn.classList.add('btn-outline-primary');
    } else {
        toggleBtn.innerHTML = '<i class="fas fa-eye-slash me-1"></i> Hide Achievements';
        toggleBtn.classList.remove('btn-outline-primary');
        toggleBtn.classList.add('btn-outline-secondary');
    }

    saveSectionOrder();
}

// Achievement Management
function deleteAchievement(aid) {
    makeCSRFRequest(`/delete_achievement/${aid}`, { method: 'DELETE'})
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                const el = document.querySelector(`[data-achid="${aid}"]`);
                if (el) el.remove();
                showNotification('Achievement deleted successfully', 'success');
            } else {
                showNotification('Error deleting achievement', 'error');
            }
        })
        .catch(() => {
            showNotification('Error deleting achievement', 'error');
        });
}

// Profile Picture Management
function changeProfilePic(input) {
    if (input.files && input.files[0]) {
        const file = input.files[0];
        
        // Validate file type
        const allowedTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif'];
        if (!allowedTypes.includes(file.type)) {
            showNotification('Please select a valid image file (JPG, PNG, or GIF)', 'error');
            return;
        }
        
        // Validate file size (max 5MB)
        const maxSize = 5 * 1024 * 1024; // 5MB in bytes
        if (file.size > maxSize) {
            showNotification('Image size must be less than 5MB', 'error');
            return;
        }
        
        // Preview the image immediately
        const reader = new FileReader();
        reader.onload = function(e) {
            document.getElementById('profile-pic').src = e.target.result;
        };
        reader.readAsDataURL(file);
        
        // Upload to server
        const formData = new FormData();
        formData.append('profile_picture', file);
        
        showNotification('Uploading profile picture...', 'info');
        
        fetch('/upload-profile-picture', {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCSRFToken()
            },
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                showNotification('Profile picture updated successfully!', 'success');
                // Update image with server URL to ensure it persists
                document.getElementById('profile-pic').src = data.image_url;
            } else {
                showNotification('Error uploading profile picture: ' + (data.error || 'Unknown error'), 'error');
                // Revert to placeholder if upload fails
                document.getElementById('profile-pic').src = '/static/placeholder.png';
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showNotification('Error uploading profile picture', 'error');
            // Revert to placeholder if upload fails
            document.getElementById('profile-pic').src = '/static/placeholder.png';
        });
    }
}

// External Roles Management
function addExternalRoleWithModal() {
    const modalHTML = `
        <div id="addExternalRoleModal" class="custom-modal" style="display: flex;">
            <div class="custom-modal-overlay" onclick="closeExternalRoleModal()"></div>
            <div class="custom-modal-content">
                <div class="custom-modal-header">
                    <h5 class="custom-modal-title"><i class="fas fa-users me-2"></i>Add External Role</h5>
                    <button type="button" class="custom-modal-close" onclick="closeExternalRoleModal()">&times;</button>
                </div>
                <div class="custom-modal-body">
                    <form id="external-role-form">
                        <div class="mb-3">
                            <label class="form-label">Role/Title *</label>
                            <input type="text" class="form-control" id="er-role-title" required placeholder="e.g., Editorial Board Member">
                        </div>
                        <div class="mb-3">
                            <label class="form-label">Organisation *</label>
                            <input type="text" class="form-control" id="er-organization" required placeholder="e.g., Journal of X, ACM SIGY">
                        </div>
                        <div class="row">
                            <div class="col-md-6">
                                <div class="mb-3">
                                    <label class="form-label">Start Year</label>
                                    <input type="number" class="form-control" id="er-start-year" min="1900" max="2035">
                                </div>
                            </div>
                            <div class="col-md-6">
                                <div class="mb-3">
                                    <label class="form-label">End Year</label>
                                    <input type="number" class="form-control" id="er-end-year" min="1900" max="2035">
                                    <small class="form-text text-muted">Leave empty if current</small>
                                </div>
                            </div>
                        </div>
                        <div class="mb-3">
                            <label class="form-label">Description</label>
                            <textarea class="form-control" id="er-description" rows="3" placeholder="Optional short description..."></textarea>
                        </div>
                    </form>
                </div>
                <div class="custom-modal-footer">
                    <button type="button" class="btn btn-secondary" onclick="closeExternalRoleModal()">Cancel</button>
                    <button type="button" class="btn btn-primary" onclick="submitExternalRole()">Add Role</button>
                </div>
            </div>
        </div>
    `;
    document.body.insertAdjacentHTML('beforeend', modalHTML);
    document.body.style.overflow = 'hidden';
    setTimeout(() => {
        const input = document.getElementById('er-role-title');
        if (input) input.focus();
    }, 100);
}

function closeExternalRoleModal() {
    const modal = document.getElementById('addExternalRoleModal');
    if (modal) modal.remove();
    document.body.style.overflow = 'auto';
}

function submitExternalRole() {
    const roleTitle = document.getElementById('er-role-title').value.trim();
    const organization = document.getElementById('er-organization').value.trim();
    const startYear = document.getElementById('er-start-year').value;
    const endYear = document.getElementById('er-end-year').value;
    const description = document.getElementById('er-description').value.trim();

    if (!roleTitle || !organization) {
        showNotification('Please fill in required fields (Role and Organization)', 'error');
        return;
    }

    const submitBtn = document.querySelector('#addExternalRoleModal .btn-primary');
    if (submitBtn) { submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-1"></i>Adding...'; submitBtn.disabled = true; }

    makeCSRFRequest('/add_external_role', {
        method: 'POST',
        body: JSON.stringify({
            role_title: roleTitle,
            organization: organization,
            start_year: startYear ? parseInt(startYear) : null,
            end_year: endYear ? parseInt(endYear) : null,
            description: description
        })
    })
    .then(r => r.json())
    .then(result => {
        if (result.success) {
            addExternalRoleToDOM(result);
            closeExternalRoleModal();
            showNotification('External role added!', 'success');
        } else {
            showNotification('Error adding role: ' + (result.error || 'Unknown error'), 'error');
        }
    })
    .catch(err => {
        console.error(err);
        showNotification('Error adding role', 'error');
    })
    .finally(() => {
        if (submitBtn) { submitBtn.innerHTML = 'Add Role'; submitBtn.disabled = false; }
    });
}

function addExternalRoleToDOM(er) {
    const list = document.getElementById('external-roles-list');
    if (!list) return;

    const emptyState = list.querySelector('.empty-state');
    if (emptyState) emptyState.remove();

    const div = document.createElement('div');
    div.className = 'list-group-item d-flex justify-content-between align-items-center';
    div.dataset.erid = er.erid;
    div.style.cursor = 'move';

    let yearRange = '';
    if (er.start_year) {
        yearRange = `<small>(${er.start_year}${er.end_year ? ' – ' + er.end_year : ' – Present'})</small>`;
    }

    div.innerHTML = `
        <div>
            <strong>${escapeHtml(er.role_title)}</strong> — ${escapeHtml(er.organization)}
            ${yearRange}
            ${er.description ? `<p class="mb-0 text-muted">${escapeHtml(er.description)}</p>` : ''}
        </div>
        <div>
            <button class="btn btn-sm btn-danger" onclick="deleteExternalRole(${er.erid})" title="Delete this role">
                <i class="fas fa-trash"></i>
            </button>
        </div>
    `;

    list.appendChild(div);

    const instructions = document.querySelector('.drag-instructions-external');
    if (!instructions && list.children.length > 1) {
        const small = document.createElement('small');
        small.className = 'text-muted mt-2 d-block drag-instructions-external';
        small.innerHTML = '<i class="fas fa-grip-vertical me-1"></i>Drag and drop to reorder roles';
        list.parentNode.appendChild(small);
    }
}

function deleteExternalRole(erid) {
    makeCSRFRequest(`/delete_external_role/${erid}`, { method: 'DELETE' })
        .then(r => r.json())
        .then(data => {
            if (data.success) {
                const el = document.querySelector(`[data-erid="${erid}"]`);
                if (el) el.remove();
                showNotification('External role deleted', 'success');
            } else {
                showNotification('Error deleting role', 'error');
            }
        })
        .catch(() => showNotification('Error deleting role', 'error'));
}

// Achievement Management
function addAchievementWithModal() {
    const modalHTML = `
        <div id="addAchievementModal" class="custom-modal" style="display: flex;">
            <div class="custom-modal-overlay" onclick="closeAchievementModal()"></div>
            <div class="custom-modal-content">
                <div class="custom-modal-header">
                    <h5 class="custom-modal-title"><i class="fas fa-trophy me-2"></i>Add Achievement</h5>
                    <button type="button" class="custom-modal-close" onclick="closeAchievementModal()">&times;</button>
                </div>
                <div class="custom-modal-body">
                    <form id="addAchievementForm">
                        <div class="mb-3">
                            <label class="form-label">Title *</label>
                            <input type="text" class="form-control" id="achievementTitle" required placeholder="e.g., Best Paper Award">
                        </div>
                        <div class="mb-3">
                            <label class="form-label">Type</label>
                            <select class="form-select" id="achievementType">
                                <option value="">Select type</option>
                                <option value="Grant">Grant</option>
                                <option value="Award">Award</option>
                                <option value="Fund">Fund</option>
                            </select>
                        </div>
                        <div class="mb-3">
                            <label class="form-label">Year</label>
                            <input type="number" class="form-control" id="achievementYear" min="1900" max="2100">
                        </div>
                        <div class="mb-3">
                            <label class="form-label">Description</label>
                            <textarea class="form-control" id="achievementDescription" rows="3" placeholder="Optional description..."></textarea>
                        </div>
                    </form>
                </div>
                <div class="custom-modal-footer">
                    <button type="button" class="btn btn-secondary" onclick="closeAchievementModal()">Cancel</button>
                    <button type="button" class="btn btn-primary" onclick="submitAchievement()">Add Achievement</button>
                </div>
            </div>
        </div>
    `;
    document.body.insertAdjacentHTML('beforeend', modalHTML);
    document.body.style.overflow = 'hidden';
    setTimeout(() => {
        const input = document.getElementById('achievementTitle');
        if (input) input.focus();
    }, 100);
}

function addAchievementToDOM(ach) {
    const list = document.getElementById('achievements-list');
    if (!list) return;

    const emptyState = list.querySelector('.empty-state');
    if (emptyState) emptyState.remove();

    const div = document.createElement('div');
    div.className = 'list-group-item d-flex justify-content-between align-items-center';
    div.dataset.achid = ach.aid;
    div.style.cursor = 'move';

    let year = ach.year ? `<small class="text-muted">(${ach.year})</small>` : '';
    let typeBadge = ach.type ? `<span class="badge bg-secondary">${ach.type}</span>` : '';

    div.innerHTML = `
        <div>
            <strong>${escapeHtml(ach.title)}</strong> ${typeBadge} ${year}
            ${ach.description ? `<p class="mb-0 text-muted">${escapeHtml(ach.description)}</p>` : ''}
        </div>
        <div>
            <button class="btn btn-sm btn-danger" onclick="deleteAchievement('${ach.aid}')" title="Delete this achievement">
                <i class="fas fa-trash"></i>
            </button>
        </div>
    `;

    list.appendChild(div);

    // Add drag instructions if more than 1 item
    const instructions = document.querySelector('.drag-instructions-achievements');
    if (!instructions && list.children.length > 1) {
        const small = document.createElement('small');
        small.className = 'text-muted mt-2 d-block drag-instructions-achievements';
        small.innerHTML = '<i class="fas fa-grip-vertical me-1"></i>Drag and drop to reorder achievements';
        list.parentNode.appendChild(small);
    }
}

function closeAchievementModal() {
    const modal = document.getElementById('addAchievementModal');
    if (modal) {
        modal.remove();
        document.body.style.overflow = '';
    }
}

async function submitAchievement() {
    const title = document.getElementById("achievementTitle").value.trim();
    const type = document.getElementById("achievementType").value.trim();
    const year = document.getElementById("achievementYear").value.trim();
    const description = document.getElementById("achievementDescription").value.trim();

    if (!title || !type) {
        showNotification("Title and Type are required.", "error");
        return;
    }

    const payload = { title, type, year, description };

    try {
        const response = await makeCSRFRequest("/add_achievement", {
            method: "POST",
            body: JSON.stringify(payload),
        });

        const result = await response.json();

        if (result.success) {
            showNotification("Achievement added successfully!", "success");

            // Clear form fields
            document.getElementById("achievementTitle").value = "";
            document.getElementById("achievementType").value = "";
            document.getElementById("achievementYear").value = "";
            document.getElementById("achievementDescription").value = "";

            // Append to list via helper
            if (typeof addAchievementToDOM === 'function') {
                addAchievementToDOM(result);
            }

            // Close modal
            closeAchievementModal();
        } else {
            showNotification(result.error || "Failed to add achievement.", "error");
        }
    } catch (err) {
        console.error("Error:", err);
        showNotification("An unexpected error occurred.", "error");
    }
}

// Research Interests Management
const researchInterests = [
    'Machine Learning', 'Artificial Intelligence', 'Data Science', 'Deep Learning',
    'Neural Networks', 'Computer Vision', 'Natural Language Processing', 'Robotics',
    'Algorithm Design', 'Data Mining', 'Big Data', 'Statistics', 'Probability',
    'Optimization', 'Linear Algebra', 'Calculus', 'Discrete Mathematics',
    'Software Engineering', 'Computer Programming', 'Database Systems', 'Information Systems',
    'Cybersecurity', 'Cryptography', 'Network Security', 'Information Security',
    'Human-Computer Interaction', 'User Experience Design', 'Web Development',
    'Mobile Development', 'Cloud Computing', 'Distributed Systems', 'Operating Systems',
    'Computer Architecture', 'Embedded Systems', 'IoT', 'Blockchain', 'Quantum Computing',
    'Bioinformatics', 'Computational Biology', 'Digital Signal Processing',
    'Image Processing', 'Pattern Recognition', 'Computer Graphics', 'Game Development',
    'Virtual Reality', 'Augmented Reality', 'Mixed Reality', 'Computer Animation',
    'Scientific Computing', 'High Performance Computing', 'Parallel Computing',
    'Machine Translation', 'Speech Recognition', 'Text Mining', 'Information Retrieval',
    'Recommender Systems', 'Social Network Analysis', 'Graph Theory', 'Complexity Theory',
    'Automata Theory', 'Formal Methods', 'Software Testing', 'Quality Assurance',
    'Project Management', 'Agile Development', 'DevOps', 'Microservices',
    'API Development', 'RESTful Services', 'GraphQL', 'Web Services',
    'Data Visualization', 'Business Intelligence', 'Analytics', 'Predictive Modeling',
    'Time Series Analysis', 'Regression Analysis', 'Classification', 'Clustering',
    'Dimensionality Reduction', 'Feature Engineering', 'Model Selection',
    'Cross-Validation', 'Hyperparameter Tuning', 'Ensemble Methods',
    'Reinforcement Learning', 'Transfer Learning', 'Federated Learning',
    'Explainable AI', 'Ethical AI', 'AI Ethics', 'Fairness in AI',
    'Bias in AI', 'AI Safety', 'Robust AI', 'Adversarial AI',
    'Generative AI', 'Large Language Models', 'Transformers', 'BERT', 'GPT',
    'Computer Networks', 'Internet Protocols', 'Wireless Networks', '5G',
    'Edge Computing', 'Fog Computing', 'Serverless Computing', 'Containerization',
    'Docker', 'Kubernetes', 'Infrastructure as Code', 'Configuration Management',
    'Version Control', 'Git', 'Continuous Integration', 'Continuous Deployment',
    'Monitoring', 'Logging', 'Debugging', 'Performance Optimization',
    'Scalability', 'Reliability', 'Fault Tolerance', 'Load Balancing',
    'Caching', 'CDN', 'Content Delivery', 'API Gateway', 'Service Mesh',
    'Event-Driven Architecture', 'Message Queues', 'Event Streaming',
    'Data Pipelines', 'ETL', 'Data Warehousing', 'Data Lakes',
    'Real-time Processing', 'Stream Processing', 'Batch Processing',
    'Data Governance', 'Data Privacy', 'GDPR', 'Compliance',
    'Risk Management', 'Audit', 'Logging', 'Compliance Monitoring',
    'Machine Learning Operations', 'MLOps', 'Model Deployment', 'Model Monitoring',
    'A/B Testing', 'Experimentation', 'Statistical Testing', 'Hypothesis Testing',
    
    // Physical Sciences
    'Physics', 'Quantum Physics', 'Theoretical Physics', 'Experimental Physics',
    'Astrophysics', 'Cosmology', 'Particle Physics', 'Nuclear Physics',
    'Materials Science', 'Nanotechnology', 'Chemistry', 'Organic Chemistry',
    'Inorganic Chemistry', 'Physical Chemistry', 'Biochemistry', 'Chemical Engineering',
    'Earth Sciences', 'Geology', 'Geophysics', 'Astronomy', 'Planetary Science',
    'Environmental Science', 'Climate Change', 'Ecology', 'Conservation Biology',
    
    // Life Sciences & Medicine
    'Biology', 'Molecular Biology', 'Cell Biology', 'Genetics', 'Genomics',
    'Neuroscience', 'Psychology', 'Medicine', 'Clinical Research', 'Public Health',
    'Cancer Research', 'Pharmacology', 'Epidemiology', 'Biomedical Engineering',
    'Nutrition Science', 'Agricultural Science', 'Veterinary Science',
    
    // Mathematics & Statistics
    'Mathematics', 'Pure Mathematics', 'Applied Mathematics', 'Algebra',
    'Geometry', 'Calculus', 'Probability Theory', 'Mathematical Statistics',
    'Optimization Theory', 'Game Theory', 'Mathematical Modeling',
    
    // Engineering
    'Engineering', 'Mechanical Engineering', 'Civil Engineering', 'Electrical Engineering',
    'Aerospace Engineering', 'Environmental Engineering', 'Materials Engineering',
    'Renewable Energy', 'Robotics Engineering', 'Biotechnology',
    
    // Social Sciences
    'Sociology', 'Political Science', 'International Relations', 'Economics',
    'Anthropology', 'Archaeology', 'Geography', 'Urban Planning',
    'Criminology', 'Criminal Justice', 'Public Policy',
    
    // Humanities
    'History', 'Literature', 'Philosophy', 'Linguistics', 'Art', 'Music',
    'Religious Studies', 'Cultural Studies', 'Media Studies',
    
    // Education
    'Education', 'Educational Psychology', 'Learning Sciences', 'Curriculum Studies',
    'Educational Technology', 'Higher Education', 'Teacher Education',
    
    // Business & Management
    'Business Administration', 'Management', 'Marketing', 'Finance',
    'Entrepreneurship', 'International Business', 'Human Resource Management',
    
    // Law & Legal Studies
    'Law', 'Constitutional Law', 'Criminal Law', 'International Law',
    'Intellectual Property Law', 'Environmental Law', 'Legal Studies',
    
    // Research Methods & Skills
    'Research Methodology', 'Experimental Design', 'Survey Design',
    'Qualitative Research', 'Quantitative Research', 'Mixed Methods Research',
    'Academic Writing', 'Technical Writing', 'Grant Writing', 'Teaching',
    'Presentation Skills', 'Public Speaking', 'Mentoring', 'Collaboration',
    'Project Management', 'Innovation', 'Creativity', 'Problem Solving',
    'Critical Thinking', 'Analytical Skills', 'Research Skills',
    'Literature Review', 'Funding', 'Communication', 'Leadership'
];

let selectedInterests = [];
let availableInterests = [...researchInterests];

// Modal Management
function showModal() {
    const modal = document.getElementById('editInterestsModal');
    if (modal) {
        modal.style.display = 'flex';
        document.body.style.overflow = 'hidden'; // Prevent background scrolling
    }
}

function closeModal() {
    const modal = document.getElementById('editInterestsModal');
    if (modal) {
        modal.style.display = 'none';
        document.body.style.overflow = 'auto'; // Restore scrolling
    }
}

function editInterests() {
    console.log('Edit interests clicked');
    
    try {
        // Get current interests from the page
        const currentInterests = [];
        const interestTags = document.querySelectorAll('#research-interests .interest-tag');
        interestTags.forEach(tag => {
            const interest = tag.textContent.trim();
            // Skip the placeholder text
            if (interest !== 'No interests selected yet') {
                currentInterests.push(interest);
            }
        });
        
        console.log('Current interests from page:', currentInterests);
        
        selectedInterests = [...currentInterests];
        availableInterests = researchInterests.filter(interest => 
            !selectedInterests.includes(interest)
        );
        
        console.log('Selected interests:', selectedInterests);
        console.log('Available interests count:', availableInterests.length);
        
        updateInterestsDisplay();
        
        // Clear search input
        const searchInput = document.getElementById('interest-search');
        if (searchInput) {
            searchInput.value = '';
        }
        
        initializeSearch();
        
        // Show modal
        showModal();
        console.log('Modal should be showing now');
        
    } catch (error) {
        console.error('Error in editInterests:', error);
        console.error('Error opening interests editor:', error);
    }
}

function updateInterestsDisplay() {
    console.log('Updating interests display');
    const selectedContainer = document.getElementById('selected-interests-list');
    
    if (!selectedContainer) {
        console.error('Selected container not found');
        return;
    }
    
    // Clear selected container
    selectedContainer.innerHTML = '';
    
    console.log('Adding selected interests:', selectedInterests.length);
    // Add selected interests
    selectedInterests.forEach(interest => {
        const tag = document.createElement('span');
        tag.className = 'interest-tag selected-tag';
        tag.textContent = interest;
        tag.onclick = () => removeInterest(interest);
        selectedContainer.appendChild(tag);
    });
    
    // Update counter
    const counter = document.getElementById('selected-count');
    if (counter) {
        counter.textContent = selectedInterests.length;
    }
}

function updateSearchResults(searchTerm) {
    const searchResultsDiv = document.getElementById('search-results');
    const searchResultsList = document.getElementById('search-results-list');
    
    if (!searchResultsDiv || !searchResultsList) {
        console.error('Search results elements not found');
        return;
    }
    
    // Clear previous results
    searchResultsList.innerHTML = '';
    
    if (searchTerm.length < 2) {
        searchResultsDiv.style.display = 'none';
        return;
    }
    
    // Filter interests based on search term
    const filteredInterests = researchInterests.filter(interest => 
        interest.toLowerCase().includes(searchTerm.toLowerCase()) &&
        !selectedInterests.includes(interest)
    );
    
    if (filteredInterests.length === 0) {
        searchResultsDiv.style.display = 'none';
        return;
    }
    
    // Show search results
    searchResultsDiv.style.display = 'block';
    
    // Add filtered interests
    filteredInterests.slice(0, 20).forEach(interest => { // Limit to 20 results
        const tag = document.createElement('span');
        tag.className = 'interest-tag available-tag';
        tag.textContent = interest;
        tag.onclick = () => addInterest(interest);
        searchResultsList.appendChild(tag);
    });
    
    if (filteredInterests.length > 20) {
        const moreTag = document.createElement('span');
        moreTag.className = 'interest-tag more-results';
        moreTag.textContent = `... and ${filteredInterests.length - 20} more`;
        moreTag.style.fontStyle = 'italic';
        moreTag.style.opacity = '0.7';
        searchResultsList.appendChild(moreTag);
    }
}

function addInterest(interest) {
    console.log('Adding interest:', interest);
    if (!selectedInterests.includes(interest)) {
        selectedInterests.push(interest);
        updateInterestsDisplay();
        
        // Update search results to remove the added interest
        const searchInput = document.getElementById('interest-search');
        if (searchInput) {
            updateSearchResults(searchInput.value);
        }
    }
}

function removeInterest(interest) {
    console.log('Removing interest:', interest);
    selectedInterests = selectedInterests.filter(i => i !== interest);
    updateInterestsDisplay();
    
    // Update search results to show the removed interest again
    const searchInput = document.getElementById('interest-search');
    if (searchInput) {
        updateSearchResults(searchInput.value);
    }
}

function saveInterests() {
    console.log('Saving interests:', selectedInterests);
    
    // Update the page display
    const interestsContainer = document.getElementById('research-interests');
    interestsContainer.innerHTML = '';
    
    if (selectedInterests.length === 0) {
        const tag = document.createElement('span');
        tag.className = 'interest-tag';
        tag.textContent = 'No interests selected yet';
        interestsContainer.appendChild(tag);
    } else {
        selectedInterests.forEach(interest => {
            const tag = document.createElement('span');
            tag.className = 'interest-tag';
            tag.textContent = interest;
            interestsContainer.appendChild(tag);
        });
    }
    
    // Send to server
    const interestsString = selectedInterests.join(',');
    console.log('Sending to server:', interestsString);
    
    makeCSRFRequest('/update-interests', {
        method: 'POST',
        body: JSON.stringify({
            interests: interestsString
        })
    })
    .then(response => response.json())
    .then(data => {
        console.log('Server response:', data);
        if (data.success) {
            showNotification('Research interests updated successfully!', 'success');
            closeModal();
        } else {
            showNotification('Error updating interests. Please try again.', 'error');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showNotification('Error updating interests. Please try again.', 'error');
    });
}

function initializeSearch() {
    const searchInput = document.getElementById('interest-search');
    if (searchInput) {
        searchInput.addEventListener('input', function() {
            const searchTerm = this.value;
            updateSearchResults(searchTerm);
        });
    }
}

// Utility Functions
function escapeHtml(text) {
    const map = { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#039;' };
    return String(text).replace(/[&<>"']/g, m => map[m]);
}

function showNotification(message, type) {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.innerHTML = `
        <div class="notification-content">
            <i class="fas fa-${type === 'success' ? 'check-circle' : type === 'error' ? 'exclamation-circle' : 'info-circle'}"></i>
            <span>${message}</span>
        </div>
    `;

    // Add to page
    document.body.appendChild(notification);

    // Show notification
    setTimeout(() => notification.classList.add('show'), 100);

    // Remove after 3 seconds
    setTimeout(() => {
        notification.classList.remove('show');
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

// Paper Management Functions
function addNewPaper() {
    window.location.href = "/upload-paper";
}

function managePapers() {
    showNotification('Paper management feature coming soon!', 'info');
}

function viewAllPapers() {
    window.location.href = "/my-papers";
}

// Test function 
function testModal() {
    console.log('Testing modal...');
    const modalElement = document.getElementById('editInterestsModal');
    if (modalElement) {
        console.log('Modal element found');
        modalElement.style.display = 'flex';
        console.log('Modal should be showing');
    } else {
        console.error('Modal element not found');
    }
}
