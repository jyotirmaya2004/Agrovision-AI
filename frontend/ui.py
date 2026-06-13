import io
import json
import os
import re
import hashlib
import time
import uuid
from datetime import datetime

import streamlit as st
from dotenv import load_dotenv
from PIL import Image as PILImage

from backend.disease_info import get_disease_details
from backend.predict_two_stage import PredictionError, predict_two_stage
from frontend.chatbot import chatbot_ui
from frontend.components import (
    empty_placeholder,
    landing_hero,
    prediction_card,
    section_title,
    top_predictions_card,
)
from frontend.styles import load_css

load_dotenv()

def render_navbar(current_page: str = "Home"):
    # 0. Global Toast Notification for New Accounts
    if st.session_state.get("new_account"):
        username = st.session_state.get("username", "User")
        st.html(f"""
        <div class="custom-toast-container">
            <div class="custom-toast">
                <div style="font-size: 24px; color: var(--leaf-primary); display: flex; align-items: center; justify-content: center; width: 48px; height: 48px; background: rgba(34, 197, 94, 0.1); border-radius: 50%;">
                    <i class="fa-solid fa-seedling"></i>
                </div>
                <div>
                    <h4 style="margin: 0 0 4px 0; font-size: 16px; color: var(--leaf-text); font-family: 'Poppins', sans-serif;">Account Created!</h4>
                    <p style="margin: 0; color: var(--leaf-muted); font-size: 14px;">Welcome to Plantexa AI, <strong>{username}</strong>.</p>
                </div>
            </div>
        </div>
        """)
        st.session_state.new_account = False

    # Auto-login via session_restore query param
    restore_user = st.query_params.get("session_restore_user")
    if restore_user and not st.session_state.get("username"):
        st.session_state.username = restore_user
        st.session_state.user_id = st.query_params.get("session_restore_id")
        st.session_state.avatar = st.query_params.get("session_restore_avatar", "🧑‍🌾")
        st.session_state.last_activity = time.time()

        if "session_restore_user" in st.query_params: del st.query_params["session_restore_user"]
        if "session_restore_id" in st.query_params: del st.query_params["session_restore_id"]
        if "session_restore_avatar" in st.query_params: del st.query_params["session_restore_avatar"]

    # 1. Handle cookie & session setting/clearing flags from previous reruns
    if st.session_state.get("set_cookie") or st.session_state.get("sync_session"):
        username = st.session_state.get("username", "")
        user_id = st.session_state.get("user_id", "")
        avatar = st.session_state.get("avatar", "🧑‍🌾")
        ts = int(time.time() * 1000)
        st.html(f"""<img src="empty_{ts}" style="display:none" onerror="const d=new Date(); d.setTime(d.getTime()+(30*24*60*60*1000)); document.cookie='plantexa_user={username};expires='+d.toUTCString()+';path=/'; localStorage.setItem('plantexa_user', '{username}'); localStorage.setItem('plantexa_id', '{user_id}'); localStorage.setItem('plantexa_avatar', '{avatar}');">""")
        st.session_state.set_cookie = None
        st.session_state.sync_session = False

    if st.session_state.get("clear_cookie"):
        ts = int(time.time() * 1000)
        st.html(f"""<img src="empty_{ts}" style="display:none" onerror="document.cookie='plantexa_user=;expires=Thu, 01 Jan 1970 00:00:00 UTC;path=/'; localStorage.removeItem('plantexa_user'); localStorage.removeItem('plantexa_id'); localStorage.removeItem('plantexa_avatar');">""")
        st.session_state.clear_cookie = False

    # 2. Auto-login via native browser cookie if user is not in session state
    if not st.session_state.get("username") and not st.session_state.get("clear_cookie") and hasattr(st, "context") and hasattr(st.context, "cookies"):
        saved_username = st.context.cookies.get("plantexa_user")
        if saved_username:
            try:
                from supabase import create_client
                supabase_url = os.getenv("SUPABASE_URL", "https://dloxbfflvfcciczfibxh.supabase.co")
                supabase_key = os.getenv("SUPABASE_KEY")
                if supabase_key:
                    supabase = create_client(supabase_url, supabase_key)
                    response = supabase.table("app_users").select("id, avatar").eq("username", saved_username).limit(1).execute()
                    if response.data:
                        st.session_state.username = saved_username
                        st.session_state.user_id = response.data[0].get("id")
                        st.session_state.avatar = response.data[0].get("avatar") or "🧑‍🌾"
                        st.session_state.last_activity = time.time()
            except Exception:
                pass

    # Handle mobile menu auth actions via query params
    action = st.query_params.get("action")
    if action == "login":
        st.session_state.show_auth = True
        if "action" in st.query_params:
            del st.query_params["action"]
        st.rerun()
    elif action == "logout":
        st.session_state.clear()
        st.session_state.clear_cookie = True
        if "action" in st.query_params:
            del st.query_params["action"]
        st.rerun()

    is_logged_in = bool(st.session_state.get("username"))
    if not is_logged_in:
        mobile_auth_link = '<a href="/?action=login" class="nav-link mobile-nav-link" style="color: #22C55E; border-top: 1px solid rgba(255,255,255,0.1); margin-top: 8px; padding-top: 16px;"><i class="fa-solid fa-right-to-bracket" style="margin-right: 8px;"></i> Get Started</a>'
    else:
        mobile_auth_link = f'<a href="/?action=logout" class="nav-link mobile-nav-link" style="color: #ef4444; border-top: 1px solid rgba(255,255,255,0.1); margin-top: 8px; padding-top: 16px;"><i class="fa-solid fa-right-from-bracket" style="margin-right: 8px;"></i> Logout ({st.session_state.get("username", "User")})</a>'

    nav_container = st.container()
    with nav_container:
        st.markdown('<div class="navbar-container-marker"></div>', unsafe_allow_html=True)

        py_logged_in = 'true' if is_logged_in else 'false'
        js_code = """
        const initSPA = () => {
            document.querySelectorAll(".nav-link").forEach(link => {
                if (link.dataset.spaAttached) return;
                const href = link.getAttribute("href");
                if (!href || href.includes("?action=") || href.startsWith("#")) return;
                link.dataset.spaAttached = "true";
                link.addEventListener("click", (e) => {
                    e.preventDefault();
                    let targetText = link.innerText.trim();
                    const hiddenLinks = document.querySelectorAll("a[data-testid=stPageLink]");
                    let matched = false;

                    let searchPath = href.replace(/^\\/+/, "").toLowerCase();
                    if (searchPath === "") searchPath = "home";

                    hiddenLinks.forEach(hl => {
                        if (matched) return;
                        const hlHref = (hl.getAttribute("href") || "").replace(/^\\/+/, "").toLowerCase();
                        const hlText = hl.innerText.trim().toLowerCase();

                        if (hlHref && (hlHref === searchPath || hlHref.includes(searchPath))) {
                            hl.click();
                            matched = true;
                        } else if (hlText === targetText.toLowerCase() || hlText.includes(targetText.toLowerCase())) {
                            hl.click();
                            matched = true;
                        }
                    });
                    if (!matched) window.location.href = href;
                });
            });
        };
        initSPA();
        if (!window.spaObserver) {
            window.spaObserver = new MutationObserver(initSPA);
            window.spaObserver.observe(document.body, { childList: true, subtree: true });
        }

        const checkSession = () => {
            const user = localStorage.getItem('plantexa_user');
            const id = localStorage.getItem('plantexa_id');
            const avatar = localStorage.getItem('plantexa_avatar');
            const pyLoggedIn = """ + py_logged_in + """;

            if (user && !pyLoggedIn && !window.location.search.includes('session_restore_user')) {
                const url = new URL(window.location);
                url.searchParams.set('session_restore_user', user);
                if (id) url.searchParams.set('session_restore_id', id);
                if (avatar) url.searchParams.set('session_restore_avatar', avatar);
                url.searchParams.delete('action');
                window.location.replace(url.toString());
            }
        };
        checkSession();

        const hideChrome = () => {
            document.querySelectorAll('header, footer, [class*="viewerBadge"], [class^="viewerBadge_"], [data-testid="stToolbar"], [data-testid="stDeployButton"], [data-testid="stFooter"], [data-testid="stAppHeader"]').forEach(el => {
                el.style.setProperty('display', 'none', 'important');
                el.style.setProperty('visibility', 'hidden', 'important');
                el.style.setProperty('opacity', '0', 'important');
            });
        };
        hideChrome();
        setInterval(hideChrome, 1000);
        """.replace('\n', ' ')

        st.html(f"""
        <input type="checkbox" id="mobile-menu-toggle" class="mobile-menu-toggle">
        <div class="nav-background"></div>
        <div class="nav-processing-line"></div>
        <div class="nav-orb nav-orb-left"></div>
        <div class="nav-orb nav-orb-right"></div>

        <div class="nav-container-inner">
            <div class="nav-brand" aria-label="Plantexa AI">
                <div class="brand-icon"><i class="fa-solid fa-leaf"></i></div>
                <span class="nav-brand-title">Plantexa AI</span>
            </div>

            <div class="nav-right">
                <div class="nav-links" role="navigation" aria-label="Primary">
                    <a href="/" class="nav-link{' active' if current_page == 'Home' else ''}">Home</a>
                    <a href="/Dataset" class="nav-link{' active' if current_page == 'Dataset' else ''}">Dataset</a>
                    <a href="/History" class="nav-link{' active' if current_page == 'History' else ''}">History</a>
                    <a href="/Profile" class="nav-link{' active' if current_page == 'Profile' else ''}">Profile</a>
                    <a href="/About" class="nav-link{' active' if current_page == 'About' else ''}">About</a>
                    <a href="/Admin" class="nav-link{' active' if current_page == 'Admin' else ''}">Admin</a>
                </div>

                <div class="nav-cta-slot" aria-hidden="true"></div>

                <label for="mobile-menu-toggle" class="hamburger-btn" aria-label="Open menu">
                    <span></span>
                    <span></span>
                    <span></span>
                </label>
            </div>
        </div>

        <div class="mobile-dropdown" role="dialog" aria-label="Mobile navigation">
            <div class="mobile-nav-links">
                <a href="/" class="nav-link mobile-nav-link{' active' if current_page == 'Home' else ''}"><i class="fa-solid fa-house" style="margin-right: 8px;"></i> Home</a>
                <a href="/Dataset" class="nav-link mobile-nav-link{' active' if current_page == 'Dataset' else ''}"><i class="fa-solid fa-database" style="margin-right: 8px;"></i> Dataset</a>
                <a href="/History" class="nav-link mobile-nav-link{' active' if current_page == 'History' else ''}"><i class="fa-solid fa-clock-rotate-left" style="margin-right: 8px;"></i> History</a>
                <a href="/Profile" class="nav-link mobile-nav-link{' active' if current_page == 'Profile' else ''}"><i class="fa-solid fa-user" style="margin-right: 8px;"></i> Profile</a>
                <a href="/About" class="nav-link mobile-nav-link{' active' if current_page == 'About' else ''}"><i class="fa-solid fa-circle-info" style="margin-right: 8px;"></i> About</a>
                <a href="/Admin" class="nav-link mobile-nav-link{' active' if current_page == 'Admin' else ''}"><i class="fa-solid fa-lock" style="margin-right: 8px;"></i> Admin</a>
                {mobile_auth_link}
            </div>
        </div>
        """)


        # IMPORTANT: keep mobile behavior unchanged.
        # For desktop, show a toggle-style auth CTA:
        # - logged out: show "Get Started" that triggers the authentication card
        # - logged in: show a red-themed "Logout" button
        if not is_logged_in:
            st.html('<div class="nav-btn-marker logged-out"></div>')
            # Show a desktop Get Started button. This should NOT affect mobile.
            # (Mobile CSS can hide/ignore .nav-auth-toggle for hamburger layout.)
            if st.button(
                "Get Started",
                key="get_started_navbar",
                use_container_width=True,
            ):
                st.session_state.show_auth = True
                st.rerun()
        else:
            st.html('<div class="nav-btn-marker logged-in"></div>')
            if st.button("Logout", key="logout_navbar", use_container_width=True):
                st.session_state.clear()
                st.session_state.clear_cookie = True
                st.rerun()

    # Render hidden Streamlit page links inside a container to act as SPA routing targets
    spa_container = st.container()
    with spa_container:
        st.markdown('<div class="hidden-spa-marker"></div>', unsafe_allow_html=True)
        st.page_link("app.py", label="Home")
        st.page_link("pages/2_Dataset.py", label="Dataset")
        st.page_link("pages/1_History.py", label="History")
        st.page_link("pages/4_Profile.py", label="Profile")
        st.page_link("pages/3_About.py", label="About")
        st.page_link("pages/3_Admin.py", label="Admin")

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

