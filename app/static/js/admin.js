


/* ============================================================
   myTemplates - Admin JavaScript
   ============================================================ */

document.addEventListener('DOMContentLoaded', function() {
    
    // ---- Confirm Delete ----
    document.querySelectorAll('.delete-confirm').forEach(btn => {
        btn.addEventListener('click', function(e) {
            if (!confirm('Are you sure you want to delete this item?')) {
                e.preventDefault();
            }
        });
    });
    
    // ---- Toggle Active Status ----
    document.querySelectorAll('.toggle-status').forEach(btn => {
        btn.addEventListener('click', function(e) {
            if (!confirm('Toggle status of this item?')) {
                e.preventDefault();
            }
        });
    });
    
    // ---- Preview Image ----
    const imageInputs = document.querySelectorAll('input[type="url"]');
    imageInputs.forEach(input => {
        input.addEventListener('input', function() {
            const preview = document.getElementById(this.dataset.previewId);
            if (preview && this.value) {
                preview.src = this.value;
                preview.style.display = 'block';
            }
        });
    });
});




