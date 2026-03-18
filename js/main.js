document.addEventListener('DOMContentLoaded', () => {
    // 1. Navigation Scroll Effect
    const navbar = document.querySelector('.navbar');
    
    window.addEventListener('scroll', () => {
        if (window.scrollY > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    });

    // 1.5 Theme Toggle Logic
    const themeToggles = document.querySelectorAll('.theme-toggle');
    const prefersDarkScheme = window.matchMedia("(prefers-color-scheme: dark)");
    
    // Check for saved theme preference or system preference
    const currentTheme = localStorage.getItem("theme");
    if (currentTheme == "dark" || (!currentTheme && prefersDarkScheme.matches)) {
        document.body.classList.add("dark-mode");
        updateThemeIcons("dark");
    }

    themeToggles.forEach(toggle => {
        toggle.addEventListener("click", function() {
            document.body.classList.toggle("dark-mode");
            let theme = "light";
            if (document.body.classList.contains("dark-mode")) {
                theme = "dark";
            }
            updateThemeIcons(theme);
            localStorage.setItem("theme", theme);
        });
    });

    function updateThemeIcons(theme) {
        themeToggles.forEach(btn => {
            const icon = btn.querySelector('i');
            if (theme === "dark") {
                icon.classList.remove('ph-moon');
                icon.classList.add('ph-sun');
            } else {
                icon.classList.remove('ph-sun');
                icon.classList.add('ph-moon');
            }
        });
    }

    // 2. Mobile Menu Toggle (Basic Implementation)
    const menuToggle = document.querySelector('.menu-toggle');
    const navLinks = document.querySelector('.nav-links');
    
    if(menuToggle && navLinks) {
        menuToggle.addEventListener('click', () => {
            // Note: We need to style the mobile menu active state in CSS later
            // For now, simple toggle
            if (navLinks.style.display === 'flex') {
                navLinks.style.display = 'none';
                navLinks.classList.remove('mobile-open');
            } else {
                navLinks.style.display = 'flex';
                navLinks.style.flexDirection = 'column';
                navLinks.style.position = 'absolute';
                navLinks.style.top = '100%';
                navLinks.style.left = '0';
                navLinks.style.width = '100%';
                navLinks.style.backgroundColor = 'var(--bg-light)';
                navLinks.style.padding = '20px';
                navLinks.style.boxShadow = 'var(--shadow-md)';
                navLinks.classList.add('mobile-open');
            }
        });
    }

    // 3. Scroll Reveal Animations
    const revealElements = document.querySelectorAll('.reveal');
    
    const revealOptions = {
        threshold: 0.1,
        rootMargin: "0px 0px -50px 0px"
    };

    const revealOnScroll = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (!entry.isIntersecting) {
                return;
            } else {
                entry.target.classList.add('active');
                observer.unobserve(entry.target);
            }
        });
    }, revealOptions);

    revealElements.forEach(el => {
        revealOnScroll.observe(el);
    });
});
