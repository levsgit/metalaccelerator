document.addEventListener('DOMContentLoaded', function () {
    // Smooth scrolling for navigation links
    document.querySelectorAll('nav a').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
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
        contactForm.addEventListener('submit', function (e) {
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

    // Spark effect for all CTA buttons
    const ctaButtons = document.querySelectorAll('.cta-button');
    let lastX = 0;
    let lastY = 0;
    let lastTime = 0;
    let isHovering = false;

    function createSpark(x, y, button) {
        const spark = document.createElement('div');
        spark.className = 'spark';
        
        // Random angle for circular spread (0 to 360 degrees)
        const angle = Math.random() * Math.PI * 2;
        
        // Calculate distance
        const distance = Math.random() * 100 + 150; // 150-250px distance
        
        // Calculate spread
        const spreadX = Math.cos(angle) * distance;
        const spreadY = Math.sin(angle) * distance;
        
        // Get button's position relative to viewport
        const rect = button.getBoundingClientRect();
        const scrollLeft = window.pageXOffset || document.documentElement.scrollLeft;
        const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
        
        // Calculate absolute position including scroll and margins
        const absoluteX = rect.left + x + scrollLeft;
        const absoluteY = rect.top + y + scrollTop;
        
        // Set initial position
        spark.style.left = absoluteX + 'px';
        spark.style.top = absoluteY + 'px';
        
        // Set random rotation
        const rotation = Math.random() * 720 - 360; // -360 to 360 degrees
        spark.style.setProperty('--rotation', `${rotation}deg`);
        
        // Add spark to body
        document.body.appendChild(spark);
        
        // Animate spark with circular spread
        const duration = Math.random() * 500 + 1000; // 1000-1500ms
        
        spark.animate([
            { 
                transform: 'translate(0, 0) scale(0) rotate(0deg)',
                opacity: 1
            },
            { 
                transform: `translate(${spreadX}px, ${spreadY}px) scale(1.5) rotate(${rotation}deg)`,
                opacity: 0.7
            },
            { 
                transform: `translate(${spreadX * 1.2}px, ${spreadY * 1.2}px) scale(1) rotate(${rotation * 1.5}deg)`,
                opacity: 0
            }
        ], {
            duration: duration,
            easing: 'cubic-bezier(0.2, 0.8, 0.2, 1)'
        }).onfinish = () => spark.remove();
    }

    function createSparkBurst(x, y, button) {
        // Create multiple sparks in a burst
        const sparkCount =10; // Increased from 8 to 20 (2.5x more sparks)
        for (let i = 0; i < sparkCount; i++) {
            createSpark(x, y, button);
        }
    }

    ctaButtons.forEach(button => {
        button.addEventListener('mouseenter', (e) => {
            isHovering = true;
            const rect = button.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            createSparkBurst(x, y, button);
        });

        button.addEventListener('mouseleave', (e) => {
            isHovering = false;
            const rect = button.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            createSparkBurst(x, y, button);
        });
    });
}); 