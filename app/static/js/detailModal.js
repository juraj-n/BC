const modal = document.getElementById('modal-detail');
const closeBtn = document.querySelector('.close-detail');
const clickableCells = document.querySelectorAll('.cell');

clickableCells.forEach(cell => {
    cell.addEventListener('click', function () {
        modal.style.display = 'flex';
    });
});

closeBtn.onclick = function () {
    modal.style.display = 'none';
}

window.onclick = function (event) {
    if (event.target == modal) {
        modal.style.display = 'none';
    }
}