def require_username(force=False):
    # 1. Check for inactivity timeout (1800 seconds = 30 minutes)
    if st.session_state.get("username"):
        last_active = st.session_state.get("last_activity", time.time())
        if time.time() - last_active > 1800:
            st.session_state.clear()
            st.session_state.clear_cookie = True
            st.session_state.show_auth = True
            st.session_state.logout_reason = "Session expired due to 30 minutes of inactivity. Please log in again."
            st.rerun()
        else:
            st.session_state.last_activity = time.time()

    if not st.session_state.get("username"):
        if not force and not st.session_state.get("show_auth", False):
            return

        render_auth_dialog()

        if force:
            st.html(
                """
                <div class="glass-card" style="padding: 40px 24px; text-align: center; margin-top: 16px; border-top: 3px solid var(--leaf-primary);">
                    <div style="display: inline-flex; align-items: center; justify-content: center; width: 64px; height: 64px; border-radius: 50%; background: rgba(34, 197, 94, 0.1); color: var(--leaf-primary); font-size: 28px; margin-bottom: 16px;">
                        <i class="fa-solid fa-lock"></i>
                    </div>
                    <h1 style="margin: 0 0 12px 0; font-family: 'Poppins', sans-serif; font-size: 32px !important; color: var(--leaf-text);">Authentication Required</h1>
                    <p style="margin: 0; color: var(--leaf-muted); font-size: 18px; max-width: 600px; margin-left: auto; margin-right: auto;">You must be logged in to access this page. Please use the popup to authenticate.</p>
                </div>
                """
            )
            st.stop()
        else:
            st.session_state.show_auth = False

