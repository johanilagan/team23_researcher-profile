document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('searchInput');
    const institutionFilter = document.getElementById('institutionFilter');
    const positionFilter = document.getElementById('positionFilter');
    const interestsFilter = document.getElementById('interestsFilter');
    const journalFilter = document.getElementById('journalFilter');
    const yearFilter = document.getElementById('yearFilter');
    const sortSelect = document.getElementById('sortSelect');
    const searchTypeRadios = document.querySelectorAll('input[name="type"]');
    const researcherFilters = document.getElementById('researcherFilters');
    const paperFilters = document.getElementById('paperFilters');
    
    // Clear all filters and submit form
    function clearFilters() {
        searchInput.value = '';
        institutionFilter.value = '';
        positionFilter.value = '';
        interestsFilter.value = '';
        journalFilter.value = '';
        yearFilter.value = '';
        sortSelect.value = 'name';
        document.getElementById('typeResearchers').checked = true;
        updateFiltersVisibility();
        document.getElementById('searchForm').submit();
    }
    
    // Update filter visibility based on search type
    function updateFiltersVisibility() {
        const selectedType = document.querySelector('input[name="type"]:checked').value;
        
        if (selectedType === 'papers') {
            researcherFilters.style.display = 'none';
            paperFilters.style.display = 'block';
            // Update sort options for papers
            updateSortOptions('papers');
        } else if (selectedType === 'researchers') {
            researcherFilters.style.display = 'block';
            paperFilters.style.display = 'none';
            // Update sort options for researchers
            updateSortOptions('researchers');
        } else { // 'all'
            researcherFilters.style.display = 'block';
            paperFilters.style.display = 'block';
            // Default sort options
            updateSortOptions('researchers');
        }
    }
    
    // Update sort options based on search type
    function updateSortOptions(type) {
        const sortSelect = document.getElementById('sortSelect');
        const currentValue = sortSelect.value;
        
        // Clear existing options
        sortSelect.innerHTML = '';
        
        if (type === 'papers') {
            const options = [
                { value: 'created_at', text: 'Sort by Date' },
                { value: 'year', text: 'Sort by Year' },
                { value: 'title', text: 'Sort by Title' },
                { value: 'journal', text: 'Sort by Journal' }
            ];
            options.forEach(option => {
                const optionElement = document.createElement('option');
                optionElement.value = option.value;
                optionElement.textContent = option.text;
                if (option.value === currentValue) {
                    optionElement.selected = true;
                }
                sortSelect.appendChild(optionElement);
            });
        } else {
            const options = [
                { value: 'name', text: 'Sort by Name' },
                { value: 'institution', text: 'Sort by Institution' },
                { value: 'position', text: 'Sort by Position' }
            ];
            options.forEach(option => {
                const optionElement = document.createElement('option');
                optionElement.value = option.value;
                optionElement.textContent = option.text;
                if (option.value === currentValue) {
                    optionElement.selected = true;
                }
                sortSelect.appendChild(optionElement);
            });
        }
    }
    
    // Auto-submit form when filters change
    if (institutionFilter) {
        institutionFilter.addEventListener('change', function() {
            document.getElementById('searchForm').submit();
        });
    }
    
    if (positionFilter) {
        positionFilter.addEventListener('change', function() {
            document.getElementById('searchForm').submit();
        });
    }
    
    if (interestsFilter) {
        interestsFilter.addEventListener('change', function() {
            document.getElementById('searchForm').submit();
        });
    }
    
    if (journalFilter) {
        journalFilter.addEventListener('change', function() {
            document.getElementById('searchForm').submit();
        });
    }
    
    if (yearFilter) {
        yearFilter.addEventListener('change', function() {
            document.getElementById('searchForm').submit();
        });
    }
    
    if (sortSelect) {
        sortSelect.addEventListener('change', function() {
            document.getElementById('searchForm').submit();
        });
    }
    
    // Handle search type changes
    searchTypeRadios.forEach(radio => {
        radio.addEventListener('change', function() {
            updateFiltersVisibility();
            document.getElementById('searchForm').submit();
        });
    });
    
    // Initialize filter visibility
    updateFiltersVisibility();
    
    // Make clearFilters function global
    window.clearFilters = clearFilters;
});

