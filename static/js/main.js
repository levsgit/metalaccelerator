document.addEventListener('DOMContentLoaded', function() {
    // Smooth scrolling for navigation links
    document.querySelectorAll('nav a').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            const targetElement = document.querySelector(targetId);
            targetElement.scrollIntoView({
                behavior: 'smooth'
            });
        });
    });

    // Form submission handling
    const contactForm = document.getElementById('contact-form');
    if (contactForm) {
        contactForm.addEventListener('submit', function(e) {
            e.preventDefault();
            // Here you would typically send the form data to your backend
            alert('Спасибо за ваше сообщение! Мы свяжемся с вами в ближайшее время.');
            contactForm.reset();
        });
    }

    // Добавляем класс fade-in-section ко всем секциям кроме hero
    const sections = document.querySelectorAll('section:not(.hero)');
    sections.forEach(section => {
        section.classList.add('fade-in-section');
    });

    // Создаем Intersection Observer
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('is-visible');
                // Отключаем наблюдение после появления
                observer.unobserve(entry.target);
            }
        });
    }, {
        // Начинаем анимацию когда элемент появится на 20% в зоне видимости
        threshold: 0.2,
        // Добавляем небольшой отступ снизу для более раннего срабатывания
        rootMargin: '0px 0px -50px 0px'
    });

    // Начинаем наблюдение за всеми секциями
    sections.forEach(section => {
        observer.observe(section);
    });
}); 