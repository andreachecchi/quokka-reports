function getCookie(name) {
    var value = "; " + document.cookie;
    var parts = value.split("; " + name + "=");
    if (parts.length == 2) return parts.pop().split(";").shift();
    return null;
}

function loadLocales(locale) {
    var locale = locale || getCookie('locale') || 'en';
    
    $.getJSON('/locales/' + locale + '.json', function(data) {
        function replacePlaceholders(element) {
            $(element).contents().filter(function() {
                return this.nodeType === 3;
            }).each(function() {
                var text = this.nodeValue;
                var match = text.match(/\{\{([^}]+)\}\}/);
                if (match) {
                    var key = match[1];
                    var value = data;
                    var keys = key.split('.');
                    for (var i = 0; i < keys.length; i++) {
                        value = value ? value[keys[i]] : undefined;
                    }
                    if (value) {
                        this.nodeValue = text.replace(/\{\{[^}]+\}\}/g, value);
                    }
                }
            });
            
            // Process attribute values (new functionality)
            if (element.attributes) {
                $.each(element.attributes, function() {
                    if (this.specified && this.value) {
                        var attrValue = this.value;
                        var match = attrValue.match(/\{\{([^}]+)\}\}/);
                        if (match) {
                            var key = match[1];
                            var replacementValue = data;
                            var keys = key.split('.');
                            for (var i = 0; i < keys.length; i++) {
                                replacementValue = replacementValue ? replacementValue[keys[i]] : undefined;
                            }
                            if (replacementValue) {
                                $(element).attr(this.name, attrValue.replace(/\{\{[^}]+\}\}/g, replacementValue));
                            }
                        }
                    }
                });
            }
        }

        $('*').each(function() {
            replacePlaceholders(this);
        });
    }).fail(function() {
        console.error('Locale file not found: locales/' + locale + '.json');
    });
}

// Auto-run on document ready
$(document).ready(function() {
    loadLocales();
});

