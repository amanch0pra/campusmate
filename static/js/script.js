/**
 * ╔═══════════════════════════════════════════════╗
 * ║  CAMPUS MATE — Neural Interaction Engine    ║
 * ║  LPU Intelligence Hub v3.0                   ║
 * ╚═══════════════════════════════════════════════╝
 */

'use strict';

// ============ DOM REFS ============
const chatContainer = document.getElementById('chatContainer');
const userInput     = document.getElementById('user-input');
const sendBtn       = document.getElementById('send-btn');
const modeSelect    = document.getElementById('modeSelect');
const toast         = document.getElementById('toast');

// ============ STATE ============
let currentMode = 'auto';
let isThinking  = false;
let toastTimer  = null;

// ============ PARTICLE SYSTEM ============
(function initParticles() {
    const canvas = document.getElementById('particleCanvas');
    if (!canvas) return;
    const ctx = canvas.getContext('2d');

    let particles = [];
    const COUNT = 60;

    function resize() {
        canvas.width  = window.innerWidth;
        canvas.height = window.innerHeight;
    }

    class Particle {
        constructor() { this.reset(); }
        reset() {
            this.x      = Math.random() * canvas.width;
            this.y      = Math.random() * canvas.height;
            this.size   = Math.random() * 1.8 + 0.3;
            this.speedX = (Math.random() - 0.5) * 0.4;
            this.speedY = (Math.random() - 0.5) * 0.4;
            this.opacity = Math.random() * 0.4 + 0.05;
            // Colors: orange, cyan, indigo
            const palette = ['255,107,53', '6,182,212', '99,102,241', '16,185,129'];
            this.color = palette[Math.floor(Math.random() * palette.length)];
        }
        update() {
            this.x += this.speedX;
            this.y += this.speedY;
            if (this.x < 0 || this.x > canvas.width ||
                this.y < 0 || this.y > canvas.height) {
                this.reset();
            }
        }
        draw() {
            ctx.beginPath();
            ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
            ctx.fillStyle = `rgba(${this.color},${this.opacity})`;
            ctx.fill();
        }
    }

    function init() {
        resize();
        particles = Array.from({ length: COUNT }, () => new Particle());
    }

    function animate() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        particles.forEach(p => { p.update(); p.draw(); });

        // Draw subtle connections
        for (let i = 0; i < particles.length; i++) {
            for (let j = i + 1; j < particles.length; j++) {
                const dx = particles[i].x - particles[j].x;
                const dy = particles[i].y - particles[j].y;
                const dist = Math.sqrt(dx * dx + dy * dy);
                if (dist < 130) {
                    ctx.beginPath();
                    ctx.strokeStyle = `rgba(255,107,53,${0.04 * (1 - dist / 130)})`;
                    ctx.lineWidth = 0.5;
                    ctx.moveTo(particles[i].x, particles[i].y);
                    ctx.lineTo(particles[j].x, particles[j].y);
                    ctx.stroke();
                }
            }
        }

        requestAnimationFrame(animate);
    }

    window.addEventListener('resize', resize);
    init();
    animate();
})();

// ============ INIT ============
document.addEventListener('DOMContentLoaded', () => {
    // Auto-resize textarea
    userInput.addEventListener('input', function () {
        this.style.height = 'auto';
        this.style.height = Math.min(this.scrollHeight, 150) + 'px';
    });

    // Enter to send (shift+enter = newline)
    userInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });

    // Initial scroll
    chatContainer.scrollTop = chatContainer.scrollHeight;

    // Focus input
    setTimeout(() => userInput.focus(), 300);
});

// ============ MODE CHANGE ============
window.changeMode = function () {
    currentMode = modeSelect.value;
    const modeName = modeSelect.options[modeSelect.selectedIndex].text;
    appendMessage('bot', `**Mode Updated:** Now operating in **${modeName}** — neural pathways re-calibrated for precision retrieval in this domain.`, null, false);
    showToast(`⚡ Switched to ${modeName}`);
};

// ============ QUICK QUERIES ============
window.setQuery = function (text) {
    userInput.value = text;
    userInput.dispatchEvent(new Event('input'));
    sendMessage();
};

window.askQuestion = function (text) {
    // Hide suggested questions smoothly
    const suggestions = document.getElementById('suggestedQuestions');
    if (suggestions) {
        suggestions.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
        suggestions.style.opacity = '0';
        suggestions.style.transform = 'translateY(-10px)';
        setTimeout(() => suggestions.remove(), 500);
    }
    userInput.value = text;
    userInput.dispatchEvent(new Event('input'));
    sendMessage();
};

