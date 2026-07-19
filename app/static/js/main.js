


/* ============================================================
   myTemplates - Main JavaScript
   ============================================================ */

document.addEventListener('DOMContentLoaded', function() {
    
    // ---- Category Filter ----
    const categoryPills = document.querySelectorAll('.category-pill');
    const productCards = document.querySelectorAll('.product-card');
    
    if (categoryPills.length && productCards.length) {
        categoryPills.forEach(pill => {
            pill.addEventListener('click', function() {
                // Update active state
                categoryPills.forEach(p => p.classList.remove('active'));
                this.classList.add('active');
                
                const category = this.dataset.category;
                
                productCards.forEach((card, index) => {
                    if (category === 'all' || card.dataset.category === category) {
                        card.style.display = 'block';
                        card.style.opacity = '0';
                        card.style.transform = 'translateY(20px)';
                        
                        setTimeout(() => {
                            card.style.opacity = '1';
                            card.style.transform = 'translateY(0)';
                        }, index * 50 + 50);
                    } else {
                        card.style.display = 'none';
                    }
                });
            });
        });
    }
    
    // ---- Quick View (Product Card Click) ----
    const productCardsForClick = document.querySelectorAll('.product-card .btn');
    productCardsForClick.forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.stopPropagation();
            // Product detail page is linked, no action needed
        });
    });
    
    // ---- Smooth Scroll ----
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                e.preventDefault();
                target.scrollIntoView({ behavior: 'smooth' });
            }
        });
    });
    
    // ---- Image Lazy Loading ----
    if ('IntersectionObserver' in window) {
        const images = document.querySelectorAll('img[loading="lazy"]');
        const imageObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    if (img.dataset.src) {
                        img.src = img.dataset.src;
                        img.removeAttribute('data-src');
                    }
                    imageObserver.unobserve(img);
                }
            });
        });
        
        images.forEach(img => imageObserver.observe(img));
    }
});




