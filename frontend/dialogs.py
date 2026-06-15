import hashlib
import os
import re
import time

import pandas as pd
import streamlit as st

from frontend.components import empty_placeholder, get_confidence_color


@st.dialog("Plantexa AI Secure Login")
def render_auth_dialog():
    if st.session_state.get("logout_reason"):
        st.warning(st.session_state.logout_reason)
        st.session_state.logout_reason = ""

    tab_login, tab_signup = st.tabs(["Login", "Create Account"])

    with tab_login:
        st.html('<h4 style="margin-top: 0; margin-bottom: 16px; color: var(--leaf-text); font-family: \'Poppins\', sans-serif;"><i class="fa-solid fa-right-to-bracket" style="color: var(--leaf-primary); margin-right: 8px;"></i> Welcome Back</h4>')
        st.html('<div style="color: var(--leaf-muted); font-size: 14px; font-weight: 600; margin-bottom: 6px;"><i class="fa-solid fa-user" style="color: var(--leaf-primary); margin-right: 8px;"></i>Username</div>')
        username = st.text_input("Username", placeholder="e.g. JohnDoe", label_visibility="collapsed", key="log_user")
        st.html('<div style="color: var(--leaf-muted); font-size: 14px; font-weight: 600; margin-bottom: 6px; margin-top: 16px;"><i class="fa-solid fa-lock" style="color: var(--leaf-primary); margin-right: 8px;"></i>Password</div>')
        password = st.text_input("Password", placeholder="Enter your secret password", type="password", label_visibility="collapsed", key="log_pass")
        st.html('<br>')
        st.markdown('<div class="login-btn-marker"></div>', unsafe_allow_html=True)
        if st.button("Login", type="primary", use_container_width=True):
            if username.strip() and password.strip():
                try:
                    from supabase import create_client
                    supabase_url = os.getenv("SUPABASE_URL", "https://dloxbfflvfcciczfibxh.supabase.co")
                    supabase_key = os.getenv("SUPABASE_KEY")
                    if supabase_key:
                        supabase = create_client(supabase_url, supabase_key)
                        hashed_pw = hashlib.sha256(password.strip().encode('utf-8')).hexdigest()
                        response = supabase.table("app_users").select("id, password, avatar").eq("username", username.strip()).limit(1).execute()
                        if response.data:
                            if response.data[0].get("password") == hashed_pw:
                                st.session_state.username = username.strip()
                                st.session_state.user_id = response.data[0].get("id")
                                st.session_state.avatar = response.data[0].get("avatar") or "🧑‍🌾"
                                st.session_state.set_cookie = username.strip()
                                st.session_state.sync_session = True
                                st.session_state.last_activity = time.time()
                                st.session_state.show_auth = False
                                st.rerun()
                            else:
                                st.error("Incorrect password.")
                        else:
                            st.error("Username not found. Please create an account.")
                except Exception as e:
                    st.error(f"Login failed: {e}")
            else:
                st.error("Please enter both username and password.")

    with tab_signup:
        st.html('<h4 style="margin-top: 0; margin-bottom: 16px; color: var(--leaf-text); font-family: \'Poppins\', sans-serif;"><i class="fa-solid fa-user-plus" style="color: var(--leaf-primary); margin-right: 8px;"></i> New Account</h4>')
        st.html('<div style="color: var(--leaf-muted); font-size: 14px; font-weight: 600; margin-bottom: 6px;"><i class="fa-solid fa-face-smile" style="color: var(--leaf-primary); margin-right: 8px;"></i>Choose Avatar</div>')
        selected_avatar = st.selectbox("Avatar", ["🧑‍🌾 Farmer", "👩‍🌾 Gardener", "👨‍🌾 Agronomist", "🪴 Plant Lover", "🌻 Sunflower", "🌵 Cactus", "🌾 Botanist", "🤖 AI Bot"], key="reg_avatar", label_visibility="collapsed")
        avatar_emoji = selected_avatar.split(" ")[0]

        st.html('<div style="color: var(--leaf-muted); font-size: 14px; font-weight: 600; margin-bottom: 6px; margin-top: 16px;"><i class="fa-solid fa-user-tag" style="color: var(--leaf-primary); margin-right: 8px;"></i>Choose a Username</div>')
        new_username = st.text_input("Choose a Username", placeholder="e.g. JaneFarmer", label_visibility="collapsed", key="reg_user")
        st.html('<div style="color: var(--leaf-muted); font-size: 14px; font-weight: 600; margin-bottom: 6px; margin-top: 16px;"><i class="fa-solid fa-shield-halved" style="color: var(--leaf-primary); margin-right: 8px;"></i>Choose a Password</div>')
        new_password = st.text_input("Choose a Password", placeholder="Create a strong password", type="password", label_visibility="collapsed", key="reg_pass")

        strength_score = 0
        if new_password:
            if len(new_password) >= 8: strength_score += 1
            if re.search(r"[a-z]", new_password): strength_score += 1
            if re.search(r"[A-Z]", new_password): strength_score += 1
            if re.search(r"[0-9]", new_password): strength_score += 1
            if re.search(r"[^a-zA-Z0-9]", new_password): strength_score += 1

        strength_colors = ["#475569", "#ef4444", "#f97316", "#eab308", "#84cc16", "#22c55e"]
        strength_labels = ["", "Very Weak", "Weak", "Fair", "Good", "Strong"]
        pct = (strength_score / 5) * 100 if new_password else 0
        color = strength_colors[strength_score] if new_password else strength_colors[0]
        label = strength_labels[strength_score] if new_password else "Waiting for input..."

        st.html(f"""
        <div style="margin-top: 10px; margin-bottom: 4px;">
            <div style="display: flex; justify-content: space-between; font-size: 13px; color: var(--leaf-muted); margin-bottom: 6px;">
                <span>Password Strength</span>
                <span style="color: {color}; font-weight: 600;">{label}</span>
            </div>
            <div style="height: 6px; width: 100%; background: rgba(255,255,255,0.05); border-radius: 3px; overflow: hidden; border: 1px solid rgba(255,255,255,0.05);">
                <div style="height: 100%; width: {pct}%; background: {color}; transition: width 0.3s ease, background-color 0.3s ease; border-radius: 3px;"></div>
            </div>
        </div>
        """)

        st.html('<div style="color: var(--leaf-muted); font-size: 14px; font-weight: 600; margin-bottom: 6px; margin-top: 16px;"><i class="fa-solid fa-key" style="color: var(--leaf-primary); margin-right: 8px;"></i>Confirm Password</div>')
        confirm_password = st.text_input("Confirm Password", placeholder="Re-enter to verify", type="password", label_visibility="collapsed", key="reg_confirm")
        st.html('<br>')

        passwords_match = False
        if new_password or confirm_password:
            if new_password == confirm_password:
                st.html('<div style="color: #22c55e; font-size: 14px; margin-bottom: 12px; font-weight: 600;"><i class="fa-solid fa-circle-check"></i> Passwords match</div>')
                passwords_match = True
            else:
                st.html('<div style="color: #ef4444; font-size: 14px; margin-bottom: 12px; font-weight: 600;"><i class="fa-solid fa-circle-xmark"></i> Passwords do not match</div>')

        btn_disabled = not (new_username.strip() and new_password.strip() and passwords_match)

        st.markdown('<div class="signup-btn-marker"></div>', unsafe_allow_html=True)
        if st.button("Create Account", type="primary", use_container_width=True, disabled=btn_disabled):
            try:
                from supabase import create_client
                supabase_url = os.getenv("SUPABASE_URL", "https://dloxbfflvfcciczfibxh.supabase.co")
                supabase_key = os.getenv("SUPABASE_KEY")
                if supabase_key:
                    supabase = create_client(supabase_url, supabase_key)
                    check = supabase.table("app_users").select("id").eq("username", new_username.strip()).execute()
                    if check.data:
                        st.error("Username already exists. Please log in or choose another.")
                    else:
                        hashed_pw = hashlib.sha256(new_password.strip().encode('utf-8')).hexdigest()
                        new_user = {"username": new_username.strip(), "password": hashed_pw, "avatar": avatar_emoji}
                        insert_res = supabase.table("app_users").insert(new_user).execute()
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
                            st.error("Failed to create new user account.")
            except Exception as e:
                st.error(f"Registration failed: {e}")


