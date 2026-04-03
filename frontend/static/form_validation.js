document.addEventListener('DOMContentLoaded', () => {
    const heartForm = document.getElementById('heartForm');
    
    if (heartForm) {
        heartForm.addEventListener('submit', (e) => {
            let isValid = true;
            let errorLog = [];

            // Targeted validation for core health metrics
            const age = heartForm.querySelector('input[name="age"]').value;
            const bps = heartForm.querySelector('input[name="trestbps"]').value;

            if (age < 1 || age > 115) {
                errorLog.push("Age must be between 1 and 115.");
                isValid = false;
            }
            if (bps < 60 || bps > 220) {
                errorLog.push("Resting Blood Pressure should be between 60 and 220 mmHg.");
                isValid = false;
            }

            if (!isValid) {
                alert(errorLog.join("\n"));
                e.preventDefault();
            }
        });
    }
});