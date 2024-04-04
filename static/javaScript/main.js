// main.js
document.addEventListener('DOMContentLoaded', () => {
    // JavaScript to make the page interactive
    const navLinks = document.querySelectorAll('.nav-links li a');
    
    navLinks.forEach(link => {
        link.addEventListener('mouseenter', () => {
            console.log(`Hovering over ${link.textContent}`);
        });
    });
});