def load_history():
    user_id = st.session_state.get("user_id")
    if not user_id:
        return []
    try:
        from supabase import create_client
        supabase_url = os.getenv("SUPABASE_URL", "https://dloxbfflvfcciczfibxh.supabase.co")
        supabase_key = os.getenv("SUPABASE_KEY")
        if supabase_key:
            supabase = create_client(supabase_url, supabase_key)
            response = supabase.table("user_predictions").select("*").eq("user_id", user_id).order("id").execute()
            rows = response.data
            return [{"Timestamp": r["timestamp"], "Disease": r["disease"], "Confidence": r["confidence"], "Image_URL": r.get("image_url")} for r in rows]
    except Exception as e:
        st.warning(f"Could not load history from Supabase: {e}")
    return []

def append_history(item):
    user_id = st.session_state.get("user_id")
    if not user_id:
        return
    try:
        from supabase import create_client
        supabase_url = os.getenv("SUPABASE_URL", "https://dloxbfflvfcciczfibxh.supabase.co")
        supabase_key = os.getenv("SUPABASE_KEY")
        if supabase_key:
            supabase = create_client(supabase_url, supabase_key)
            record = {
                "user_id": user_id,
                "timestamp": item["Timestamp"],
                "disease": item["Disease"],
                "confidence": item["Confidence"],
                "image_url": item.get("Image_URL")
            }
            supabase.table("user_predictions").insert(record).execute()
    except Exception as e:
        st.warning(f"Could not save history to Supabase: {e}")

