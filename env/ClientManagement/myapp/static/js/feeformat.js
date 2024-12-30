document.addEventListener('DOMContentLoaded', function () {
const feeCells = document.querySelectorAll('.fee-cell');
feeCells.forEach(cell => {
    const fee = parseFloat(cell.textContent.replace(/,/g, '')); // Parse fee as a number
    if (!isNaN(fee)) {
    cell.textContent = fee.toLocaleString('en-IN'); // Format with commas
    }
});
});