// script.js

document.addEventListener('DOMContentLoaded', function() {
    const fileInput = document.querySelector('input[type="file"]');
    fileInput.addEventListener('change', function() {
        const fileName = this.files[0].name;
        const label = document.querySelector('.file-label');
        label.textContent = fileName;
    });
});