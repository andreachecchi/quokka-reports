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
    
    // Load reports data
    const reports = REPORTS_DATA || [];
    
    // Populate category filter
    const categories = [...new Set(reports.map(r => r.category).filter(c => c))].sort();
    categories.forEach(category => {
        $('#category-filter').append(`<option value="${category}">${category}</option>`);
    });
    
    // Render reports table
    renderReports(reports);
    
    // Search functionality
    $('#search-input').on('keyup', function() {
        filterReports();
    });
    
    // Category filter
    $('#category-filter').on('change', function() {
        filterReports();
    });
    
    // Sort order
    $('#sort-order').on('change', function() {
        filterReports();
    });
    
    // Click on tag to filter
    $(document).on('click', '.tag', function() {
        const clickedTag = $(this).text().trim();
        const currentSearch = $('#search-input').val().trim();
        
        // Verifica se il tag è già nella ricerca (come parola singola o parte di un termine)
        const words = currentSearch.toLowerCase().split(/\s+/).filter(w => w.length > 0);
        const tagIndex = words.findIndex(w => w === clickedTag.toLowerCase());
        
        let newSearch;
        if (tagIndex !== -1) {
            // Rimuovi il tag dalla ricerca
            words.splice(tagIndex, 1);
            newSearch = words.join(' ');
        } else {
            // Aggiungi il tag alla ricerca
            if (currentSearch) {
                newSearch = currentSearch + ' ' + clickedTag;
            } else {
                newSearch = clickedTag;
            }
        }
        
        $('#search-input').val(newSearch);
        filterReports();
    });
    
    // Generate deterministic color from string
    function stringToColor(str) {
        let hash = 0;
        for (let i = 0; i < str.length; i++) {
            hash = str.charCodeAt(i) + ((hash << 5) - hash);
        }
        const hue = Math.abs(hash % 360);
        return `hsl(${hue}, 70%, 85%)`;
    }
    
    // Generate border color from string
    function stringToBorderColor(str) {
        let hash = 0;
        for (let i = 0; i < str.length; i++) {
            hash = str.charCodeAt(i) + ((hash << 5) - hash);
        }
        const hue = Math.abs(hash % 360);
        return `hsl(${hue}, 70%, 60%)`;
    }
    
    // Render reports
    function renderReports(reportsList) {
        const $tbody = $('#reports-body');
        $tbody.empty();
        
        if (reportsList.length === 0) {
            $('#no-reports').show();
            $('#reports-error').hide();
            return;
        }
        
        $('#no-reports').hide();
        $('#reports-error').hide();
        
        reportsList.forEach(report => {
            const tagsHtml = report.tags && report.tags.length > 0 
                ? report.tags.map(t => 
                    `<span class="tag" style="background-color: ${stringToColor(t)}; border: 1px solid ${stringToBorderColor(t)};">${t}</span>`
                ).join('') 
                : '';
            
            const $row = $(`
                <tr>
                    <td><strong>${report.name}</strong></td>
                    <td>${report.description}</td>
                    <td>${report.category}</td>
                    <td>${tagsHtml}</td>
                    <td>
                        <button class="btn btn-action run-btn" data-report-id="${report.id}">Esegui</button>
                    </td>
                </tr>
            `);
            
            $tbody.append($row);
        });
        
        // Run button handlers
        $('.run-btn').on('click', function() {
            const reportId = $(this).data('report-id');
            window.location.href = `/report/${reportId}`;
        });
    }
    
    // Filter and sort reports
    function filterReports() {
        const searchTerm = $('#search-input').val().toLowerCase().trim();
        const selectedCategory = $('#category-filter').val();
        const sortOrder = $('#sort-order').val();
        
        // Se la ricerca ha parole separate da spazio, applica logica AND
        const searchWords = searchTerm.split(/\s+/).filter(w => w.length > 0);
        
        let filtered = REPORTS_DATA.filter(report => {
            // Controlla se ogni parola cercata matcha almeno uno dei campi
            const matchesSearch = searchWords.every(word => {
                return report.name.toLowerCase().includes(word) ||
                       report.description.toLowerCase().includes(word) ||
                       (report.tags && report.tags.some(tag => tag.toLowerCase().includes(word)));
            });
            const matchesCategory = !selectedCategory || report.category === selectedCategory;
            return matchesSearch && matchesCategory;
        });
        
        // Sort
        filtered.sort((a, b) => {
            if (sortOrder === 'name-desc') {
                return b.name.localeCompare(a.name);
            }
            return a.name.localeCompare(b.name);
        });
        
        renderReports(filtered);
    }
});