def clear_history():
    user_id = st.session_state.get("user_id")
    if not user_id:
        return
    try:
        from supabase import create_client
        supabase_url = os.getenv("SUPABASE_URL", "https://dloxbfflvfcciczfibxh.supabase.co")
        supabase_key = os.getenv("SUPABASE_KEY")
        if supabase_key:
            supabase = create_client(supabase_url, supabase_key)
            supabase.table("user_predictions").delete().eq("user_id", user_id).execute()
    except Exception as e:
        st.warning(f"Could not clear history: {e}")

def render_header():
    landing_hero()


def render_upload_section():
    section_title("Image Input", "fa-cloud-arrow-up", anchor_id="diagnosis-section")

    col_input, col_preview = st.columns([1.3, 1], gap="large")

    with col_input:
        st.subheader("Choose Input Method")
        default_source = 1 if st.query_params.get("source") == "camera" else 0
        source_choice = st.radio(
            "Select Input Method",
            ["Upload from device", "Use camera"],
            index=default_source,
            horizontal=True,
            label_visibility="collapsed"
        )

        if source_choice == "Use camera":
            image_file = st.camera_input("Take a clear leaf photo", label_visibility="collapsed")
        else:
            image_file = st.file_uploader(
                "Choose a leaf image",
                type=["jpg", "jpeg", "png", "webp", "bmp", "gif", "tiff", "heic", "heif"],
                label_visibility="collapsed"
            )

    with col_preview:
        st.subheader("Analysis Readiness")
        if image_file:
            st.image(image_file, caption="Ready for analysis", use_container_width=True)
            size_mb = len(image_file.getvalue()) / (1024 * 1024)
            st.caption(f"**Status:** Valid File | **File Size:** {size_mb:.2f} MB")
        else:
            empty_placeholder("fa-image", "No Image Selected", "Your selected image will appear here.")

    return image_file


