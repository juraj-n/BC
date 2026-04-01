function setAllCheckboxes(checked) {
    document.querySelectorAll(".spectra-checkbox")
        .forEach(checkbox => checkbox.checked = checked)
}