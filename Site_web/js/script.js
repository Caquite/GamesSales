function toggleInfo() {
    const popup = document.getElementById('infoPopup');
    popup.classList.toggle('visible');
}

document.addEventListener('click', function(e) {
    const popup = document.getElementById('infoPopup');
    const btn = document.querySelector('.info');
    if (!popup.contains(e.target) && e.target !== btn) {
        popup.classList.remove('visible');
    }
});

document.getElementById('monMenu').addEventListener('change', function() {
    const valeur = this.value;
    console.log('Valeur choisie :', valeur);
});