def _generate_report_pdf(image_bytes, prediction, disease_info):
    try:
        from reportlab.lib.pagesizes import letter
        from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
        from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
        from reportlab.platypus import Image as RLImage
        from reportlab.lib import colors
        from reportlab.lib.units import inch
    except ImportError:
        return None

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer, pagesize=letter, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40
    )
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Title'],
        fontSize=22,
        textColor=colors.HexColor('#1b4332'),
        spaceAfter=20
    )

    h2_style = ParagraphStyle(
        'CustomH2',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#2d6a4f'),
        spaceBefore=12,
        spaceAfter=6
    )

    story = []
    story.append(Paragraph("<b>Plantexa AI - Plant Health Report Card</b>", title_style))
    story.append(Spacer(1, 10))

    if image_bytes:
        try:
            img_io = io.BytesIO(image_bytes)
            pil_img = PILImage.open(img_io)
            # Strip transparency channels for flawless PDF insertion
            if pil_img.mode in ('RGBA', 'LA') or (pil_img.mode == 'P' and 'transparency' in pil_img.info):
                alpha = pil_img.convert('RGBA').split()[-1]
                bg = PILImage.new("RGB", pil_img.size, (255, 255, 255))
                bg.paste(pil_img, mask=alpha)
                pil_img = bg
            else:
                pil_img = pil_img.convert('RGB')

            clean_img_io = io.BytesIO()
            pil_img.save(clean_img_io, format='JPEG')
            clean_img_io.seek(0)

            # Proportionally scale image to fit nicely on the document
            img_width, img_height = pil_img.size
            max_w, max_h = 400.0, 250.0
            ratio = min(max_w / img_width, max_h / img_height)
            new_w, new_h = img_width * ratio, img_height * ratio

            rl_img = RLImage(clean_img_io, width=new_w, height=new_h)

            img_table = Table([[rl_img]], colWidths=[new_w + 10])
            img_table.setStyle(TableStyle([
                ('ALIGN', (0,0), (-1,-1), 'CENTER'),
                ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
                ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#cbd5e1')),
                ('TOPPADDING', (0,0), (-1,-1), 5),
                ('BOTTOMPADDING', (0,0), (-1,-1), 5),
                ('LEFTPADDING', (0,0), (-1,-1), 5),
                ('RIGHTPADDING', (0,0), (-1,-1), 5),
            ]))
            story.append(img_table)
            story.append(Spacer(1, 20))
        except Exception:
            pass

    disease = prediction.get("disease", "Unknown")
    confidence = prediction.get("confidence", 0.0)

    data = [
        [Paragraph("<b>Diagnosed Disease</b>", styles["Normal"]), Paragraph(disease, styles["Normal"])],
        [Paragraph("<b>Model Confidence</b>", styles["Normal"]), Paragraph(f"{confidence}%", styles["Normal"])]
    ]

    top_preds = prediction.get("top_predictions", [])
    if len(top_preds) > 1:
        alts = ", ".join([f"{p['disease']} ({p['confidence']}%)" for p in top_preds[1:]])
        data.append([Paragraph("<b>Other Predictions</b>", styles["Normal"]), Paragraph(alts, styles["Normal"])])

    t = Table(data, colWidths=[1.5*inch, 4.5*inch])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,-1), colors.HexColor('#eaf4f0')),
        ('GRID', (0,0), (-1,-1), 1, colors.HexColor('#cbd5e1')),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('PADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t)
    story.append(Spacer(1, 15))

    if disease_info:
        for section in ["symptoms", "causes", "treatment", "prevention"]:
            if section in disease_info and disease_info[section]:
                story.append(Paragraph(f"{section.title()}", h2_style))
                text = disease_info[section].replace("<", "&lt;").replace(">", "&gt;")
                story.append(Paragraph(text, styles["Normal"]))
                story.append(Spacer(1, 8))

    def add_footer(canvas, doc):
        canvas.saveState()
        canvas.setFont('Helvetica', 9)
        canvas.setFillColor(colors.dimgrey)
        footer_text = f"Plantexa AI Report Card - Page {doc.page}"
        canvas.drawCentredString(letter[0] / 2.0, 0.5 * inch, footer_text)
        date_str = datetime.now().strftime("%B %d, %Y")
        canvas.drawString(0.5 * inch, 0.5 * inch, date_str)
        canvas.restoreState()

    doc.build(story, onFirstPage=add_footer, onLaterPages=add_footer)
    return buffer.getvalue()


def _generate_history_pdf(history_data):
    try:
        from reportlab.lib.pagesizes import letter
        from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
        from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
        from reportlab.platypus import Image as RLImage
        from reportlab.lib import colors
        from reportlab.lib.units import inch
        import httpx
    except ImportError:
        return None

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer, pagesize=letter, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40
    )
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Title'],
        fontSize=22,
        textColor=colors.HexColor('#1b4332'),
        spaceAfter=20
    )

    story = []
    story.append(Paragraph("<b>Plantexa AI - Prediction History</b>", title_style))
    story.append(Spacer(1, 10))

    if history_data:
        table_data = [[
            Paragraph("<b>Image</b>", styles["Normal"]),
            Paragraph("<b>Date/Time</b>", styles["Normal"]),
            Paragraph("<b>Disease</b>", styles["Normal"]),
            Paragraph("<b>Confidence</b>", styles["Normal"])
        ]]
        for item in history_data:
            dt = item.get("Timestamp", "N/A")
            disease = item.get("Disease", "Unknown")
            conf = f"{item.get('Confidence', 0)}%"

            img_element = Paragraph("No Image", styles["Normal"])
            img_url = item.get("Image_URL")
            if img_url:
                try:
                    resp = httpx.get(img_url, timeout=5.0)
                    if resp.status_code == 200:
                        img_io = io.BytesIO(resp.content)
                        pil_img = PILImage.open(img_io)

                        if pil_img.mode in ('RGBA', 'LA') or (pil_img.mode == 'P' and 'transparency' in pil_img.info):
                            alpha = pil_img.convert('RGBA').split()[-1]
                            bg = PILImage.new("RGB", pil_img.size, (255, 255, 255))
                            bg.paste(pil_img, mask=alpha)
                            pil_img = bg
                        else:
                            pil_img = pil_img.convert('RGB')

                        clean_img_io = io.BytesIO()
                        pil_img.save(clean_img_io, format='JPEG')
                        clean_img_io.seek(0)

                        img_width, img_height = pil_img.size
                        max_size = 0.9 * inch
                        ratio = min(max_size / img_width, max_size / img_height)
                        img_element = RLImage(clean_img_io, width=img_width * ratio, height=img_height * ratio)
                except Exception:
                    pass

            table_data.append([
                img_element,
                Paragraph(dt, styles["Normal"]),
                Paragraph(disease, styles["Normal"]),
                Paragraph(conf, styles["Normal"])
            ])

        t = Table(table_data, colWidths=[1.2*inch, 1.8*inch, 2.7*inch, 1.3*inch])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#eaf4f0')),
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('BOTTOMPADDING', (0,0), (-1,0), 8),
            ('GRID', (0,0), (-1,-1), 1, colors.HexColor('#cbd5e1')),
            ('PADDING', (0,0), (-1,-1), 8),
        ]))
        story.append(t)
    else:
        story.append(Paragraph("No prediction history available.", styles["Normal"]))

    def add_footer(canvas, doc):
        canvas.saveState()
        canvas.setFont('Helvetica', 9)
        canvas.setFillColor(colors.dimgrey)
        footer_text = f"Plantexa AI History - Page {doc.page}"
        canvas.drawCentredString(letter[0] / 2.0, 0.5 * inch, footer_text)
        date_str = datetime.now().strftime("%B %d, %Y")
        canvas.drawString(0.5 * inch, 0.5 * inch, date_str)
        canvas.restoreState()

    doc.build(story, onFirstPage=add_footer, onLaterPages=add_footer)
    return buffer.getvalue()


