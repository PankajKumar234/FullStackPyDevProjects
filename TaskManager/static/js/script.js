// static/js/script.js

function confirmDelete(taskId) {
    if (confirm("Are you sure you want to delete this task")) {
        window.location.href = '/delete-task/${taskId}';
    }
}