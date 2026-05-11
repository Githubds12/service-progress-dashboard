class TourGuide {
    constructor(steps) {
        this.steps = steps;
        this.currentStep = 0;
        this.overlay = null;
        this.tooltip = null;
        this.init();
    }

    init() {
        // Create overlay
        this.overlay = document.createElement('div');
        this.overlay.className = 'tour-overlay';
        Object.assign(this.overlay.style, {
            position: 'fixed', top: 0, left: 0, width: '100%', height: '100%',
            background: 'rgba(0,0,0,0.7)', zIndex: 9998, display: 'none',
            transition: 'opacity 0.3s'
        });
        document.body.appendChild(this.overlay);

        // Create tooltip
        this.tooltip = document.createElement('div');
        this.tooltip.className = 'tour-tooltip';
        Object.assign(this.tooltip.style, {
            position: 'fixed', zIndex: 9999, display: 'none',
            background: '#0c0c0c', border: '1px solid #00e5ff',
            borderRadius: '12px', padding: '20px', width: '300px',
            boxShadow: '0 0 20px rgba(0, 229, 255, 0.2)',
            color: '#fff', fontFamily: 'Outfit, sans-serif'
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
        document.body.appendChild(this.tooltip);

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
        if (!this.steps || this.steps.length === 0) {
            console.error('TourGuide: No steps defined');
            this.finish();
            return;
        }
        const step = this.steps[this.currentStep];
        const el = document.querySelector(step.element);
        
        document.getElementById('tour-title').innerText = step.title;
        document.getElementById('tour-content').innerText = step.content;
        document.getElementById('tour-progress').innerText = `${this.currentStep + 1} / ${this.steps.length}`;
        
        if (el) {
            el.scrollIntoView({ behavior: 'smooth', block: 'center' });
            const rect = el.getBoundingClientRect();
            
            // Position tooltip
            this.tooltip.style.top = `${rect.bottom + 15}px`;
            this.tooltip.style.left = `${Math.max(20, rect.left)}px`;
            
            // Highlight element (simple implementation)
            document.querySelectorAll('.tour-highlight').forEach(e => e.classList.remove('tour-highlight'));
            el.classList.add('tour-highlight');
            
            // Add pulse effect if not present
            if (!document.getElementById('tour-styles')) {
                const style = document.createElement('style');
                style.id = 'tour-styles';
                style.innerHTML = `
                    .tour-highlight { position: relative; z-index: 9999 !important; box-shadow: 0 0 0 5px rgba(0, 229, 255, 0.4), 0 0 40px rgba(0, 229, 255, 0.2) !important; transition: all 0.3s; pointer-events: none; }
                `;
                document.head.appendChild(style);
            }
        }
        
        document.getElementById('tour-next').innerText = this.currentStep === this.steps.length - 1 ? 'FINISH' : 'NEXT';
        document.getElementById('tour-prev').style.visibility = this.currentStep === 0 ? 'hidden' : 'visible';
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
