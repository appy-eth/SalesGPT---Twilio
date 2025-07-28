// Flash message auto-dismiss
document.addEventListener('DOMContentLoaded', function() {
    const flashMessages = document.querySelectorAll('.alert');
    flashMessages.forEach(function(message) {
        setTimeout(function() {
            message.style.opacity = '0';
            setTimeout(function() {
                message.remove();
            }, 300);
        }, 3000);
    });
});

// Form validation
document.addEventListener('DOMContentLoaded', function() {
    const forms = document.querySelectorAll('form');
    forms.forEach(function(form) {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        });
    });
});

// File upload preview
document.addEventListener('DOMContentLoaded', function() {
    const fileInput = document.querySelector('input[type="file"]');
    if (fileInput) {
        fileInput.addEventListener('change', function(event) {
            const fileName = event.target.files[0].name;
            const fileLabel = event.target.nextElementSibling;
            if (fileLabel) {
                fileLabel.textContent = fileName;
            }
        });
    }
});

// Campaign status updates
document.addEventListener('DOMContentLoaded', function() {
    const statusButtons = document.querySelectorAll('.status-update');
    statusButtons.forEach(function(button) {
        button.addEventListener('click', async function(event) {
            event.preventDefault();
            const leadId = this.dataset.leadId;
            const newStatus = this.dataset.status;
            
            try {
                const response = await fetch(`/leads/${leadId}/status`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ status: newStatus })
                });
                
                if (response.ok) {
                    const data = await response.json();
                    const statusBadge = document.querySelector(`#lead-${leadId} .status-badge`);
                    if (statusBadge) {
                        statusBadge.className = `status-badge badge bg-${newStatus}`;
                        statusBadge.textContent = newStatus;
                    }
                } else {
                    alert('Failed to update status');
                }
            } catch (error) {
                console.error('Error:', error);
                alert('An error occurred while updating status');
            }
        });
    });
});

// Notes editor
document.addEventListener('DOMContentLoaded', function() {
    const notesEditors = document.querySelectorAll('.notes-editor');
    notesEditors.forEach(function(editor) {
        editor.addEventListener('blur', async function(event) {
            const leadId = this.dataset.leadId;
            const notes = this.value;
            
            try {
                const response = await fetch(`/leads/${leadId}/notes`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ notes: notes })
                });
                
                if (!response.ok) {
                    alert('Failed to save notes');
                }
            } catch (error) {
                console.error('Error:', error);
                alert('An error occurred while saving notes');
            }
        });
    });
}); 