@st.dialog("Prediction History", width="large")
def render_history_dialog():
    from frontend.sections import _generate_history_pdf, clear_history, load_history

    history = load_history()
    if not history:
        empty_placeholder("fa-folder-open", "No History Found", "Analyze a leaf from the Home page first to see records here.")
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
                "Image_URL": st.column_config.ImageColumn("Uploaded Image"),
                "Confidence": st.column_config.NumberColumn("Confidence", format="%.2f%%")
            }
        )

        col1, col2, col3 = st.columns(3)
        pdf_bytes = _generate_history_pdf(history)
        if pdf_bytes:
            with col1:
                st.download_button(
                    label="Download History PDF",
                    data=pdf_bytes,
                    file_name="plantexa_ai_history.pdf",
                    mime="application/pdf",
                    use_container_width=True,
                )
        with col2:
            st.download_button(
                "Download CSV",
                df.to_csv(index=False),
                file_name="prediction_history.csv",
                mime="text/csv",
                use_container_width=True,
            )
        with col3:
            if st.button("Clear History", use_container_width=True):
                clear_history()
                st.session_state.prediction_history = []
                st.rerun()


@st.dialog("Dataset Information", width="large")
def render_dataset_dialog():
    st.html("""
    <div class="glass-card" style="padding: 24px; height: 100%;">
        <h3 style="margin-top: 0; color: var(--leaf-primary); font-family: 'Poppins', sans-serif;"><i class="fa-solid fa-chart-pie"></i> Dataset Summary</h3>
        <ul style="color: var(--leaf-muted); font-size: 16px; padding-left: 20px; line-height: 1.8; margin: 0;">
            <li><strong>Total classes:</strong> 38+</li>
            <li><strong>Image format:</strong> 224 x 224 (RGB)</li>
            <li><strong>Primary purpose:</strong> Plant disease identification from leaf images</li>
            <li><strong>Source:</strong> PlantVillage & Augmented variations</li>
        </ul>
    </div>
    <br>
    <div class="glass-card" style="padding: 24px; height: 100%;">
        <h3 style="margin-top: 0; color: var(--leaf-primary); font-family: 'Poppins', sans-serif;"><i class="fa-solid fa-seedling"></i> Supported Crops</h3>
        <ul style="color: var(--leaf-muted); font-size: 16px; padding-left: 20px; line-height: 1.6; margin: 0; display: grid; grid-template-columns: 1fr 1fr; gap: 8px;">
            <li><i class="fa-solid fa-apple-whole" style="color: #ef4444; width: 20px;"></i> Apple</li>
            <li><i class="fa-solid fa-seedling" style="color: #eab308; width: 20px;"></i> Corn</li>
            <li><i class="fa-solid fa-leaf" style="color: #a855f7; width: 20px;"></i> Grape</li>
            <li><i class="fa-solid fa-lemon" style="color: #fb923c; width: 20px;"></i> Peach</li>
            <li><i class="fa-solid fa-pepper-hot" style="color: #ef4444; width: 20px;"></i> Pepper</li>
            <li><i class="fa-solid fa-carrot" style="color: #d97706; width: 20px;"></i> Potato</li>
            <li><i class="fa-solid fa-leaf" style="color: #f43f5e; width: 20px;"></i> Strawberry</li>
            <li><i class="fa-solid fa-apple-whole" style="color: #ef4444; width: 20px;"></i> Tomato</li>
        </ul>
    </div>
    <br>
    <div class="glass-card" style="padding: 24px; margin-bottom: 8px;">
        <h3 style="margin-top: 0; color: var(--leaf-primary); font-family: 'Poppins', sans-serif;"><i class="fa-solid fa-viruses"></i> Disease Categories</h3>
        <p style="color: var(--leaf-muted); font-size: 16px; line-height: 1.6; margin: 0;">
            The dataset includes healthy leaves and common disease categories such as
            bacterial spot, early blight, late blight, leaf mold, rust, powdery mildew,
            scab, and leaf scorch.
        </p>
    </div>
    """)