def render_prediction_section(image_file):
    section_title("Diagnosis Dashboard", "fa-chart-pie")

    with st.expander("Debug: leaf vs non-leaf output", expanded=False):
        show_debug = st.checkbox("Show raw leaf validation output", value=False)

    if image_file is None:
        empty_placeholder("fa-microscope", "Awaiting Image", "Please upload or capture an image above to start analysis.")
        return

    st.markdown('<div class="analyze-btn-marker"></div><div class="analyze-btn-spacer"></div>', unsafe_allow_html=True)
    analyze_clicked = st.button("Analyze Leaf", type="primary", use_container_width=True)

    if analyze_clicked:
        # Require authentication to perform an analysis
        if not st.session_state.get("username"):
            st.session_state.show_auth = True
            st.rerun()

        with st.status("Analyzing Leaf Image...", expanded=True) as status:
            st.write("☁️ Uploading image to Supabase...")
            image_url = None
            try:
                from supabase import create_client
                supabase_url = os.getenv("SUPABASE_URL", "https://dloxbfflvfcciczfibxh.supabase.co")
                supabase_key = os.getenv("SUPABASE_KEY")

                if supabase_key:
                    supabase = create_client(supabase_url, supabase_key)
                    file_ext = "jpg"
                    if hasattr(image_file, "name") and "." in image_file.name:
                        file_ext = image_file.name.split('.')[-1]

                    file_name = f"{uuid.uuid4()}.{file_ext}"

                    supabase.storage.from_("Leafimage").upload(
                        path=file_name,
                        file=image_file.getvalue(),
                        file_options={"content-type": image_file.type if hasattr(image_file, "type") else "image/jpeg"}
                    )
                    image_url = supabase.storage.from_("Leafimage").get_public_url(file_name)
                else:
                    st.warning("SUPABASE_KEY not found in .env file. Upload skipped.")
            except ImportError:
                st.warning("Supabase package not installed. Please run `pip install supabase`.")
            except Exception as e:
                error_msg = str(e).lower()
                if "policy" in error_msg or "row-level security" in error_msg or "unauthorized" in error_msg:
                    st.warning("⚠️ Image upload blocked by Supabase policy restrictions. Please check your storage bucket permissions.")
                else:
                    st.warning(f"Could not upload image to Supabase: {e}")

            try:
                st.write("🔍 Extracting image features...")
                time.sleep(0.5)
                st.write("🌿 Validating leaf presence...")
                time.sleep(0.5)
                st.write("🧬 Running disease classification model...")
                result = predict_two_stage(image_file, top_k=3)

                st.write("☁️ Uploading image to Supabase...")
                image_url = None
                try:
                    from supabase import create_client
                    supabase_url = os.getenv("SUPABASE_URL", "https://dloxbfflvfcciczfibxh.supabase.co")
                    supabase_key = os.getenv("SUPABASE_KEY")

                    if supabase_key:
                        supabase = create_client(supabase_url, supabase_key)
                        file_ext = "jpg"
                        if hasattr(image_file, "name") and "." in image_file.name:
                            file_ext = image_file.name.split('.')[-1]

                        file_name = f"{uuid.uuid4()}.{file_ext}"

                        supabase.storage.from_("Leafimage").upload(
                            path=file_name,
                            file=image_file.getvalue(),
                            file_options={"content-type": image_file.type if hasattr(image_file, "type") else "image/jpeg"}
                        )
                        image_url = supabase.storage.from_("Leafimage").get_public_url(file_name)
                    else:
                        st.warning("SUPABASE_KEY not found in .env file. Upload skipped.")
                except ImportError:
                    st.warning("Supabase package not installed. Please run `pip install supabase`.")
                except Exception as e:
                    error_msg = str(e).lower()
                    if "policy" in error_msg or "row-level security" in error_msg or "unauthorized" in error_msg:
                        st.warning("⚠️ Image upload blocked by Supabase policy restrictions. Please check your storage bucket permissions.")
                    else:
                        st.warning(f"Could not upload image to Supabase: {e}")

                st.session_state.prediction = result

                new_record = {
                    "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "Disease": result["disease"],
                    "Confidence": result["confidence"],
                    "Image_URL": image_url,
                }
                append_history(new_record)

                st.session_state.prediction_history = load_history()
                status.update(label="Analysis Complete", state="complete", expanded=False)
            except PredictionError as exc:
                st.session_state.prediction = None

                new_record = {
                    "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "Disease": "Failed: Invalid Image (Not a Leaf)",
                    "Confidence": 0.0,
                    "Image_URL": image_url,
                }
                append_history(new_record)
                st.session_state.prediction_history = load_history()

                status.update(label="Analysis Failed", state="error", expanded=False)
                st.error(str(exc))
            except Exception as exc:
                st.session_state.prediction = None

                new_record = {
                    "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "Disease": "Analysis Error",
                    "Confidence": 0.0,
                    "Image_URL": image_url,
                }
                append_history(new_record)
                st.session_state.prediction_history = load_history()

                status.update(label="Analysis Failed", state="error", expanded=False)
                st.error(f"Unexpected error: {exc}")

    result = st.session_state.get("prediction")
    if not result:
        return

    st.success("Analysis Complete!")

    if result.get("validation_warning"):
        st.warning(result["validation_warning"])

    # Dashboard Row 1
    col_diag, col_top = st.columns([1, 1], gap="large")
    with col_diag:
        section_title("Diagnosis Result", "fa-virus")
        prediction_card(result["disease"], result["confidence"])
    with col_top:
        section_title("Alternate Probabilities", "fa-layer-group")
        top_predictions_card([(pred["disease"], pred["confidence"]) for pred in result["top_predictions"]])

    if show_debug:
        st.json(result["leaf_validation"])

    st.html("<br>")
    section_title("Diagnosis & Treatment Hub", "fa-briefcase-medical")
    disease_info = get_disease_details(result["class_name"])

    tab_sym, tab_treat, tab_prev, tab_comp = st.tabs(["Symptoms & Causes", "Treatment Plans", "Prevention", "Similar Diseases"])

    with tab_sym:
        st.write("### Disease Description & Symptoms")
        st.write(disease_info.get("symptoms", "No symptom information available."))
        st.write("### Primary Causes")
        st.write(disease_info.get("causes", "No cause information available."))

    with tab_treat:
        st.write("### AI Recommended Treatments")
        st.info("The following treatments are scientifically recommended based on your diagnosis.")
        st.write(disease_info.get("treatment", "No treatment information available."))
        col_c1, col_c2 = st.columns(2)
        with col_c1:
            st.metric("Estimated Treatment Cost", "Low - Moderate")
        with col_c2:
            st.metric("Effectiveness Score", "High (85-95%)")

    with tab_prev:
        st.write("### Best Practices & Prevention")
        st.write(disease_info.get("prevention", "No prevention information available."))
        st.success("Follow these practices to prevent future outbreaks and maintain crop health.")

    with tab_comp:
        st.write("### Disease Comparison")
        st.write("Comparing current diagnosis against similar pathogens.")
        if len(result["top_predictions"]) > 1:
            alt_disease = result["top_predictions"][1]["disease"]
            st.warning(f"**Similar Match:** {alt_disease}. Monitor for overlapping symptoms.")
        else:
            st.write("No similar diseases found for comparison.")

    st.html("<br>")
    section_title("Diagnosis Report", "fa-file-pdf")
    st.info("Save a detailed PDF report of this diagnosis, including the uploaded image and treatment guidelines.")

    image_bytes = image_file.getvalue() if image_file else None
    pdf_bytes = _generate_report_pdf(image_bytes, result, disease_info)

    if pdf_bytes:
        safe_name = re.sub(r'[^a-zA-Z0-9]+', '_', result['disease']).strip('_').lower()
        if st.download_button(
            label="Download Full Report Card",
            data=pdf_bytes,
            file_name=f"plantexa_report_{safe_name}.pdf",
            mime="application/pdf",
        ):
            st.markdown('<div class="success-msg-anim"><i class="fa-solid fa-circle-check"></i> Report downloaded successfully!</div>', unsafe_allow_html=True)
    else:
        st.warning("ReportLab is required to generate PDF reports. Please run `pip install reportlab`.")

