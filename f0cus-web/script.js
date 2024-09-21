document.addEventListener('scroll', function() {
    const sections = document.querySelectorAll('.content-section');
    sections.forEach(section => {
        if (section.getBoundingClientRect().top < window.innerHeight && section.getBoundingClientRect().bottom >= 0) {
            console.log(`${section.querySelector('h2').innerText} is in view!`);
        }
    });
});
