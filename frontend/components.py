import streamlit as st


def get_confidence_color(confidence: float) -> str:
    if confidence >= 90:
        return "#22c55e"
    elif confidence >= 70:
        return "#fbbf24"
    else:
        return "#ef4444"

def landing_hero() -> None:
    st.html(
        """
        <div class="saas-hero-wrapper">

            <div class="saas-hero-grid">
                <!-- Left Column: Content & CTAs -->
                <div class="hero-left">
                    <div class="hero-logo"><i class="fa-solid fa-leaf"></i> Plantexa AI</div>
                    <h1 class="hero-title-main">AI-Powered Plant Disease Detection</h1>
                    <p class="hero-subtitle-main">Upload a leaf image and receive instant disease diagnosis, confidence analysis, treatment recommendations, and prevention strategies.</p>

                    <div class="hero-cta-group">
                        <a href="#diagnosis-section" class="hero-btn-primary" style="text-decoration: none;"><i class="fa-solid fa-rocket"></i> Start Diagnosis</a>
                        <button class="hero-btn-secondary"><i class="fa-solid fa-play"></i> View Demo</button>
                    </div>

                    <div class="hero-trust">
                        <span><i class="fa-solid fa-check"></i> 98% Model Accuracy</span>
                        <span><i class="fa-solid fa-check"></i> &lt;2s Detection</span>
                        <span><i class="fa-solid fa-check"></i> 38+ Diseases</span>
                        <span><i class="fa-solid fa-check"></i> 15+ Plants</span>
                    </div>
                </div>

                <!-- Right Column: Animated AI Preview -->
                <div class="hero-right">
                    <div class="mock-dashboard">
                        <div class="mock-header">
                            <span class="dot red"></span><span class="dot yellow"></span><span class="dot green"></span>
                            <span class="mock-title">AI Processing Pipeline</span>
                        </div>
                        <div class="mock-body">
                            <div class="scanner-box">
                                <i class="fa-solid fa-leaf scanner-target"></i>
                                <div class="laser"></div>
                            </div>
                            <div class="floating-card fc-1">
                                <div class="fc-title">Disease Detected</div>
                                <div class="fc-val text-green">Apple Scab</div>
                            </div>
                            <div class="floating-card fc-2">
                                <div class="fc-title">Confidence</div>
                                <div class="fc-val text-green">98.4%</div>
                            </div>
                            <div class="floating-card fc-3">
                                <div class="fc-title">Severity Status</div>
                                <div class="fc-badge">Moderate</div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        """,
    )


def page_header(title: str, subtitle: str, icon: str = "fa-leaf") -> None:
    st.html(
        f"""
        <div class="glass-card" style="padding: 40px 24px; text-align: center; margin-bottom: 32px; margin-top: 16px; border-top: 3px solid var(--leaf-primary);">
            <div style="display: inline-flex; align-items: center; justify-content: center; width: 64px; height: 64px; border-radius: 50%; background: rgba(34, 197, 94, 0.1); color: var(--leaf-primary); font-size: 28px; margin-bottom: 16px;">
                <i class="fa-solid {icon}"></i>
            </div>
            <h1 style="margin: 0 0 12px 0; font-family: 'Poppins', sans-serif; font-size: 42px !important; color: var(--leaf-text);">{title}</h1>
            <p style="margin: 0; color: var(--leaf-muted); font-size: 18px; max-width: 600px; margin-left: auto; margin-right: auto;">{subtitle}</p>
        </div>
        """
    )


def section_title(title: str, icon: str, anchor_id: str = "") -> None:
    id_attr = f' id="{anchor_id}"' if anchor_id else ""
    st.html(
        f'<h3 class="section-title"{id_attr}><i class="fa-solid {icon}"></i> {title}</h3>',
    )


def empty_placeholder(icon: str, title: str, description: str = "") -> None:
    st.html(
        f"""
        <div class="empty-placeholder">
            <i class="fa-solid {icon}"></i>
            <h4>{title}</h4>
            <p>{description}</p>
        </div>
        """
    )


def prediction_card(disease, confidence):
    confidence = float(confidence)
    badge_color = get_confidence_color(confidence)

    if confidence >= 90:
        badge_text = "High Confidence"
    elif confidence >= 70:
        badge_text = "Moderate Confidence"
    else:
        badge_text = "Low Confidence"

    st.html(f"""
    <div class="glass-card" style="padding: 24px; margin-bottom: 16px;">
        <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 16px;">
            <div>
                <h3 style="margin: 0; font-size: 22px; color: var(--leaf-text);">{disease}</h3>
                <p style="margin: 4px 0 0 0; color: var(--leaf-muted); font-size: 14px;">Primary AI Diagnosis</p>
            </div>
            <span style="background: {badge_color}22; color: {badge_color}; padding: 6px 12px; border-radius: 99px; font-size: 12px; font-weight: 600; border: 1px solid {badge_color}44;">{badge_text}</span>
        </div>
        <div style="display: flex; align-items: baseline; gap: 8px; margin-bottom: 12px;">
            <h2 class="count-up" data-target="{confidence}" style="margin: 0; font-size: 48px; font-weight: 800; color: {badge_color}; line-height: 1;">{confidence:.1f}%</h2>
            <span style="color: var(--leaf-muted); font-size: 14px;">Confidence Score</span>
        </div>
        <div style="width: 100%; background: rgba(255,255,255,0.05); height: 8px; border-radius: 4px; overflow: hidden; margin-top: 16px;">
            <div style="width: {confidence}%; height: 100%; background: {badge_color}; border-radius: 4px; transform-origin: left; animation: growBar 1s cubic-bezier(0.25, 0.8, 0.25, 1) forwards;"></div>
        </div>
    </div>
    """)


def top_predictions_card(predictions):
    html_content = '<div class="glass-card" style="padding: 16px; height: 100%; display: flex; flex-direction: column; justify-content: center;">'
    for i, (disease, score) in enumerate(predictions):
        score_val = float(score)
        color = get_confidence_color(score_val)
        html_content += f"""
        <div class="pop-in-card" style="padding: 12px 8px; border-bottom: 1px solid rgba(255,255,255,0.05); animation-delay: {i * 0.15}s;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                <span style="color: var(--leaf-text); font-weight: 500;">{disease}</span>
                <span class="count-up" data-target="{score_val}" style="color: {color}; font-family: 'Poppins', sans-serif; font-weight: 600;">{score_val:.1f}%</span>
            </div>
            <div style="width: 100%; background: rgba(255,255,255,0.05); height: 6px; border-radius: 3px; overflow: hidden;">
                <div style="width: {score_val}%; height: 100%; background: {color}; border-radius: 3px; transform-origin: left; transform: scaleX(0); animation: growBar 1s cubic-bezier(0.25, 0.8, 0.25, 1) forwards; animation-delay: {i * 0.15}s;"></div>
            </div>
        </div>
        """
    html_content += '</div>'
    st.html(html_content)
