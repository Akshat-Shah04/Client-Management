function searchTable() {
    const query = document.getElementById('searchBar').value.toLowerCase()
    const rows = document.querySelectorAll('table tbody tr')
    rows.forEach((row) => {
      const name = row.cells[1].textContent.toLowerCase()
      const mobile = row.cells[2].textContent.toLowerCase()
      if (name.includes(query) || mobile.includes(query)) {
        row.style.display = ''
      } else {
        row.style.display = 'none'
      }
    })
}
  