@st.dialog("About Plantexa AI", width="large")
def render_about_dialog():
    st.html("""
    <div class="glass-card" style="padding: 24px; margin-bottom: 24px;">
        <p style="color: var(--leaf-muted); font-size: 16px; margin: 0;">
            Plantexa AI uses a two-stage deep learning workflow. It first checks
            whether the uploaded image looks like a plant leaf, then predicts the
            most likely disease and shows symptoms, causes, treatment, and prevention
            guidance from the disease knowledge base.
        </p>
    </div>
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 16px; margin-bottom: 24px;">
        <div class="glass-card" style="padding: 24px;">
            <h4 style="margin-top: 0; color: var(--leaf-primary); font-family: 'Poppins', sans-serif;"><i class="fa-solid fa-desktop"></i> Frontend</h4>
            <ul style="color: var(--leaf-muted); font-size: 14px; padding-left: 20px;">
                <li>Streamlit</li>
                <li>HTML components</li>
                <li>Modern Glassmorphism CSS</li>
            </ul>
        </div>
        <div class="glass-card" style="padding: 24px;">
            <h4 style="margin-top: 0; color: var(--leaf-primary); font-family: 'Poppins', sans-serif;"><i class="fa-solid fa-server"></i> Backend</h4>
            <ul style="color: var(--leaf-muted); font-size: 14px; padding-left: 20px;">
                <li>Python</li>
                <li>TensorFlow</li>
                <li>NumPy & Pandas</li>
            </ul>
        </div>
        <div class="glass-card" style="padding: 24px;">
            <h4 style="margin-top: 0; color: var(--leaf-primary); font-family: 'Poppins', sans-serif;"><i class="fa-solid fa-brain"></i> Models</h4>
            <ul style="color: var(--leaf-muted); font-size: 14px; padding-left: 20px;">
                <li>MobileNetV2 classifier</li>
                <li>Leaf validation network</li>
                <li>224 x 224 resolution</li>
            </ul>
        </div>
    </div>
    <div class="glass-card" style="padding: 24px; margin-bottom: 24px;">
        <h4 style="margin-top: 0; color: var(--leaf-text); font-family: 'Poppins', sans-serif;"><i class="fa-solid fa-list-check" style="color: var(--leaf-primary);"></i> Project Features</h4>
        <ul style="color: var(--leaf-muted); font-size: 15px; margin: 0; padding-left: 20px; line-height: 1.8;">
            <li><strong>Two-Stage Pipeline:</strong> Leaf detection before disease classification</li>
            <li><strong>AI Analysis:</strong> Top 3 predictions with real-time confidence scores</li>
            <li><strong>Knowledge Base:</strong> Detailed disease symptoms, causes, treatment, and prevention</li>
            <li><strong>NVIDIA LLM:</strong> Context-aware AI agriculture assistant</li>
            <li><strong>Reporting:</strong> Downloadable PDF report cards and session prediction history</li>
        </ul>
    </div>
    <div class="glass-card" style="padding: 24px; margin-bottom: 8px;">
        <h4 style="margin-top: 0; color: var(--leaf-text); font-family: 'Poppins', sans-serif;"><i class="fa-solid fa-graduation-cap" style="color: var(--leaf-primary);"></i> Academic Details</h4>
        <p style="color: var(--leaf-muted); font-size: 15px; line-height: 1.8; margin-bottom: 8px;"><strong>Project Team Members:</strong><br>
        Jyotirmaya Behera (3146/24), Diptesh Ranjan Pradhan (3141/24), Bibekananda Sahoo (3136/24), Pritam Kumar Behera (3159/24), Laxman Kumar Sahoo (3148/24)</p>
        <p style="color: var(--leaf-muted); font-size: 15px; margin: 0;"><strong>Academic Year:</strong> 2025 - 2026</p>
    </div>
    """)


