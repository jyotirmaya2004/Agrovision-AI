import os
import streamlit as st


def load_css():
    base_dir = os.path.dirname(__file__)

    # Support loading style.css from frontend/ or styles/
    css_path = os.path.join(base_dir, "style.css")
    if not os.path.exists(css_path):
        css_path = os.path.join(os.path.dirname(base_dir), "styles", "style.css")

    if os.path.exists(css_path):
        with open(css_path, "r", encoding="utf-8") as f:
            css_content = f.read()
        st.html(f"<style>\n{css_content}\n</style>")

    # Dynamically load mobile.css if it exists
    mobile_css_path = os.path.join(base_dir, "mobile.css")
    if not os.path.exists(mobile_css_path):
        # Backward-compatible fallback (older layouts)
        mobile_css_path = os.path.join(os.path.dirname(base_dir), "styles", "mobile.css")

    if os.path.exists(mobile_css_path):
        with open(mobile_css_path, "r", encoding="utf-8") as f:
            mobile_css_content = f.read()
        st.html(f"<style>\n{mobile_css_content}\n</style>")

    st.html(
        """
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.2/css/all.min.css">
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Poppins:wght@500;600;700;800&display=swap" rel="stylesheet">

        <!-- 5-Layer Premium Animated Background -->
        <div class="global-bg-container">
            <!-- Layer 1: Moving Gradient Mesh (handled by .stApp base) -->

            <!-- Layer 2: Floating Green Glow Orbs -->
            <div class="bg-layer orbs">
                <div class="orb orb-1"></div>
                <div class="orb orb-2"></div>
                <div class="orb orb-3"></div>
            </div>

            <!-- Layer 3: AI Neural Network -->
            <div class="bg-layer neural"></div>

            <!-- Layer 4: Agriculture Theme (Floating Leaves) -->
            <div class="bg-layer nature">
                <i class="fa-solid fa-leaf float-leaf l1"></i>
                <i class="fa-solid fa-leaf float-leaf l2"></i>
                <i class="fa-solid fa-leaf float-leaf l3"></i>
                <i class="fa-solid fa-leaf float-leaf l4"></i>
                <i class="fa-solid fa-seedling float-leaf l5"></i>
            </div>

            <!-- Layer 5: Glass Overlay -->
            <div class="bg-layer overlay"></div>
        </div>

        <!-- Animated Back to Top Button -->
        <button id="backToTopBtn" class="back-to-top-btn" aria-label="Scroll back to top">
            <i class="fa-solid fa-arrow-up"></i>
        </button>


        <script>
        const initCounters = () => {
            document.querySelectorAll('.count-up').forEach(el => {
                if(el.dataset.animated) return;
                el.dataset.animated = 'true';
                let target = parseFloat(el.dataset.target);
                let duration = 1000;
                let start = performance.now();
                let update = (t) => {
                    let p = Math.min((t - start) / duration, 1);
                    let ease = 1 - Math.pow(1 - p, 4); // Quartic ease out
                    el.innerText = (ease * target).toFixed(1) + '%';
                    if(p < 1) requestAnimationFrame(update);
                    else el.innerText = target.toFixed(1) + '%';
                };
                requestAnimationFrame(update);
            });
        };

        const initChatDrag = () => {
            const marker = document.querySelector('.chat-floating-panel-marker');
            if (marker) {
                const panel = marker.closest('div[data-testid="stVerticalBlock"]');
                if (panel && !panel.dataset.dragAttached) {
                    panel.dataset.dragAttached = 'true';
                    let isDragging = false;
                    let offsetX, offsetY;

                    panel.addEventListener('mousedown', (e) => {
                        const tag = e.target.tagName.toLowerCase();
                        if (['input', 'button', 'textarea'].includes(tag) || e.target.closest('button')) return;

                        // Prevent drag if clicking the resize handle (bottom-right area)
                        const rect = panel.getBoundingClientRect();
                        if (e.clientX > rect.right - 20 && e.clientY > rect.bottom - 20) return;

                        if (e.detail === 2) {
                            isDragging = true;
                            offsetX = e.clientX - rect.left;
                            offsetY = e.clientY - rect.top;
                            panel.style.cursor = 'grabbing';
                            panel.style.animation = 'none';
                            panel.style.transition = 'none';

                            // Prevent text selection while dragging
                            document.body.style.userSelect = 'none';
                            window.getSelection().removeAllRanges();
                            e.preventDefault();
                        }
                    });

                    document.addEventListener('mousemove', (e) => {
                        if (!isDragging) return;
                        e.preventDefault();
                        panel.style.left = (e.clientX - offsetX) + 'px';
                        panel.style.top = (e.clientY - offsetY) + 'px';
                        panel.style.bottom = 'auto';
                        panel.style.right = 'auto';
                    });

                    document.addEventListener('mouseup', () => {
                        if (isDragging) {
                            isDragging = false;
                            panel.style.cursor = 'auto';
                            // Restore text selection
                            document.body.style.userSelect = '';
                        }
                    });
                }
            }
        };

        const initBackToTop = () => {
            const btn = document.getElementById('backToTopBtn');
            if (!btn || btn.dataset.initialized) return;
            btn.dataset.initialized = 'true';

            const scrollContainer = document.querySelector('[data-testid="stAppViewContainer"]') || window;
            const scrollElement = scrollContainer === window ? document.documentElement : scrollContainer;

            const toggleBtn = () => {
                if (scrollElement.scrollTop > 400) {
                    btn.classList.add('visible');
                } else {
                    btn.classList.remove('visible');
                }
            };

            scrollContainer.addEventListener('scroll', toggleBtn, { passive: true });
            toggleBtn(); // Check initial state on load

            btn.addEventListener('click', () => {
                scrollContainer.scrollTo({ top: 0, behavior: 'smooth' });
            });
        };

        const runObservers = () => {
            initCounters();
            initChatDrag();
            initBackToTop();
        };

        // Initial run
        setTimeout(runObservers, 100);
        if (!window.customUiObserver) {
            if (window.counterObserver) { window.counterObserver.disconnect(); }
            window.customUiObserver = new MutationObserver(runObservers);
            window.customUiObserver.observe(document.body, { childList: true, subtree: true });
        }
        </script>
        """
    )

