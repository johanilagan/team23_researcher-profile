document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('searchInput');
    const institutionFilter = document.getElementById('institutionFilter');
    const positionFilter = document.getElementById('positionFilter');
    const interestsFilter = document.getElementById('interestsFilter');
    const sortSelect = document.getElementById('sortSelect');
    
    // Clear all filters and submit form
    function clearFilters() {
        searchInput.value = '';
        institutionFilter.value = '';
        positionFilter.value = '';
        interestsFilter.value = '';
        sortSelect.value = 'name';
        document.getElementById('searchForm').submit();
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
    
    if (sortSelect) {
        sortSelect.addEventListener('change', function() {
            document.getElementById('searchForm').submit();
        });
    }
    
    // Make clearFilters function global
    window.clearFilters = clearFilters;
});

