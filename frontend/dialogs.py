import os
import re
import time

import pandas as pd
import streamlit as st

from frontend.components import empty_placeholder, get_confidence_color
from backend.disease_info import _t


@st.dialog(_t("Plantexa AI Secure Login"))
def render_auth_dialog():
    if st.session_state.get("logout_reason"):
        st.warning(_t(st.session_state.logout_reason))
        st.session_state.logout_reason = ""

    tab_login, tab_signup = st.tabs([_t("Login"), _t("Create Account")])

    with tab_login:
        st.html(f'<h4 style="margin-top: 0; margin-bottom: 16px; color: var(--leaf-text); font-family: \'Poppins\', sans-serif;"><i class="fa-solid fa-right-to-bracket" style="color: var(--leaf-primary); margin-right: 8px;"></i> {_t("Welcome Back")}</h4>')
        st.html(f'<div style="color: var(--leaf-muted); font-size: 14px; font-weight: 600; margin-bottom: 6px;"><i class="fa-solid fa-user" style="color: var(--leaf-primary); margin-right: 8px;"></i>{_t("Username")}</div>')
        username = st.text_input(_t("Username"), placeholder=_t("e.g. JohnDoe"), label_visibility="collapsed", key="log_user")
        st.html(f'<div style="color: var(--leaf-muted); font-size: 14px; font-weight: 600; margin-bottom: 6px; margin-top: 16px;"><i class="fa-solid fa-lock" style="color: var(--leaf-primary); margin-right: 8px;"></i>{_t("Password")}</div>')
        password = st.text_input(_t("Password"), placeholder=_t("Enter your secret password"), type="password", label_visibility="collapsed", key="log_pass")
        st.html('<br>')
        st.markdown('<div class="login-btn-marker"></div>', unsafe_allow_html=True)
        if st.button(_t("Login"), type="primary", use_container_width=True):
            if username.strip() and password.strip():
                try:
                    from backend.db import authenticate_user, check_user_exists
                    user_data = authenticate_user(username, password)
                    if user_data:
                        st.session_state.username = username.strip()
                        st.session_state.user_id = user_data.get("id")
                        st.session_state.avatar = user_data.get("avatar") or "🧑‍🌾"
                        st.session_state.set_cookie = username.strip()
                        st.session_state.sync_session = True
                        st.session_state.last_activity = time.time()
                        st.session_state.show_auth = False
                        st.rerun()
                    else:
                        if check_user_exists(username):
                            st.error(_t("Incorrect password."))
                        else:
                            st.error(_t("Username not found. Please create an account."))
                except Exception as e:
                    st.error(f"{_t('Login failed:')} {e}")
            else:
                st.error(_t("Please enter both username and password."))

    with tab_signup:
        st.html(f'<h4 style="margin-top: 0; margin-bottom: 16px; color: var(--leaf-text); font-family: \'Poppins\', sans-serif;"><i class="fa-solid fa-user-plus" style="color: var(--leaf-primary); margin-right: 8px;"></i> {_t("New Account")}</h4>')
        st.html(f'<div style="color: var(--leaf-muted); font-size: 14px; font-weight: 600; margin-bottom: 6px;"><i class="fa-solid fa-face-smile" style="color: var(--leaf-primary); margin-right: 8px;"></i>{_t("Choose Avatar")}</div>')
        selected_avatar = st.selectbox(_t("Avatar"), [_t("🧑‍🌾 Farmer"), _t("👩‍🌾 Gardener"), _t("👨‍🌾 Agronomist"), _t("🪴 Plant Lover"), _t("🌻 Sunflower"), _t("🌵 Cactus"), _t("🌾 Botanist"), _t("🤖 AI Bot")], key="reg_avatar", label_visibility="collapsed")
        avatar_emoji = selected_avatar.split(" ")[0]

        st.html(f'<div style="color: var(--leaf-muted); font-size: 14px; font-weight: 600; margin-bottom: 6px; margin-top: 16px;"><i class="fa-solid fa-user-tag" style="color: var(--leaf-primary); margin-right: 8px;"></i>{_t("Choose a Username")}</div>')
        new_username = st.text_input(_t("Choose a Username"), placeholder=_t("e.g. JaneFarmer"), label_visibility="collapsed", key="reg_user")
        st.html(f'<div style="color: var(--leaf-muted); font-size: 14px; font-weight: 600; margin-bottom: 6px; margin-top: 16px;"><i class="fa-solid fa-shield-halved" style="color: var(--leaf-primary); margin-right: 8px;"></i>{_t("Choose a Password")}</div>')
        new_password = st.text_input(_t("Choose a Password"), placeholder=_t("Create a strong password"), type="password", label_visibility="collapsed", key="reg_pass")

        strength_score = 0
        if new_password:
            if len(new_password) >= 8: strength_score += 1
            if re.search(r"[a-z]", new_password): strength_score += 1
            if re.search(r"[A-Z]", new_password): strength_score += 1
            if re.search(r"[0-9]", new_password): strength_score += 1
            if re.search(r"[^a-zA-Z0-9]", new_password): strength_score += 1

        strength_colors = ["#475569", "#ef4444", "#f97316", "#eab308", "#84cc16", "#22c55e"]
        strength_labels = ["", _t("Very Weak"), _t("Weak"), _t("Fair"), _t("Good"), _t("Strong")]
        pct = (strength_score / 5) * 100 if new_password else 0
        color = strength_colors[strength_score] if new_password else strength_colors[0]
        label = strength_labels[strength_score] if new_password else _t("Waiting for input...")

        st.html(f"""
        <div style="margin-top: 10px; margin-bottom: 4px;">
            <div style="display: flex; justify-content: space-between; font-size: 13px; color: var(--leaf-muted); margin-bottom: 6px;">
                <span>{_t("Password Strength")}</span>
                <span style="color: {color}; font-weight: 600;">{label}</span>
            </div>
            <div style="height: 6px; width: 100%; background: rgba(255,255,255,0.05); border-radius: 3px; overflow: hidden; border: 1px solid rgba(255,255,255,0.05);">
                <div style="height: 100%; width: {pct}%; background: {color}; transition: width 0.3s ease, background-color 0.3s ease; border-radius: 3px;"></div>
            </div>
        </div>
        """)

        st.html(f'<div style="color: var(--leaf-muted); font-size: 14px; font-weight: 600; margin-bottom: 6px; margin-top: 16px;"><i class="fa-solid fa-key" style="color: var(--leaf-primary); margin-right: 8px;"></i>{_t("Confirm Password")}</div>')
        confirm_password = st.text_input(_t("Confirm Password"), placeholder=_t("Re-enter to verify"), type="password", label_visibility="collapsed", key="reg_confirm")
        st.html('<br>')

        passwords_match = False
        if new_password or confirm_password:
            if new_password == confirm_password:
                st.html(f'<div style="color: #22c55e; font-size: 14px; margin-bottom: 12px; font-weight: 600;"><i class="fa-solid fa-circle-check"></i> {_t("Passwords match")}</div>')
                passwords_match = True
            else:
                st.html(f'<div style="color: #ef4444; font-size: 14px; margin-bottom: 12px; font-weight: 600;"><i class="fa-solid fa-circle-xmark"></i> {_t("Passwords do not match")}</div>')

        btn_disabled = not (new_username.strip() and new_password.strip() and passwords_match)

        st.markdown('<div class="signup-btn-marker"></div>', unsafe_allow_html=True)
        if st.button(_t("Create Account"), type="primary", use_container_width=True, disabled=btn_disabled):
            try:
                from backend.db import check_user_exists, create_user
                if check_user_exists(new_username):
                    st.error(_t("Username already exists. Please log in or choose another."))
                else:
                    insert_res = create_user(new_username, new_password, avatar_emoji)
                    if insert_res.data:
                        st.session_state.username = new_username.strip()
                        st.session_state.user_id = insert_res.data[0].get("id")
                        st.session_state.avatar = avatar_emoji
                        st.session_state.set_cookie = new_username.strip()
                        st.session_state.sync_session = True
                        st.session_state.last_activity = time.time()
                        st.session_state.show_auth = False
                        st.session_state.new_account = True
                        st.rerun()
                    else:
                        st.error(_t("Failed to create new user account."))
            except Exception as e:
                st.error(f"{_t('Registration failed:')} {e}")


