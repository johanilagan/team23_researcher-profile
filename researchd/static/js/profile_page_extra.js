// Additional profile page initialization
// Note: This file is loaded after profile.js and handles Sortable.js initialization

document.addEventListener('DOMContentLoaded', function() {
    // Check if Sortable is available and user is owner
    if (typeof Sortable !== 'undefined' && document.getElementById('profile-sections')) {
        new Sortable(document.getElementById('profile-sections'), {
            animation: 150,
            handle: '.profile-section',
            onEnd: function (evt) {
                if (typeof saveSectionOrder === 'function') {
                    saveSectionOrder();
                }
            }
        });

        // Initialize sortable for External Roles list if present
        const extList = document.getElementById('external-roles-list');
        if (extList) {
            new Sortable(extList, {
                animation: 150,
                handle: '.list-group-item',
                onEnd: function () {
                    const order = Array.from(extList.children)
                        .filter(item => item.dataset.erid)
                        .map(item => item.dataset.erid);
                    
                    if (typeof makeCSRFRequest === 'function') {
                        makeCSRFRequest('/update_external_role_order', {
                            method: 'POST',
                            body: JSON.stringify({ order: order })
                        }).then(r => r.json()).then(data => {
                            if (data.success && typeof showNotification === 'function') {
                                showNotification('External roles order updated!', 'success');
                            } else if (typeof showNotification === 'function') {
                                showNotification('Error updating roles order', 'error');
                            }
                        });
                    }
                }
            });
        }

        // Initialize sortable for Achievements list if present
        const achList = document.getElementById('achievements-list');
        if (achList) {
            new Sortable(achList, {
                animation: 150,
                handle: '.list-group-item',
                onEnd: function () {
                    console.log("Achievement dragged!");
                    const order = Array.from(achList.querySelectorAll('.list-group-item[data-achid]'))
                        .map(item => item.dataset.achid)
                        .filter(id => id); // Filter out any undefined or null ids

                    if (order.length && typeof makeCSRFRequest === 'function') {
                        makeCSRFRequest('/update_achievement_order', {
                            method: 'POST',
                            body: JSON.stringify({ order: order })
                        })
                        .then(r => r.json())
                        .then(data => {
                            console.log("Response from server:", data);
                            if (data.success) showNotification('Achievements order updated!', 'success');
                            else showNotification('Error updating achievements order', 'error');
                        })
                        .catch(err => console.error("Request failed:", err));
                    }
                }
            })
        }
    }
});

// Initialize edit interests button
document.addEventListener('DOMContentLoaded', function() {
    
    // Setup button
    const editBtn = document.getElementById('edit-interests-btn');
    if (editBtn) {
        editBtn.addEventListener('click', function(e) {
            e.preventDefault();
            if (typeof editInterests === 'function') {
                editInterests();
            }
        });
    } else {
        console.log('Edit button not found');
    }
});