@st.dialog("Admin - Database Viewer", width="large")
def render_admin_dialog():
    ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin123")

    if not st.session_state.get("admin_authenticated", False):
        st.html("""
        <div class="glass-card" style="padding: 32px 24px; text-align: center; margin-bottom: 24px; border-top: 3px solid #ef4444;">
            <div style="display: inline-flex; align-items: center; justify-content: center; width: 64px; height: 64px; border-radius: 50%; background: rgba(239, 68, 68, 0.1); color: #ef4444; font-size: 28px; margin-bottom: 16px;">
                <i class="fa-solid fa-lock"></i>
            </div>
            <h2 style="margin: 0 0 12px 0; font-family: 'Poppins', sans-serif; color: var(--leaf-text);">Admin Access Restricted</h2>
            <p style="margin: 0; color: var(--leaf-muted); font-size: 16px;">Please enter the master admin password to access the database viewer.</p>
        </div>
        """)
        pwd = st.text_input("Admin Password", type="password", placeholder="Enter admin password", label_visibility="collapsed", key="dlg_admin_pass")
        if st.button("Unlock Dashboard", type="primary", use_container_width=True):
            if pwd == ADMIN_PASSWORD:
                st.session_state.admin_authenticated = True
                st.rerun()
            else:
                st.error("Incorrect admin password.")
        return

    if st.button("Lock Dashboard", key="dlg_lock_dashboard"):
        st.session_state.admin_authenticated = False
        st.rerun()

    try:
        from supabase import create_client
        supabase_url = os.getenv("SUPABASE_URL", "https://dloxbfflvfcciczfibxh.supabase.co")
        supabase_key = os.getenv("SUPABASE_KEY")
        if not supabase_key:
            st.error("SUPABASE_KEY not found in .env file.")
            return

        supabase = create_client(supabase_url, supabase_key)
        response = supabase.table("user_predictions").select("id, timestamp, disease, confidence, image_url, user_id, app_users(username)").execute()
        df = pd.DataFrame(response.data)

        if not df.empty:
            df["username"] = df["app_users"].apply(lambda x: x.get("username") if isinstance(x, dict) else "Unknown")
            df = df.drop(columns=["app_users"])
            cols = ["id", "username", "timestamp", "disease", "confidence", "image_url", "user_id"]
            df = df[[c for c in cols if c in df.columns]]
        else:
            df = pd.DataFrame(columns=["id", "username", "timestamp", "disease", "confidence", "image_url", "user_id"])

        st.write(f"### Total Records: {len(df)}")
        st.dataframe(
            df.style.map(lambda v: f'color: {get_confidence_color(float(v))}' if isinstance(v, (int, float)) else '', subset=['confidence']),
            use_container_width=True,
            column_config={
                "image_url": st.column_config.ImageColumn("Uploaded Image"),
                "confidence": st.column_config.NumberColumn("Confidence", format="%.2f%%")
            }
        )

        if not df.empty:
            st.write("#### Manage Records")
            col_sel, col_btn_del, col_btn_all = st.columns([2, 1, 1])
            with col_sel:
                row_id = st.selectbox("Select Record ID to delete", df["id"].tolist(), label_visibility="collapsed")
            with col_btn_del:
                if st.button("Delete Row", use_container_width=True):
                    supabase.table("user_predictions").delete().eq("id", row_id).execute()
                    st.rerun()
            with col_btn_all:
                confirm_delete = st.checkbox("Confirm wipe")
                if st.button("Delete ALL", type="primary", use_container_width=True, disabled=not confirm_delete):
                    supabase.table("user_predictions").delete().neq("id", -1).execute()
                    st.rerun()
    except Exception as e:
        st.error(f"Could not load database: {e}")


