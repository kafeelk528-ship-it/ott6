// Simple fade-up animation for cards and hero section
document.addEventListener("DOMContentLoaded", () => {
  const fadeElements = document.querySelectorAll(".card, .hero-left, .hero-right");

  fadeElements.forEach((el, index) => {
    el.style.opacity = "0";
    el.style.transform = "translateY(20px)";

    setTimeout(() => {
      el.style.opacity = "1";
      el.style.transform = "translateY(0)";
      el.style.transition = "all .6s ease";
    }, 150 * index);
  });
});

// Future mobile menu support (optional)
function toggleMenu() {
  const nav = document.querySelector(".nav");
  nav.classList.toggle("open");
}
