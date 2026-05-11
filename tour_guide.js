class TourGuide {
    constructor(steps) {
        this.steps = steps;
        this.currentStep = 0;
        this.overlay = null;
        this.tooltip = null;
        this.init();
    }

    init() {
        if (!document.body) {
            window.addEventListener('DOMContentLoaded', () => this.init());
            return;
        }
        // Create or find overlay
        this.overlay = document.querySelector('.tour-overlay');
        if (!this.overlay) {
            this.overlay = document.createElement('div');
            this.overlay.className = 'tour-overlay';
            document.body.appendChild(this.overlay);
        }

        Object.assign(this.overlay.style, {
            position: 'fixed', top: 0, left: 0, width: '100%', height: '100%',
            background: 'rgba(0,0,0,0.8)', zIndex: 10000, display: 'none',
            transition: 'opacity 0.3s', backdropFilter: 'blur(4px)'
        });

        // Create or find tooltip
        this.tooltip = document.querySelector('.tour-tooltip');
        if (!this.tooltip) {
            this.tooltip = document.createElement('div');
            this.tooltip.className = 'tour-tooltip';
            document.body.appendChild(this.tooltip);
        }

        Object.assign(this.tooltip.style, {
            position: 'fixed', zIndex: 10001, display: 'none',
            background: '#0c0c0c', border: '1px solid #00e5ff',
            borderRadius: '12px', padding: '20px', width: '300px',
            boxShadow: '0 0 30px rgba(0, 229, 255, 0.3)',
            color: '#fff', fontFamily: 'Outfit, sans-serif',
            boxSizing: 'border-box'
        });

        this.tooltip.innerHTML = `
            <h4 id="tour-title" style="margin:0 0 10px 0; color:#00e5ff; font-size:14px; text-transform:uppercase; letter-spacing:1px;"></h4>
            <p id="tour-content" style="font-size:13px; color:#aaa; line-height:1.5; margin-bottom:20px;"></p>
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <span id="tour-progress" style="font-size:11px; color:#555;"></span>
                <div>
                    <button id="tour-prev" style="background:none; border:none; color:#555; cursor:pointer; font-size:11px; margin-right:10px;">BACK</button>
                    <button id="tour-next" style="background:#00e5ff; border:none; color:#000; padding:6px 15px; border-radius:4px; font-weight:700; cursor:pointer; font-size:11px;">NEXT</button>
                </div>
            </div>
        `;

        // Re-bind buttons to current instance
        this.tooltip.querySelector('#tour-next').onclick = () => this.next();
        this.tooltip.querySelector('#tour-prev').onclick = () => this.prev();
    }

    start() {
        this.currentStep = 0;
        this.overlay.style.display = 'block';
        this.tooltip.style.display = 'block';
        this.showStep();
    }

    showStep() {
        if (!this.steps || this.steps.length === 0) return;
        const step = this.steps[this.currentStep];
        const el = document.querySelector(step.element);
        
        const titleEl = this.tooltip.querySelector('#tour-title');
        const contentEl = this.tooltip.querySelector('#tour-content');
        const progressEl = this.tooltip.querySelector('#tour-progress');
        const nextBtn = this.tooltip.querySelector('#tour-next');
        const prevBtn = this.tooltip.querySelector('#tour-prev');

        if (titleEl) titleEl.innerText = step.title;
        if (contentEl) contentEl.innerText = step.content;
        if (progressEl) progressEl.innerText = `${this.currentStep + 1} / ${this.steps.length}`;
        
        if (el) {
            el.scrollIntoView({ behavior: 'smooth', block: 'center' });
            
            // Positioning update (small delay to wait for scroll)
            setTimeout(() => {
                const rect = el.getBoundingClientRect();
                this.tooltip.style.transform = 'none';
                
                let top = rect.bottom + 15;
                if (top + 150 > window.innerHeight) { // Tooltip would go off-bottom
                    top = rect.top - 180;
                }
                
                this.tooltip.style.top = `${Math.max(20, top)}px`;
                this.tooltip.style.left = `${Math.max(20, Math.min(window.innerWidth - 320, rect.left))}px`;
                
                document.querySelectorAll('.tour-highlight').forEach(e => e.classList.remove('tour-highlight'));
                el.classList.add('tour-highlight');
                
                // Ensure highlight style exists
                if (!document.getElementById('tour-styles')) {
                    const style = document.createElement('style');
                    style.id = 'tour-styles';
                    style.innerHTML = `
                        .tour-highlight { position: relative; z-index: 10001 !important; box-shadow: 0 0 0 5px rgba(0, 229, 255, 0.4), 0 0 40px rgba(0, 229, 255, 0.2) !important; transition: all 0.3s; pointer-events: none; }
                    `;
                    document.head.appendChild(style);
                }
            }, 350);
        } else {
            console.warn(`TourGuide: Element "${step.element}" not found.`);
            // Fallback: center the tooltip
            this.tooltip.style.top = '50%';
            this.tooltip.style.left = '50%';
            this.tooltip.style.transform = 'translate(-50%, -50%)';
        }
        
        if (nextBtn) nextBtn.innerText = this.currentStep === this.steps.length - 1 ? 'FINISH' : 'NEXT';
        if (prevBtn) prevBtn.style.visibility = this.currentStep === 0 ? 'hidden' : 'visible';
    }

    next() {
        if (this.currentStep < this.steps.length - 1) {
            this.currentStep++;
            this.showStep();
        } else {
            this.finish();
        }
    }

    prev() {
        if (this.currentStep > 0) {
            this.currentStep--;
            this.showStep();
        }
    }

    finish() {
        this.overlay.style.display = 'none';
        this.tooltip.style.display = 'none';
        document.querySelectorAll('.tour-highlight').forEach(e => e.classList.remove('tour-highlight'));
    }
}
