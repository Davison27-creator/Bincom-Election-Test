// Simple JavaScript for enhanced interactivity
document.addEventListener('DOMContentLoaded', function() {
    // Auto-submit forms when select changes
    const autoSubmitSelects = document.querySelectorAll('select[onchange]');
    autoSubmitSelects.forEach(select => {
        select.addEventListener('change', function() {
            this.form.submit();
        });
    });

    // Add loading states to buttons
    const buttons = document.querySelectorAll('.btn');
    buttons.forEach(button => {
        button.addEventListener('click', function(e) {
            if (this.type === 'submit' || this.href) {
                this.classList.add('loading');
                this.innerHTML = 'Loading...';
            }
        });
    });

    // Simple chart data for future enhancements
    console.log('Election Results System loaded successfully');
});