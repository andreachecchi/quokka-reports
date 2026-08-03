$(document).ready(function() {
    // Display username from response data
    function getCookie(name) {
        const value = `; ${document.cookie}`;
        const parts = value.split(`; ${name}=`); 
        if (parts.length === 2) {
            const decoded = parts.pop().split(';').shift();
            // Decode URL-encoded cookie value
            try {
                return decodeURIComponent(decoded);
            } catch (e) {
                return decoded;
            }
        }
        return '';
    }
    
    // Try to get display_name from cookie (set by server after successful login)
    // If not available, fall back to username
    const displayName = getCookie('display_name') || getCookie('username') || 'Unknown';
    $('#username-display').text(displayName);
    
    const report = REPORT_DATA || {};
    const datasets = DATASETS_DATA || [];
    
    // Show report name
    $('h2').text(report.name || 'Report');
    $('.report-description').html(report.description || '');
    
    // Build parameter form if datasets have parameters
    if (datasets.length > 0) {
        const $paramsContainer = $('#params-container');
        const $form = $('#report-form');
        
                datasets.forEach(dataset => {
                    if (dataset.params && dataset.params.length > 0) {
$form.append(`<h4 title="${dataset.description || ''}">Dataset: ${dataset.name}</h4>`);
                        
                        dataset.params.forEach(param => {
                    // Determine input type based on param.type
                    let inputType = 'text';
                    switch(param.type) {
                        case 'date':
                            inputType = 'date';
                            break;
                        case 'datetime':
                            inputType = 'datetime-local';
                            break;
                        case 'time':
                            inputType = 'time';
                            break;
                        case 'number':
                            inputType = 'number';
                            break;
                        case 'email':
                            inputType = 'email';
                            break;
                        case 'string':
                        default:
                            inputType = 'text';
                            break;
                    }
                    
                    $form.append(`
                        <div class="form-group">
                            <label for="param-${dataset.id}-${param.id}">${param.name || param.id}</label>
                            <input type="${inputType}" id="param-${dataset.id}-${param.id}" 
                                   class="param-input" 
                                   data-dataset="${dataset.id}" 
                                   data-param="${param.id}">
                        </div>
                    `);
                });
                
                $form.append('<hr>');
            }
        });
        
        $paramsContainer.show();
    } else {
        $('#params-container').hide();
    }
    
    // Execute report button
    $('#execute-btn').on('click', function() {
        const $btn = $(this);
        $btn.prop('disabled', true).addClass('btn-loading');
        $('#report-error').removeClass('visible');
        $('#report-status').empty();
        $('#report-iframe').hide();
        
        // Clear previous validation errors
        $('.param-input').next('.error-message').remove();
        $('.param-input').removeClass('error');
        
        // Validate parameters
        let hasErrors = false;
        $('.param-input').each(function() {
            const $input = $(this);
            const value = $input.val().trim();
            const inputType = $input.attr('type');
            
            // Check if empty
            if (!value) {
                $input.after('<span class="error-message">Campo obbligatorio</span>').addClass('error');
                hasErrors = true;
                return;
            }
            
            // Validate input types
            if (inputType === 'number') {
                if (isNaN(parseFloat(value)) || !isFinite(value)) {
                    $input.after('<span class="error-message">Valore numerico non valido</span>').addClass('error');
                    hasErrors = true;
                }
            } else if (inputType === 'email') {
                const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
                if (!emailRegex.test(value)) {
                    $input.after('<span class="error-message">Formato email non valido</span>').addClass('error');
                    hasErrors = true;
                }
            }
        });
        
        // If validation fails, re-enable button and stop
        if (hasErrors) {
            $btn.prop('disabled', false).removeClass('btn-loading');
            return;
        }
        
        // Collect parameters
        const params = {};
        $('.param-input').each(function() {
            const dataset = $(this).data('dataset');
            const param = $(this).data('param');
            const value = $(this).val();
            
            if (!params[dataset]) {
                params[dataset] = {};
            }
            params[dataset][param] = value;
        });
        
        const reportId = report.id;
        
        // Execute report
        $.ajax({
            url: `/api/report/${reportId}/execute`,
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ params: params }),
            success: function(response) {
                $btn.prop('disabled', false).removeClass('btn-loading');
                
                if (response.success) {
                    $('#report-status').html('<div class="success-message">Report generato con successo!</div>');
                    $('#report-iframe').attr('src', `/generated/${response.html_path.split('/').pop()}?t=${Date.now()}`);
                    $('#report-iframe').show();
                    $('#export-pdf-btn').css('display', 'inline-block');
                    $('#export-excel-btn').css('display', 'inline-block');
                } else {
                    $btn.prop('disabled', false).removeClass('btn-loading');
                    $('#report-error').text(response.detail || 'Errore durante la generazione del report').addClass('visible');
                }
            },
            error: function(xhr) {
                $btn.prop('disabled', false).removeClass('btn-loading');
                
                let errorMessage = 'Errore durante la generazione del report';
                if (xhr.responseJSON && xhr.responseJSON.detail) {
                    errorMessage = xhr.responseJSON.detail;
                }
                $('#report-error').text(errorMessage).addClass('visible');
            }
        });
    });
    