@st.dialog(_t("Prediction History"), width="large")
def render_history_dialog():
    from frontend.sections import _generate_history_pdf, clear_history, load_history

    history = load_history()
    if not history:
        empty_placeholder("fa-folder-open", _t("No History Found"), _t("Analyze a leaf from the Home page first to see records here."))
    else:
        df = pd.DataFrame(history)

        def color_confidence(val):
            try:
                return f'color: {get_confidence_color(float(val))}'
            except Exception:
                return ''

        styled_df = df.style.map(color_confidence, subset=['Confidence'])

        st.dataframe(
            styled_df,
            use_container_width=True,
            column_config={
                "Image_URL": st.column_config.ImageColumn(_t("Uploaded Image")),
                "Confidence": st.column_config.NumberColumn(_t("Confidence"), format="%.2f%%")
            }
        )

        col1, col2, col3 = st.columns(3)
        pdf_bytes = _generate_history_pdf(history)
        if pdf_bytes:
            with col1:
                st.download_button(
                    label=_t("Download History PDF"),
                    data=pdf_bytes,
                    file_name="plantexa_ai_history.pdf",
                    mime="application/pdf",
                    use_container_width=True,
                )
        with col2:
            st.download_button(
                _t("Download CSV"),
                df.to_csv(index=False),
                file_name="prediction_history.csv",
                mime="text/csv",
                use_container_width=True,
            )
        with col3:
            if st.button(_t("Clear History"), use_container_width=True):
                clear_history()
                st.session_state.prediction_history = []
                st.rerun()