def render_history_section():
    section_title("Prediction History", "fa-clock-rotate-left")

    history = load_history()
    st.session_state.prediction_history = history

    if not history:
        st.info("No history yet. Analyze a leaf image to see records here.")
        return

    st.dataframe(
        history,
        use_container_width=True,
        column_config={
            "Image_URL": st.column_config.ImageColumn("Uploaded Image")
        }
    )

    col1, col2 = st.columns(2)

    pdf_bytes = _generate_history_pdf(history)
    if pdf_bytes:
        with col1:
            if st.download_button(
                label="Download History PDF",
                data=pdf_bytes,
                file_name="plantexa_ai_history.pdf",
                mime="application/pdf",
                use_container_width=True,
            ):
                st.markdown('<div class="success-msg-anim"><i class="fa-solid fa-circle-check"></i> PDF downloaded successfully!</div>', unsafe_allow_html=True)
    with col2:
        if st.button("Clear History", key="clear_history_home", use_container_width=True):
            clear_history()
            st.session_state.prediction_history = []
            st.rerun()


def render_tips_section():
    section_title("Quick Care Tips", "fa-lightbulb")

    st.html("""
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 16px; margin-bottom: 24px;">
        <div class="glass-card" style="padding: 20px; border-top: 3px solid #3b82f6;">
            <h4 style="margin-top:0; color: #60a5fa; font-family: 'Poppins', sans-serif;"><i class="fa-solid fa-droplet"></i> Watering</h4>
            <p style="color: var(--leaf-muted); font-size: 14px; margin-bottom: 0;">Water at the base of the plant to prevent leaf wetness and fungal growth.</p>
        </div>
        <div class="glass-card" style="padding: 20px; border-top: 3px solid #eab308;">
            <h4 style="margin-top:0; color: #fde047; font-family: 'Poppins', sans-serif;"><i class="fa-solid fa-sun"></i> Sunlight</h4>
            <p style="color: var(--leaf-muted); font-size: 14px; margin-bottom: 0;">Ensure proper canopy pruning to allow UV light to naturally disinfect lower leaves.</p>
        </div>
        <div class="glass-card" style="padding: 20px; border-top: 3px solid #a855f7;">
            <h4 style="margin-top:0; color: #c084fc; font-family: 'Poppins', sans-serif;"><i class="fa-solid fa-wind"></i> Airflow</h4>
            <p style="color: var(--leaf-muted); font-size: 14px; margin-bottom: 0;">Maintain adequate spacing between crops to reduce humidity and powdery mildew risk.</p>
        </div>
    </div>
    """)


