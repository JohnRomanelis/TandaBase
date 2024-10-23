// app/static/js/song.js
document.addEventListener('DOMContentLoaded', function() {
    const typeSelect = document.getElementById('type_id');
    const styleField = document.getElementById('style_field');

    function toggleStyleField() {
        if (typeSelect.options[typeSelect.selectedIndex].text === 'Tango') {
            styleField.style.display = 'block';
        } else {
            styleField.style.display = 'none';
        }
    }

    typeSelect.addEventListener('change', toggleStyleField);
    toggleStyleField(); // Initial check
});
