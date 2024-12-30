document.addEventListener("DOMContentLoaded", function () {
    const statusSelects = document.querySelectorAll(".status-select");
    statusSelects.forEach((select) => {
        const selectedStatus = select.getAttribute("data-status");
        if (selectedStatus) {
            select.value = selectedStatus; // Set the selected value dynamically
        }
    });
});
