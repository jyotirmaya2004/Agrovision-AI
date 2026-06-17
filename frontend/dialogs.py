import re
import time

import streamlit as st

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
                loader_placeholder = st.empty()
                loader_placeholder.html(f"""
                <div class="global-loader-overlay">
                    <div class="global-spinner"></div>
                    <h3 class="global-loader-text">{_t("Authenticating...")}</h3>
                </div>
                """)
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
                        loader_placeholder.empty()
                        if check_user_exists(username):
                            st.error(_t("Incorrect password."))
                        else:
                            st.error(_t("Username not found. Please create an account."))
                except Exception as e:
                    loader_placeholder.empty()
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
            loader_placeholder = st.empty()
            loader_placeholder.html(f"""
            <div class="global-loader-overlay">
                <div class="global-spinner"></div>
                <h3 class="global-loader-text">{_t("Creating account...")}</h3>
            </div>
            """)
            try:
                from backend.db import check_user_exists, create_user
                if check_user_exists(new_username):
                    loader_placeholder.empty()
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
                        loader_placeholder.empty()
                        st.error(_t("Failed to create new user account."))
            except Exception as e:
                loader_placeholder.empty()
                st.error(f"{_t('Registration failed:')} {e}")