/**
 * Main.js - Core Functionality
 * Sidebar toggle, particles background, and service worker
 * Note: We use Framework7 CSS and icons but not the framework itself
 */

// Framework7 is loaded but NOT initialized to avoid DOM manipulation

// ===============================
// SIDEBAR TOGGLE WITH PERSISTENCE
// ===============================
(function () {
    const body = document.body;
    const btn = document.querySelector('.sidebar-toggle');

    // Restore saved state
    const saved = localStorage.getItem('mds_sidebar');
    if (saved === 'collapsed') {
        body.classList.add('sidebar-collapsed');
    }

    // Toggle on click
    if (btn) {
        btn.addEventListener('click', () => {
            body.classList.toggle('sidebar-collapsed');
            localStorage.setItem(
                'mds_sidebar',
                body.classList.contains('sidebar-collapsed') ? 'collapsed' : 'expanded'
            );
        });
    }
})();

// ===============================
// PARTICLE BACKGROUND (Mouse Interaction)
// ===============================
(function () {
    const canvas = document.getElementById('particle-canvas');
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    let width, height;
    let particles = [];

    // Mouse interaction
    let mouse = { x: null, y: null };
    window.addEventListener('mousemove', (e) => {
        mouse.x = e.clientX;
        mouse.y = e.clientY;
    });

    function resize() {
        width = canvas.width = window.innerWidth;
        height = canvas.height = window.innerHeight;
    }
    window.addEventListener('resize', resize);
    resize();

    class Particle {
        constructor() {
            this.x = Math.random() * width;
            this.y = Math.random() * height;
            this.vx = (Math.random() - 0.5) * 0.5;
            this.vy = (Math.random() - 0.5) * 0.5;
            this.size = Math.random() * 2 + 1;
            this.color = `rgba(${Math.random() * 50 + 100}, ${Math.random() * 50 + 100}, 255, ${Math.random() * 0.5})`;
        }

        update() {
            this.x += this.vx;
            this.y += this.vy;

            // Mouse interaction (Vortex/Repel)
            if (mouse.x != null) {
                let dx = mouse.x - this.x;
                let dy = mouse.y - this.y;
                let distance = Math.sqrt(dx * dx + dy * dy);
                if (distance < 200) {
                    const forceDirectionX = dx / distance;
                    const forceDirectionY = dy / distance;
                    const force = (200 - distance) / 200;
                    const directionX = forceDirectionX * force * 0.5;
                    const directionY = forceDirectionY * force * 0.5;
                    this.vx += directionX;
                    this.vy += directionY;
                }
            }

            // Friction
            this.vx *= 0.99;
            this.vy *= 0.99;

            // Boundaries
            if (this.x < 0 || this.x > width) this.vx = -this.vx;
            if (this.y < 0 || this.y > height) this.vy = -this.vy;
        }

        draw() {
            ctx.fillStyle = this.color;
            ctx.beginPath();
            ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
            ctx.fill();
        }
    }

    function initParticles() {
        particles = [];
        for (let i = 0; i < 100; i++) {
            particles.push(new Particle());
        }
    }
    initParticles();

    function animate() {
        // Clear with minimal opacity for trail effect
        ctx.fillStyle = 'rgba(233, 239, 255, 0.1)';
        ctx.fillRect(0, 0, width, height);

        particles.forEach(p => {
            p.update();
            p.draw();
        });
        requestAnimationFrame(animate);
    }
    animate();
})();

// ===============================
// SERVICE WORKER REGISTRATION
// ===============================
if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        navigator.serviceWorker
            .register('/static/sw.js')
            .then(registration => {
                console.log('SW registered: ', registration);
            })
            .catch(registrationError => {
                console.log('SW registration failed: ', registrationError);
            });
    });
}

// ===============================
// SKELETON LOADING HELPERS
// ===============================
window.showSkeleton = function (containerId) {
    const container = document.getElementById(containerId);
    if (container) {
        container.classList.add('skeleton');
    }
};

window.hideSkeleton = function (containerId) {
    const container = document.getElementById(containerId);
    if (container) {
        container.classList.remove('skeleton');
    }
};

// ===============================
// SESSION TIMER
// ===============================
(function () {
    const timerElement = document.getElementById('session-timer');
    if (!timerElement) return;

    let sessionTime = 30 * 60; // 30 minutes in seconds
    let idleTime = 0; // Idle time counter
    const idleThreshold = 20 * 60; // 20 minutes

    // Reset idle time on user activity
    const resetIdle = () => {
        idleTime = 0;
        // Update user status to "Online" if it was "Ausente"
        if (window.userStatus === 'ausente') {
            window.userStatus = 'online';
            if (typeof updateUserStatus === 'function') {
                updateUserStatus('online');
            }
        }
    };

    // Listen to user activity
    ['mousedown', 'mousemove', 'keypress', 'scroll', 'touchstart', 'click'].forEach(event => {
        document.addEventListener(event, resetIdle, true);
    });

    // Update timer every second
    setInterval(() => {
        sessionTime--;
        idleTime++;

        // Check if user is idle (20 minutes)
        if (idleTime >= idleThreshold && window.userStatus !== 'ausente') {
            window.userStatus = 'ausente';
            if (typeof updateUserStatus === 'function') {
                updateUserStatus('ausente');
            }
        }

        // Format time as MM:SS
        const minutes = Math.floor(sessionTime / 60);
        const seconds = sessionTime % 60;
        timerElement.textContent = `⏱️ ${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;

        // Warn when time is low
        if (sessionTime <= 5 * 60) {
            timerElement.style.color = '#ef4444'; // Red
        }

        // Session expired
        if (sessionTime <= 0) {
            window.location.href = '/logout';
        }
    }, 1000);

    // Initialize user status
    window.userStatus = 'online';
})();