@st.dialog("User Profile", width="large")
def render_profile_dialog():
    from frontend.sections import load_history

    username = st.session_state.get("username", "Unknown")
    avatar = st.session_state.get("avatar", "🧑‍🌾")
    user_id = st.session_state.get("user_id", "N/A")
    history = load_history()

    st.html(f"""
    <div class="glass-card" style="padding: 32px 24px; text-align: center; margin-bottom: 24px; border-top: 3px solid var(--leaf-primary);">
        <div style="font-size: 72px; margin-bottom: 16px;">{avatar}</div>
        <h2 style="margin: 0 0 8px 0; font-family: 'Poppins', sans-serif; color: var(--leaf-text);">{username}</h2>
        <p style="margin: 0; color: var(--leaf-muted); font-size: 14px;"><strong>Account ID:</strong> {user_id}</p>
    </div>
    <div style="display: flex; gap: 16px; margin-bottom: 24px;">
        <div class="glass-card" style="flex: 1; padding: 16px; text-align: center;">
            <div style="font-size: 24px; font-weight: 800; color: var(--leaf-primary);">{len(history)}</div>
            <div style="font-size: 13px; color: var(--leaf-muted); text-transform: uppercase;">Total Scans</div>
        </div>
    </div>
    """)

    if st.button("Logout", type="primary", use_container_width=True):
        st.session_state.clear()
        st.session_state.clear_cookie = True
        st.rerun()