// ============ CLEAR CHAT ============
window.clearChat = function () {
    // Remove all messages except welcome
    const rows = chatContainer.querySelectorAll('.message-row:not(#welcomeMsg)');
    rows.forEach(row => {
        row.style.transition = 'opacity 0.3s ease, transform 0.3s ease';
        row.style.opacity = '0';
        row.style.transform = 'scale(0.95)';
        setTimeout(() => row.remove(), 300);
    });

    // Also remove suggestion panel if gone, recreate
    const existingSug = document.getElementById('suggestedQuestions');
    if (!existingSug) {
        setTimeout(() => {
            const sugDiv = document.createElement('div');
            sugDiv.className = 'suggested-questions';
            sugDiv.id = 'suggestedQuestions';
            sugDiv.innerHTML = `
                <h3><i class="fas fa-bolt"></i>&nbsp;POPULAR QUERIES</h3>
                <div class="question-chips" id="questionChips">
                    <div class="question-chip" onclick="askQuestion('What is the fee structure for BTech at LPU?')">🎓 BTech Fee Structure</div>
                    <div class="question-chip" onclick="askQuestion('How to check attendance on UMS portal?')">📋 Check UMS Attendance</div>
                    <div class="question-chip" onclick="askQuestion('What hostel facilities are available for boys?')">🏠 Hostel Facilities</div>
                    <div class="question-chip" onclick="askQuestion('Which top companies visit LPU for placements?')">💼 Top Placement Companies</div>
                    <div class="question-chip" onclick="askQuestion('How to apply for duty leave at LPU?')">📅 Duty Leave Process</div>
                    <div class="question-chip" onclick="askQuestion('How does the LPUNEST scholarship work?')">🏆 LPUNEST Scholarship</div>
                    <div class="question-chip" onclick="askQuestion('What is the attendance rule at LPU?')">⚠️ Attendance Rules</div>
                    <div class="question-chip" onclick="askQuestion('What societies and clubs are at LPU?')">🎭 Clubs & Societies</div>
                </div>`;
            chatContainer.appendChild(sugDiv);
        }, 400);
    }

    showToast('🗑️ Chat cleared');
};

// ============ SEND MESSAGE ============
async function sendMessage() {
    const text = userInput.value.trim();
    if (!text || isThinking) return;

    // Clear suggestions panel if present
    const suggestions = document.getElementById('suggestedQuestions');
    if (suggestions) {
        suggestions.style.transition = 'opacity 0.4s ease';
        suggestions.style.opacity = '0';
        setTimeout(() => suggestions.remove(), 400);
    }

    // Render user message
    appendUserMessage(text);
    userInput.value = '';
    userInput.style.height = 'auto';
    isThinking = true;

    // Update send button state
    sendBtn.classList.add('loading');
    sendBtn.innerHTML = '<i class="fas fa-circle-notch fa-spin"></i>';

    // Show typing indicator
    const loadingId = showTypingIndicator();

    try {
        const response = await fetch('/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: text, mode: currentMode })
        });

        if (!response.ok) throw new Error(`HTTP ${response.status}`);

        const data = await response.json();

        removeTypingIndicator(loadingId);
        isThinking = false;
        resetSendBtn();

        appendMessage('bot', data.response, data, true);

    } catch (err) {
        console.error('[Vertos] Network Error:', err);
        removeTypingIndicator(loadingId);
        isThinking = false;
        resetSendBtn();
        appendMessage('bot',
            '⚠️ **Connection Lost** — Could not reach the neural link. Check your internet connection and try again.',
            null, false
        );
    }
}

function resetSendBtn() {
    sendBtn.classList.remove('loading');
    sendBtn.innerHTML = '<i class="fas fa-paper-plane"></i>';
}

// ============ APPEND USER MESSAGE ============
function appendUserMessage(text) {
    const row = document.createElement('div');
    row.classList.add('message-row', 'user');

    row.innerHTML = `
        <div class="message-content">
            <div class="avatar user-avatar">S</div>
            <div class="text-block">
                <div class="text-main">${escapeHtml(text)}</div>
            </div>
        </div>`;

    chatContainer.appendChild(row);
    scrollToBottom();
}

