$(document).ready(function() {
    // Login form submission
    $('#login-form').submit(function(e) {
        e.preventDefault();
        
        const username = $('#username').val().trim();
        const password = $('#password').val().trim();
        
        if (!username || !password) {
            showErrorMessage('Please fill in all fields');
            return;
        }
        
        // Disable submit button
        const submitBtn = $('button[type="submit"]');
        submitBtn.prop('disabled', true);
        submitBtn.addClass('btn-loading');
        
        // Show loading state on error message
        $('#error-message').removeClass('visible');
        
        // Send login request
        $.ajax({
            url: '/api/login',
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({
                username: username,
                password: password
            }),
            success: function(response) {
                // Redirect to reports page
                // display_name cookie is set by server with httponly=False
                window.location.href = '/reports';
            },
            error: function(xhr) {
                // Re-enable submit button
                submitBtn.prop('disabled', false);
                submitBtn.removeClass('btn-loading');
                
                // Show error message
                let errorMessage = 'Login failed';
                if (xhr.responseJSON && xhr.responseJSON.detail) {
                    errorMessage = xhr.responseJSON.detail;
                }
                showErrorMessage(errorMessage);
            }
        });
    });
    
    // Function to show error message
    function showErrorMessage(message) {
        const $errorMessage = $('#error-message');
        $errorMessage.text(message);
        $errorMessage.addClass('visible');
    }
});