@st.dialog(_t("Dataset Information"), width="large")
def render_dataset_dialog():
    st.html(f"""
    <div class="glass-card" style="padding: 24px; height: 100%;">
        <h3 style="margin-top: 0; color: var(--leaf-primary); font-family: 'Poppins', sans-serif;"><i class="fa-solid fa-chart-pie"></i> {_t('Dataset Summary')}</h3>
        <ul style="color: var(--leaf-muted); font-size: 16px; padding-left: 20px; line-height: 1.8; margin: 0;">
            <li><strong>{_t('Total classes')}:</strong> 38+</li>
            <li><strong>{_t('Image format')}:</strong> 224 x 224 (RGB)</li>
            <li><strong>{_t('Primary purpose')}:</strong> {_t('Plant disease identification from leaf images')}</li>
            <li><strong>{_t('Source')}:</strong> {_t('PlantVillage & Augmented variations')}</li>
        </ul>
    </div>
    <br>
    <div class="glass-card" style="padding: 24px; height: 100%;">
        <h3 style="margin-top: 0; color: var(--leaf-primary); font-family: 'Poppins', sans-serif;"><i class="fa-solid fa-seedling"></i> {_t('Supported Crops')}</h3>
        <ul style="color: var(--leaf-muted); font-size: 16px; padding-left: 20px; line-height: 1.6; margin: 0; display: grid; grid-template-columns: 1fr 1fr; gap: 8px;">
            <li><i class="fa-solid fa-apple-whole" style="color: #ef4444; width: 20px;"></i> {_t('Apple')}</li>
            <li><i class="fa-solid fa-seedling" style="color: #eab308; width: 20px;"></i> {_t('Corn')}</li>
            <li><i class="fa-solid fa-leaf" style="color: #a855f7; width: 20px;"></i> {_t('Grape')}</li>
            <li><i class="fa-solid fa-lemon" style="color: #fb923c; width: 20px;"></i> {_t('Peach')}</li>
            <li><i class="fa-solid fa-pepper-hot" style="color: #ef4444; width: 20px;"></i> {_t('Pepper')}</li>
            <li><i class="fa-solid fa-carrot" style="color: #d97706; width: 20px;"></i> {_t('Potato')}</li>
            <li><i class="fa-solid fa-leaf" style="color: #f43f5e; width: 20px;"></i> {_t('Strawberry')}</li>
            <li><i class="fa-solid fa-apple-whole" style="color: #ef4444; width: 20px;"></i> {_t('Tomato')}</li>
        </ul>
    </div>
    <br>
    <div class="glass-card" style="padding: 24px; margin-bottom: 8px;">
        <h3 style="margin-top: 0; color: var(--leaf-primary); font-family: 'Poppins', sans-serif;"><i class="fa-solid fa-viruses"></i> {_t('Disease Categories')}</h3>
        <p style="color: var(--leaf-muted); font-size: 16px; line-height: 1.6; margin: 0;">
            {_t('The dataset includes healthy leaves and common disease categories such as bacterial spot, early blight, late blight, leaf mold, rust, powdery mildew, scab, and leaf scorch.')}
        </p>
    </div>
    """)