// ============ APPEND BOT MESSAGE ============
function appendMessage(sender, text, meta = null, showActions = true) {
    const row = document.createElement('div');
    row.classList.add('message-row', sender);

    const content = document.createElement('div');
    content.classList.add('message-content');

    const avatar = document.createElement('div');
    avatar.classList.add('avatar', `${sender}-avatar`);
    avatar.textContent = sender === 'bot' ? 'V' : 'S';

    const textBlock = document.createElement('div');
    textBlock.classList.add('text-block');

    const mode = meta.mode || 'University';
        const method = meta.method || 'neural';
        // thought process removed

    // Main text
    const textMain = document.createElement('div');
    textMain.classList.add('text-main');
    textMain.innerHTML = formatMarkdown(text);
    textBlock.appendChild(textMain);

    // confidence badge removed

    // Action buttons
    if (sender === 'bot' && showActions && meta && !text.includes('Mode Updated')) {
        const actions = document.createElement('div');
        actions.classList.add('msg-actions');

        // Copy button
        const copyBtn = document.createElement('button');
        copyBtn.classList.add('bot-action-btn');
        copyBtn.innerHTML = '<i class="fas fa-copy"></i> Copy';
        copyBtn.onclick = () => {
            const raw = text.replace(/\*\*(.*?)\*\*/g, '$1').replace(/\n/g, '\n');
            navigator.clipboard.writeText(raw).then(() => {
                copyBtn.innerHTML = '<i class="fas fa-check"></i> Copied!';
                copyBtn.style.background = 'var(--accent-emerald)';
                copyBtn.style.color = 'white';
                copyBtn.style.borderColor = 'var(--accent-emerald)';
                setTimeout(() => {
                    copyBtn.innerHTML = '<i class="fas fa-copy"></i> Copy';
                    copyBtn.style.background = '';
                    copyBtn.style.color = '';
                    copyBtn.style.borderColor = '';
                }, 2000);
            });
        };
        actions.appendChild(copyBtn);

        // Share via UMS button
        const umsBtn = document.createElement('button');
        umsBtn.classList.add('bot-action-btn');
        umsBtn.innerHTML = '<i class="fas fa-external-link-alt"></i> Open UMS';
        umsBtn.onclick = () => window.open('https://ums.lpu.in/', '_blank');
        actions.appendChild(umsBtn);

        textBlock.appendChild(actions);
    }

    content.appendChild(avatar);
    content.appendChild(textBlock);
    row.appendChild(content);
    chatContainer.appendChild(row);
    scrollToBottom();
}

// ============ TYPING INDICATOR ============
function showTypingIndicator() {
    const id = 'typing-' + Date.now();
    const row = document.createElement('div');
    row.classList.add('message-row', 'bot');
    row.id = id;
    row.innerHTML = `
        <div class="message-content">
            <div class="avatar bot-avatar">V</div>
            <div class="text-block">
                <div class="typing-indicator">
                    <span></span><span></span><span></span>
                </div>
            </div>
        </div>`;
    chatContainer.appendChild(row);
    scrollToBottom();
    return id;
}

function removeTypingIndicator(id) {
    const el = document.getElementById(id);
    if (el) {
        el.style.transition = 'opacity 0.2s ease';
        el.style.opacity = '0';
        setTimeout(() => el.remove(), 200);
    }
}

// ============ TOAST ============
function showToast(message) {
    if (!toast) return;
    toast.textContent = message;
    toast.classList.add('show');
    if (toastTimer) clearTimeout(toastTimer);
    toastTimer = setTimeout(() => toast.classList.remove('show'), 2800);
}

// ============ SCROLL ============
function scrollToBottom() {
    chatContainer.scrollTo({
        top: chatContainer.scrollHeight,
        behavior: 'smooth'
    });
}

// ============ MARKDOWN FORMATTER ============
function formatMarkdown(text) {
    if (!text) return '';

    // Escape first if user-content, but bot content comes from server
    let t = text
        // Headers
        .replace(/^### (.+)$/gm, '<h4 style="color:var(--lpu-orange);margin:12px 0 6px;font-size:0.95rem;">$1</h4>')
        .replace(/^## (.+)$/gm,  '<h3 style="color:var(--accent-cyan);margin:14px 0 8px;font-size:1.05rem;">$1</h3>')
        .replace(/^# (.+)$/gm,   '<h2 style="color:var(--text-bright);margin:16px 0 10px;font-size:1.15rem;">$1</h2>')
        // Bold
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
        // Italic
        .replace(/\*(.*?)\*/g, '<em>$1</em>')
        // Inline code
        .replace(/`([^`]+)`/g, '<code>$1</code>')
        // Bullet points (- or * at line start)
        .replace(/^[\-\*] (.+)$/gm, '<li>$1</li>')
        // Ordered list
        .replace(/^\d+\. (.+)$/gm, '<li style="list-style-type:decimal;">$1</li>')
        // Wrap consecutive <li> in <ul>
        .replace(/(<li>.*?<\/li>(\s*<li>.*?<\/li>)*)/gs, '<ul style="margin:8px 0;padding-left:20px;">$1</ul>')
        // Newlines to <br>
        .replace(/\n\n/g, '<br><br>')
        .replace(/\n/g, '<br>')
        // URLs
        .replace(/(https?:\/\/[^\s<>"]+)/g, '<a href="$1" target="_blank" rel="noopener">$1</a>');

    return t;
}

// ============ HTML ESCAPE (user msgs) ============
function escapeHtml(str) {
    const div = document.createElement('div');
    div.appendChild(document.createTextNode(str));
    return div.innerHTML;
}

// ============ HELPERS ============
function capitalizeMode(mode) {
    const map = {
        'auto': 'General',
        'Academic': 'Academic',
        'Admissions and Administration': 'Admissions',
        'Campus Life': 'Campus Life',
        'Placements and Career': 'Placements',
        'Rules Safety and Grievance': 'Rules & Safety',
        'system': 'System',
        'error': 'System',
        'groq_braintrust': 'Groq',
        'semantic_fallback': 'Semantic',
    };
    return map[mode] || mode;
}