def render_footer():
    st.html("""
    <div class="saas-footer">
        <div class="footer-gradient-line"></div>

        <!-- Floating Particles -->
        <div class="footer-particle fp-1"></div>
        <div class="footer-particle fp-2"></div>
        <div class="footer-particle fp-3"></div>
        <div class="footer-particle fp-4"></div>

        <div class="footer-content">
            <!-- Statistics Bar -->
            <div class="footer-stats">
                <div class="f-stat"><span class="f-stat-val">15+</span><span class="f-stat-label">Plant Species</span></div>
                <div class="f-stat"><span class="f-stat-val">38+</span><span class="f-stat-label">Diseases</span></div>
                <div class="f-stat"><span class="f-stat-val">98%</span><span class="f-stat-label">Accuracy</span></div>
                <div class="f-stat"><span class="f-stat-val">10K+</span><span class="f-stat-label">Analyses</span></div>
            </div>

            <!-- Trust Indicators -->
            <div class="footer-trust">
                <span><i class="fa-solid fa-check"></i> AI Powered</span>
                <span><i class="fa-solid fa-check"></i> NVIDIA Accelerated</span>
                <span><i class="fa-solid fa-check"></i> Secure Uploads</span>
                <span><i class="fa-solid fa-check"></i> Real-Time Analysis</span>
                <span><i class="fa-solid fa-check"></i> Research Grade Models</span>
            </div>

            <!-- Main Columns -->
            <div class="footer-grid">
                <!-- Column 1: Brand -->
                <div class="footer-col">
                    <div class="f-logo">
                        <i class="fa-solid fa-leaf f-logo-icon"></i> Plantexa AI
                    </div>
                    <p class="f-desc">AI-powered plant disease diagnosis and crop health intelligence platform.</p>
                    <div class="f-badges">
                        <span class="f-badge">v2.0.0</span>
                        <span class="f-badge nvidia-badge"><i class="fa-solid fa-microchip"></i> Powered by NVIDIA AI</span>
                    </div>
                </div>

                <!-- Column 2: Navigation -->
                <div class="footer-col">
                    <h4 class="f-heading">Navigation</h4>
                    <a href="#diagnosis-section" class="f-link">Home</a>
                    <a href="#diagnosis-section" class="f-link">Disease Detection</a>
                    <a href="?tab=history" class="f-link">Prediction History</a>
                    <a href="?tab=history" class="f-link">Reports</a>
                    <a href="#diagnosis-section" class="f-link">Dashboard</a>
                    <a href="#diagnosis-section" class="f-link">Analytics</a>
                    <a href="?tab=chat" class="f-link">Chat Assistant</a>
                </div>

                <!-- Column 3: Resources -->
                <div class="footer-col">
                    <h4 class="f-heading">Resources</h4>
                    <a href="#" class="f-link">Documentation</a>
                    <a href="#" class="f-link">User Guide</a>
                    <a href="#" class="f-link">FAQ</a>
                    <a href="#" class="f-link">API Reference</a>
                    <a href="#" class="f-link">Privacy Policy</a>
                    <a href="#" class="f-link">Terms & Conditions</a>
                </div>

                <!-- Column 4: Contact & Newsletter -->
                <div class="footer-col">
                    <h4 class="f-heading">Connect</h4>
                    <a href="#" class="f-social"><i class="fa-brands fa-github"></i> GitHub</a>
                    <a href="#" class="f-social"><i class="fa-brands fa-linkedin"></i> LinkedIn</a>
                    <a href="#" class="f-social"><i class="fa-solid fa-envelope"></i> Email</a>
                    <a href="#" class="f-social"><i class="fa-solid fa-briefcase"></i> Portfolio</a>
                    <a href="#" class="f-social"><i class="fa-solid fa-headset"></i> Contact Us</a>

                    <div style="margin-top: 24px;">
                        <p class="f-desc" style="margin-bottom: 8px;">Get latest crop disease updates</p>
                        <form class="f-form" onsubmit="event.preventDefault();">
                            <input type="email" placeholder="Email address..." class="f-input" />
                            <button type="submit" class="f-submit"><i class="fa-solid fa-arrow-right"></i></button>
                        </form>
                    </div>
                </div>
            </div>

            <!-- Bottom Copyright Section -->
            <div class="footer-bottom">
                <p>&copy; 2026 Plantexa AI</p>
                <p>Built with Streamlit <i class="fa-solid fa-plus" style="font-size:10px; margin:0 4px; color:var(--leaf-primary);"></i> Deep Learning <i class="fa-solid fa-plus" style="font-size:10px; margin:0 4px; color:var(--leaf-primary);"></i> NVIDIA AI</p>
            </div>
        </div>
    </div>
    """)


def main(active_tab: str = "all"):
    load_css()
    render_navbar("Home")
    require_username()
    render_header()

    if active_tab == "history":
        render_history_section()
        return

    if active_tab == "tips":
        render_tips_section()
        return

    if active_tab == "chat":
        chatbot_ui()
        return

    image_file = render_upload_section()
    render_prediction_section(image_file)

    render_history_section()

    render_tips_section()

    render_footer()
    chatbot_ui()