@st.dialog(_t("About Plantexa AI"), width="large")
def render_about_dialog():
    st.html(f"""
    <div class="glass-card" style="padding: 24px; margin-bottom: 24px;">
        <p style="color: var(--leaf-muted); font-size: 16px; margin: 0;">
            {_t('Plantexa AI uses a two-stage deep learning workflow. It first checks whether the uploaded image looks like a plant leaf, then predicts the most likely disease and shows symptoms, causes, treatment, and prevention guidance from the disease knowledge base.')}
        </p>
    </div>
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 16px; margin-bottom: 24px;">
        <div class="glass-card" style="padding: 24px;">
            <h4 style="margin-top: 0; color: var(--leaf-primary); font-family: 'Poppins', sans-serif;"><i class="fa-solid fa-desktop"></i> {_t('Frontend')}</h4>
            <ul style="color: var(--leaf-muted); font-size: 14px; padding-left: 20px;">
                <li>{_t('Streamlit')}</li>
                <li>{_t('HTML components')}</li>
                <li>{_t('Modern Glassmorphism CSS')}</li>
            </ul>
        </div>
        <div class="glass-card" style="padding: 24px;">
            <h4 style="margin-top: 0; color: var(--leaf-primary); font-family: 'Poppins', sans-serif;"><i class="fa-solid fa-server"></i> {_t('Backend')}</h4>
            <ul style="color: var(--leaf-muted); font-size: 14px; padding-left: 20px;">
                <li>{_t('Python')}</li>
                <li>{_t('TensorFlow')}</li>
                <li>{_t('NumPy & Pandas')}</li>
            </ul>
        </div>
        <div class="glass-card" style="padding: 24px;">
            <h4 style="margin-top: 0; color: var(--leaf-primary); font-family: 'Poppins', sans-serif;"><i class="fa-solid fa-brain"></i> {_t('Models')}</h4>
            <ul style="color: var(--leaf-muted); font-size: 14px; padding-left: 20px;">
                <li>{_t('MobileNetV2 classifier')}</li>
                <li>{_t('Leaf validation network')}</li>
                <li>{_t('224 x 224 resolution')}</li>
            </ul>
        </div>
    </div>
    <div class="glass-card" style="padding: 24px; margin-bottom: 24px;">
        <h4 style="margin-top: 0; color: var(--leaf-text); font-family: 'Poppins', sans-serif;"><i class="fa-solid fa-list-check" style="color: var(--leaf-primary);"></i> {_t('Project Features')}</h4>
        <ul style="color: var(--leaf-muted); font-size: 15px; margin: 0; padding-left: 20px; line-height: 1.8;">
            <li><strong>{_t('Two-Stage Pipeline')}:</strong> {_t('Leaf detection before disease classification')}</li>
            <li><strong>{_t('AI Analysis')}:</strong> {_t('Top 3 predictions with real-time confidence scores')}</li>
            <li><strong>{_t('Knowledge Base')}:</strong> {_t('Detailed disease symptoms, causes, treatment, and prevention')}</li>
            <li><strong>{_t('NVIDIA LLM')}:</strong> {_t('Context-aware AI agriculture assistant')}</li>
            <li><strong>{_t('Reporting')}:</strong> {_t('Downloadable PDF report cards and session prediction history')}</li>
        </ul>
    </div>
    <div class="glass-card" style="padding: 24px; margin-bottom: 8px;">
        <h4 style="margin-top: 0; color: var(--leaf-text); font-family: 'Poppins', sans-serif;"><i class="fa-solid fa-graduation-cap" style="color: var(--leaf-primary);"></i> {_t('Academic Details')}</h4>
        <p style="color: var(--leaf-muted); font-size: 15px; line-height: 1.8; margin-bottom: 8px;"><strong>{_t('Project Team Members')}:</strong><br>
        Jyotirmaya Behera (3146/24), Diptesh Ranjan Pradhan (3141/24), Bibekananda Sahoo (3136/24), Pritam Kumar Behera (3159/24), Laxman Kumar Sahoo (3148/24)</p>
        <p style="color: var(--leaf-muted); font-size: 15px; margin: 0;"><strong>{_t('Academic Year')}:</strong> 2025 - 2026</p>
    </div>
    """)


