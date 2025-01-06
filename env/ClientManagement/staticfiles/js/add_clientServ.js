document.addEventListener("DOMContentLoaded", function () {
    // Get the form element
    const form = document.querySelector("form");
  
    // Add event listener for form submission
    form.addEventListener("submit", function (event) {
        let valid = true;
  
        // Loop through each service checkbox
        const serviceCheckboxes = document.querySelectorAll(".form-check-input");
        serviceCheckboxes.forEach(function (checkbox) {
            const serviceId = checkbox.value;
  
            // Check if the service is selected
            if (checkbox.checked) {
                // Get the values for fee, status, and description (billing date is optional)
                const feeValue = document.querySelector(`input[name="fee_${serviceId}"]`).value;
                const statusValue = document.querySelector(`select[name="status_${serviceId}"]`).value;
                const billingDateValue = document.querySelector(`input[name="billing_date_${serviceId}"]`).value || "NA";
                const descValue = document.querySelector(`input[name="desc_${serviceId}"]`).value;
  
                // Validate fee and status (description is optional)
                if (!feeValue || !statusValue) {
                    valid = false;
                    alert("Please fill out all required fields (Fee and Status).");
                }
            }
        });
  
        // Prevent form submission if validation fails
        if (!valid) {
            event.preventDefault();
        }
    });
  
    // Show/hide service-specific inputs when checkboxes are toggled
    const serviceCheckboxes = document.querySelectorAll(".form-check-input");
    serviceCheckboxes.forEach(function (checkbox) {
        checkbox.addEventListener("change", function () {
            const serviceId = checkbox.value;
  
            // Get the input fields related to the service
            const feeInput = document.querySelector(`#fee-input-${serviceId}`);
            const statusInput = document.querySelector(`#status-input-${serviceId}`);
            const billingDateInput = document.querySelector(`#billing-date-input-${serviceId}`);
            const descInput = document.querySelector(`#desc-input-${serviceId}`);
  
            // Toggle visibility of inputs based on whether the checkbox is checked
            if (checkbox.checked) {
                feeInput.style.display = "block";
                statusInput.style.display = "block";
                billingDateInput.style.display = "block";
                descInput.style.display = "block";
            } else {
                feeInput.style.display = "none";
                statusInput.style.display = "none";
                billingDateInput.style.display = "none";
                descInput.style.display = "none";
            }
        });
    });
  });
  