// Export to PDF button
$('#export-pdf-btn').on('click', function() {
    const $btn = $(this);
    $btn.prop('disabled', true).addClass('btn-loading');
    $('#report-error').removeClass('visible');
    $('#report-status').empty();
    $('#report-iframe').hide();
    
    // Clear previous validation errors
    $('.param-input').next('.error-message').remove();
    $('.param-input').removeClass('error');
    
    // Validate parameters
    let hasErrors = false;
    $('.param-input').each(function() {
        const $input = $(this);
        const value = $input.val().trim();
        const inputType = $input.attr('type');
        
        // Check if empty
        if (!value) {
            $input.after('<span class="error-message">Campo obbligatorio</span>').addClass('error');
            hasErrors = true;
            return;
        }
        
        // Validate input types
        if (inputType === 'number') {
            if (isNaN(parseFloat(value)) || !isFinite(value)) {
                $input.after('<span class="error-message">Valore numerico non valido</span>').addClass('error');
                hasErrors = true;
            }
        } else if (inputType === 'email') {
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailRegex.test(value)) {
                $input.after('<span class="error-message">Formato email non valido</span>').addClass('error');
                hasErrors = true;
            }
        }
    });
    
    if (hasErrors) {
        $btn.prop('disabled', false).removeClass('btn-loading');
        return;
    }
        
        // Collect parameters
        const params = {};
        $('.param-input').each(function() {
            const dataset = $(this).data('dataset');
            const param = $(this).data('param');
            const value = $(this).val();
            
            if (!params[dataset]) {
                params[dataset] = {};
            }
            params[dataset][param] = value;
        });
        
        // Execute report
        $.ajax({
            url: `/api/report/${report.id}/execute`,
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ params: params }),
                success: function(response) {
                    $btn.prop('disabled', false).removeClass('btn-loading');
                    
                    if (response.success) {
                        $('#report-status').html('<div class="success-message">Report generato con successo!</div>');
                        
                        // Hide success message after 3 seconds
                        setTimeout(function() {
                            $('#report-status').empty();
                        }, 3000);
                        
                        // Export to PDF
                        const htmlPath = response.html_path;
                        const htmlFileName = htmlPath.split('/').pop();
                        
                        $.ajax({
                            url: `/api/report/${report.id}/pdf?html_path=${htmlFileName}`,
                            method: 'GET',
                            success: function(pdfResponse) {
                                if (pdfResponse.success) {
                                    // Display PDF in iframe
                                    const pdfPath = pdfResponse.pdf_path;
                                    const pdfName = pdfPath.split('/').pop();
                                    $('#report-iframe').attr('src', `/generated/${pdfName}?t=${Date.now()}`);
                                    $('#report-iframe').show();
                        } else {
                                    $btn.prop('disabled', false).removeClass('btn-loading');
                                    $('#report-error').text(pdfResponse.detail || 'Errore durante l\'esportazione in PDF').addClass('visible');
                                }
                            },
                            error: function(xhr) {
                                $btn.prop('disabled', false).removeClass('btn-loading');
                                let errorMessage = 'Errore durante l\'esportazione in PDF';
                                if (xhr.responseJSON && xhr.responseJSON.detail) {
                                    errorMessage = xhr.responseJSON.detail;
                                }
                                $('#report-error').text(errorMessage).addClass('visible');
                            }
                        });
                    } else {
                        $btn.prop('disabled', false).removeClass('btn-loading');
                        $('#report-error').text(response.detail || 'Errore durante la generazione del report').addClass('visible');
                    }
                },
                error: function(xhr) {
                    $btn.prop('disabled', false).removeClass('btn-loading');
                    let errorMessage = 'Errore durante la generazione del report';
                    if (xhr.responseJSON && xhr.responseJSON.detail) {
                        errorMessage = xhr.responseJSON.detail;
                    }
                    $('#report-error').text(errorMessage).addClass('visible');
                }
        });
    });
    
    // Back button
    $('#back-btn').on('click', function() {
        window.location.href = '/reports';
    });
    
    // Export to Excel button
    $('#export-excel-btn').on('click', function() {
        const $btn = $(this);
        $btn.prop('disabled', true).addClass('btn-loading');
        $('#report-error').removeClass('visible');
        $('#report-status').empty();
        $('#report-iframe').hide();
        
        // Clear previous validation errors
        $('.param-input').next('.error-message').remove();
        $('.param-input').removeClass('error');
        
        // Validate parameters
        let hasErrors = false;
        $('.param-input').each(function() {
            const $input = $(this);
            const value = $input.val().trim();
            const inputType = $input.attr('type');
            
            // Check if empty
            if (!value) {
                $input.after('<span class="error-message">Campo obbligatorio</span>').addClass('error');
                hasErrors = true;
                return;
            }
            
            // Validate input types
            if (inputType === 'number') {
                if (isNaN(parseFloat(value)) || !isFinite(value)) {
                    $input.after('<span class="error-message">Valore numerico non valido</span>').addClass('error');
                    hasErrors = true;
                }
            } else if (inputType === 'email') {
                const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
                if (!emailRegex.test(value)) {
                    $input.after('<span class="error-message">Formato email non valido</span>').addClass('error');
                    hasErrors = true;
                }
            }
        });
        
        if (hasErrors) {
            $btn.prop('disabled', false).removeClass('btn-loading');
            return;
        }
        
        // Collect parameters
        const params = {};
        $('.param-input').each(function() {
            const dataset = $(this).data('dataset');
            const param = $(this).data('param');
            const value = $(this).val();
            
            if (!params[dataset]) {
                params[dataset] = {};
            }
            params[dataset][param] = value;
        });
        
        // Execute report and export to Excel
        $.ajax({
            url: `/api/report/${report.id}/execute`,
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ params: params }),
            success: function(response) {
                $btn.prop('disabled', false).removeClass('btn-loading');
                
                if (response.success) {
                    $('#report-status').html('<div class="success-message">Report generato con successo!</div>');
                    
                    // Hide success message after 3 seconds
                    setTimeout(function() {
                        $('#report-status').empty();
                    }, 3000);
                    
                    // Export to Excel
                    const htmlPath = response.html_path;
                    const htmlFileName = htmlPath.split('/').pop();
                    
                    $.ajax({
                        url: `/api/report/${report.id}/excel?html_path=${htmlFileName}&params=${encodeURIComponent(JSON.stringify(params))}`,
                        method: 'GET',
                            success: function(excelResponse) {
                                if (excelResponse.success) {
                                // Download Excel file
                                const excelPath = excelResponse.excel_path;
                                const excelName = excelPath.split('/').pop();
                                window.location.href = `/generated/${excelName}`;
                            } else {
                                $btn.prop('disabled', false).removeClass('btn-loading');
                                $('#report-error').text(excelResponse.detail || 'Errore durante l\'esportazione in Excel').addClass('visible');
                            }
                        },
                            error: function(xhr) {
                                $btn.prop('disabled', false).removeClass('btn-loading');
                                let errorMessage = 'Errore durante l\'esportazione in Excel';
                            if (xhr.responseJSON && xhr.responseJSON.detail) {
                                errorMessage = xhr.responseJSON.detail;
                            }
                            $('#report-error').text(errorMessage).addClass('visible');
                        }
                    });
                } else {
                    $('#report-error').text(response.detail || 'Errore durante la generazione del report').addClass('visible');
                }
            },
            error: function(xhr) {
                let errorMessage = 'Errore durante la generazione del report';
                if (xhr.responseJSON && xhr.responseJSON.detail) {
                    errorMessage = xhr.responseJSON.detail;
                }
                $('#report-error').text(errorMessage).addClass('visible');
                $btn.prop('disabled', false).removeClass('btn-loading');
            }
        });
    });
});