@st.dialog(_t("Admin - Database Viewer"), width="large")
def render_admin_dialog():
    ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin123")

    if not st.session_state.get("admin_authenticated", False):
        st.html(f"""
        <div class="glass-card" style="padding: 32px 24px; text-align: center; margin-bottom: 24px; border-top: 3px solid #ef4444;">
            <div style="display: inline-flex; align-items: center; justify-content: center; width: 64px; height: 64px; border-radius: 50%; background: rgba(239, 68, 68, 0.1); color: #ef4444; font-size: 28px; margin-bottom: 16px;">
                <i class="fa-solid fa-lock"></i>
            </div>
            <h2 style="margin: 0 0 12px 0; font-family: 'Poppins', sans-serif; color: var(--leaf-text);">{_t('Admin Access Restricted')}</h2>
            <p style="margin: 0; color: var(--leaf-muted); font-size: 16px;">{_t('Please enter the master admin password to access the database viewer.')}</p>
        </div>
        """)
        pwd = st.text_input(_t("Admin Password"), type="password", placeholder=_t("Enter admin password"), label_visibility="collapsed", key="dlg_admin_pass")
        if st.button(_t("Unlock Dashboard"), type="primary", use_container_width=True):
            if pwd == ADMIN_PASSWORD:
                st.session_state.admin_authenticated = True
                st.rerun()
            else:
                st.error(_t("Incorrect admin password."))
        return

    if st.button(_t("Lock Dashboard"), key="dlg_lock_dashboard"):
        st.session_state.admin_authenticated = False
        st.rerun()

    try:
        from backend.db import get_all_predictions, delete_prediction, delete_all_predictions
        response = get_all_predictions()
        df = pd.DataFrame(response.data)

        if not df.empty:
            df["username"] = df["app_users"].apply(lambda x: x.get("username") if isinstance(x, dict) else _t("Unknown"))
            df = df.drop(columns=["app_users"])
            cols = ["id", "username", "timestamp", "disease", "confidence", "image_url", "user_id"]
            df = df[[c for c in cols if c in df.columns]]
        else:
            df = pd.DataFrame(columns=["id", "username", "timestamp", "disease", "confidence", "image_url", "user_id"])

        st.write(f"### {_t('Total Records')}: {len(df)}")
        st.dataframe(
            df.style.map(lambda v: f'color: {get_confidence_color(float(v))}' if isinstance(v, (int, float)) else '', subset=['confidence']),
            use_container_width=True,
            column_config={
                "image_url": st.column_config.ImageColumn(_t("Uploaded Image")),
                "confidence": st.column_config.NumberColumn(_t("Confidence"), format="%.2f%%")
            }
        )

        if not df.empty:
            st.write(f"#### {_t('Manage Records')}")
            col_sel, col_btn_del, col_btn_all = st.columns([2, 1, 1])
            with col_sel:
                row_id = st.selectbox(_t("Select Record ID to delete"), df["id"].tolist(), label_visibility="collapsed")
            with col_btn_del:
                if st.button(_t("Delete Row"), use_container_width=True):
                    delete_prediction(row_id)
                    st.rerun()
            with col_btn_all:
                confirm_delete = st.checkbox(_t("Confirm wipe"))
                if st.button(_t("Delete ALL"), type="primary", use_container_width=True, disabled=not confirm_delete):
                    delete_all_predictions()
                    st.rerun()
    except Exception as e:
        st.error(f"{_t('Could not load database:')} {e}")


@st.dialog(_t("User Profile"), width="large")
def render_profile_dialog():
    from frontend.sections import load_history

    username = st.session_state.get("username", _t("Unknown User"))
    avatar = st.session_state.get("avatar", "🧑‍🌾")
    user_id = st.session_state.get("user_id", "N/A")
    history = load_history()

    st.html(f"""
    <div class="glass-card" style="padding: 32px 24px; text-align: center; margin-bottom: 24px; border-top: 3px solid var(--leaf-primary);">
        <div style="font-size: 72px; margin-bottom: 16px;">{avatar}</div>
        <h2 style="margin: 0 0 8px 0; font-family: 'Poppins', sans-serif; color: var(--leaf-text);">{username}</h2>
        <p style="margin: 0; color: var(--leaf-muted); font-size: 14px;"><strong>{_t('Account ID')}:</strong> {user_id}</p>
    </div>
    <div style="display: flex; gap: 16px; margin-bottom: 24px;">
        <div class="glass-card" style="flex: 1; padding: 16px; text-align: center;">
            <div style="font-size: 24px; font-weight: 800; color: var(--leaf-primary);">{len(history)}</div>
            <div style="font-size: 13px; color: var(--leaf-muted); text-transform: uppercase;">{_t('Total Scans')}</div>
        </div>
    </div>
    """)

    if st.button(_t("Logout"), type="primary", use_container_width=True):
        st.session_state.clear()
        st.session_state.clear_cookie = True
        st.rerun()