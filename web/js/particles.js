// Particle/Spark Animation System for Immersive Experience

class ParticleSystem {
    constructor(canvas) {
        this.canvas = canvas;
        this.ctx = canvas.getContext('2d');
        this.particles = [];
        this.maxParticles = 80;
        this.mouse = { x: 0, y: 0 };
        
        this.resizeCanvas();
        this.init();
        
        window.addEventListener('resize', () => this.resizeCanvas());
        window.addEventListener('mousemove', (e) => this.updateMouse(e));
    }
    
    resizeCanvas() {
        this.canvas.width = window.innerWidth;
        this.canvas.height = window.innerHeight;
    }
    
    updateMouse(e) {
        this.mouse.x = e.clientX;
        this.mouse.y = e.clientY;
    }
    
    init() {
        for (let i = 0; i < this.maxParticles; i++) {
            this.particles.push(this.createParticle());
        }
    }
    
    createParticle() {
        return {
            x: Math.random() * this.canvas.width,
            y: Math.random() * this.canvas.height,
            size: Math.random() * 2 + 0.5,
            speedX: (Math.random() - 0.5) * 0.5,
            speedY: (Math.random() - 0.5) * 0.5,
            opacity: Math.random() * 0.5 + 0.2,
            color: this.getRandomColor()
        };
    }
    
    getRandomColor() {
        const colors = [
            'rgba(233, 69, 96, ',  // highlight-color
            'rgba(52, 152, 219, ', // info
            'rgba(240, 240, 240, ', // text-color
            'rgba(15, 52, 96, '    // accent-color
        ];
        return colors[Math.floor(Math.random() * colors.length)];
    }
    
    drawParticle(particle) {
        this.ctx.beginPath();
        this.ctx.arc(particle.x, particle.y, particle.size, 0, Math.PI * 2);
        this.ctx.fillStyle = particle.color + particle.opacity + ')';
        this.ctx.fill();
        
        // Add glow effect
        this.ctx.shadowBlur = 10;
        this.ctx.shadowColor = particle.color + particle.opacity + ')';
    }
    
    drawConnections() {
        for (let i = 0; i < this.particles.length; i++) {
            for (let j = i + 1; j < this.particles.length; j++) {
                const dx = this.particles[i].x - this.particles[j].x;
                const dy = this.particles[i].y - this.particles[j].y;
                const distance = Math.sqrt(dx * dx + dy * dy);
                
                if (distance < 120) {
                    this.ctx.beginPath();
                    this.ctx.strokeStyle = 'rgba(233, 69, 96, ' + (0.15 * (1 - distance / 120)) + ')';
                    this.ctx.lineWidth = 0.5;
                    this.ctx.moveTo(this.particles[i].x, this.particles[i].y);
                    this.ctx.lineTo(this.particles[j].x, this.particles[j].y);
                    this.ctx.stroke();
                }
            }
        }
    }
    
    updateParticle(particle) {
        particle.x += particle.speedX;
        particle.y += particle.speedY;
        
        // Mouse interaction
        const dx = this.mouse.x - particle.x;
        const dy = this.mouse.y - particle.y;
        const distance = Math.sqrt(dx * dx + dy * dy);
        
        if (distance < 100) {
            particle.x -= dx * 0.01;
            particle.y -= dy * 0.01;
        }
        
        // Wrap around edges
        if (particle.x < 0) particle.x = this.canvas.width;
        if (particle.x > this.canvas.width) particle.x = 0;
        if (particle.y < 0) particle.y = this.canvas.height;
        if (particle.y > this.canvas.height) particle.y = 0;
    }
    
    animate() {
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
        
        // Draw connections first (behind particles)
        this.drawConnections();
        
        // Update and draw particles
        for (let particle of this.particles) {
            this.updateParticle(particle);
            this.drawParticle(particle);
        }
        
        requestAnimationFrame(() => this.animate());
    }
}

// Scroll animation system
class ScrollAnimator {
    constructor() {
        this.elements = document.querySelectorAll('.animate-on-scroll');
        this.init();
        
        window.addEventListener('scroll', () => this.checkScroll());
        this.checkScroll(); // Initial check
    }
    
    init() {
        this.elements.forEach(el => {
            el.style.opacity = '0';
            el.style.transform = 'translateY(30px)';
            el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        });
    }
    
    checkScroll() {
        this.elements.forEach(el => {
            const rect = el.getBoundingClientRect();
            const windowHeight = window.innerHeight;
            
            if (rect.top < windowHeight * 0.85) {
                el.style.opacity = '1';
                el.style.transform = 'translateY(0)';
            }
        });
    }
}

// Sparkle effect on hover
class SparkleEffect {
    constructor() {
        this.sparkles = [];
        this.setupListeners();
    }
    
    setupListeners() {
        document.querySelectorAll('.feature-card, .stat-card').forEach(card => {
            card.addEventListener('mouseenter', (e) => this.createSparkle(e));
        });
    }
    
    createSparkle(e) {
        const rect = e.currentTarget.getBoundingClientRect();
        const sparkle = document.createElement('div');
        sparkle.className = 'sparkle';
        sparkle.style.left = (Math.random() * rect.width) + 'px';
        sparkle.style.top = (Math.random() * rect.height) + 'px';
        
        e.currentTarget.appendChild(sparkle);
        
        setTimeout(() => sparkle.remove(), 1000);
    }
}

// Initialize on load
document.addEventListener('DOMContentLoaded', function() {
    // Create canvas for particle system
    const canvas = document.createElement('canvas');
    canvas.id = 'particle-canvas';
    canvas.style.position = 'fixed';
    canvas.style.top = '0';
    canvas.style.left = '0';
    canvas.style.width = '100%';
    canvas.style.height = '100%';
    canvas.style.pointerEvents = 'none';
    canvas.style.zIndex = '1';
    canvas.style.opacity = '0.6';
    document.body.insertBefore(canvas, document.body.firstChild);
    
    // Initialize systems
    const particleSystem = new ParticleSystem(canvas);
    particleSystem.animate();
    
    const scrollAnimator = new ScrollAnimator();
    const sparkleEffect = new SparkleEffect();
    
    // Add animate-on-scroll class to sections
    document.querySelectorAll('.intro-section, .features-grid, .stats-section, .quick-access, .notice-section').forEach(section => {
        section.classList.add('animate-on-scroll');
    });
    
    // Add animate-on-scroll to feature cards with delay
    document.querySelectorAll('.feature-card').forEach((card, index) => {
        card.classList.add('animate-on-scroll');
        card.style.transitionDelay = (index * 0.1) + 's';
    });
});
