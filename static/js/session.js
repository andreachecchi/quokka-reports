/**
 * Session management module
 * Handles login, logout, and session validation
 */

$(document).ready(function() {
    // Logout handler for all pages
    $(document).on('click', '.logout-link', function(e) {
        e.preventDefault();
        
        $.ajax({
            url: '/api/logout',
            method: 'POST',
            success: function(response) {
                // Backend clears cookies, redirect to login
                window.location.href = '/login';
            },
            error: function(xhr) {
                console.error('Logout error:', xhr);
                // Fallback to direct navigation if API fails
                window.location.href = '/login';
            }
        });
    });
});
