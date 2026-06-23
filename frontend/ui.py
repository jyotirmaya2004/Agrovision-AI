import time

import streamlit as st
from dotenv import load_dotenv

from frontend.chatbot import chatbot_ui
from frontend.dialogs import render_auth_dialog

from frontend.sections import (
    render_footer,
    render_header,
    render_history_section,
    render_prediction_section,
    render_tips_section,
    render_upload_section,
    render_team_section,
)
from frontend.styles import load_css
from backend.disease_info import _t

load_dotenv()

def _handle_query_params():
    """Safely handle explicit actions and dialog triggers from query params.

    Important: this must only run after we have attempted to restore a session.
    We also ensure we never clear session unless the user is already logged in.
    """
    action = st.query_params.get("action")
    if action in ["login", "logout"]:
        if action == "login":
            st.session_state.show_auth = True
        elif action == "logout":
            # Only clear when the user is currently logged in; otherwise ignore.
            if st.session_state.get("username"):
                st.session_state.clear()
                st.session_state.clear_cookie = True

        if "action" in st.query_params:
            del st.query_params["action"]

        st.rerun()

    lang = st.query_params.get("lang")
    if lang:
        lang_map = {
            "en": "English",
            "hi": "Hindi (हिंदी)",
            "or": "Odia (ଓଡ଼ିଆ)"
        }
        if lang in lang_map:
            st.session_state.app_lang = lang_map[lang]
            st.session_state.lang_code = lang
        if "lang" in st.query_params:
            del st.query_params["lang"]
        st.rerun()

def render_navbar(current_page: str = "Home"):
    # Ensure auth/session is restored as early as possible on every rerun
    restore_session_if_needed()

    # Handle explicit actions and dialog triggers from query params
    _handle_query_params()

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
                    <h4 style="margin: 0 0 4px 0; font-size: 16px; color: var(--leaf-text); font-family: 'Poppins', sans-serif;">{_t('Account Created!')}</h4>
                    <p style="margin: 0; color: var(--leaf-muted); font-size: 14px;">{_t('Welcome to Plantexa AI')}, <strong>{username}</strong>.</p>
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
                from backend.db import get_user_by_username
                user_data = get_user_by_username(saved_username)
                if user_data:
                    st.session_state.username = saved_username
                    st.session_state.user_id = user_data.get("id")
                    st.session_state.avatar = user_data.get("avatar") or "🧑‍🌾"
                    st.session_state.last_activity = time.time()
            except Exception:
                pass


    is_logged_in = bool(st.session_state.get("username"))
    if not is_logged_in:
        mobile_auth_link = f'<a href="?action=login" class="nav-link mobile-nav-link" style="color: #22C55E; border-top: 1px solid rgba(255,255,255,0.1); margin-top: 8px; padding-top: 16px;"><i class="fa-solid fa-right-to-bracket" style="margin-right: 8px;"></i> {_t("Get Started")}</a>'
    else:
        mobile_auth_link = f'<a href="?action=logout" class="nav-link mobile-nav-link" style="color: #ef4444; border-top: 1px solid rgba(255,255,255,0.1); margin-top: 8px; padding-top: 16px;"><i class="fa-solid fa-right-from-bracket" style="margin-right: 8px;"></i> {_t("Logout")} ({st.session_state.get("username", "User")})</a>'

    nav_container = st.container()
    with nav_container:
        st.markdown('<div class="navbar-container-marker"></div>', unsafe_allow_html=True)

        py_logged_in = 'true' if is_logged_in else 'false'
        js_code = """
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

        curr_lang = st.session_state.get('lang_code', 'en')
        check_icon = '<i class="fa-solid fa-check" style="margin-left: auto;"></i>'

        # Use relative anchors for smooth CSS scrolling when already on the Home page
        history_link = "#history-section" if current_page == "Home" else "/#history-section"
        team_link = "#team-section" if current_page == "Home" else "/#team-section"

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
                    <a href="/" class="nav-link{' active' if current_page == 'Home' else ''}" target="_self">{_t('Home')}</a>
                    <a href="/Dataset" class="nav-link{' active' if current_page == 'Dataset' else ''}" target="_self">{_t('Dataset')}</a>
                    <a href="{history_link}" class="nav-link{' active' if current_page == 'History' else ''}">{_t('History')}</a>
                    <a href="{team_link}" class="nav-link{' active' if current_page == 'Team' else ''}">{_t('Team')}</a>
                    <a href="/About" class="nav-link{' active' if current_page == 'About' else ''}" target="_self">{_t('About')}</a>
                    <a href="/Admin" class="nav-link{' active' if current_page == 'Admin' else ''}" target="_self">{_t('Admin')}</a>
                </div>

                <div class="lang-dropdown-container desktop-lang-toggle">
                    <div class="lang-btn">
                        <i class="fa-solid fa-globe"></i> {_t('Lang')} <i class="fa-solid fa-chevron-down" style="font-size: 10px; margin-left: 2px;"></i>
                    </div>
                    <div class="lang-dropdown-content">
                        <a href="?lang=en" class="lang-dropdown-item{' active-lang' if curr_lang == 'en' else ''}">English {check_icon if curr_lang == 'en' else ''}</a>
                        <a href="?lang=hi" class="lang-dropdown-item{' active-lang' if curr_lang == 'hi' else ''}">Hindi (हिंदी) {check_icon if curr_lang == 'hi' else ''}</a>
                        <a href="?lang=or" class="lang-dropdown-item{' active-lang' if curr_lang == 'or' else ''}">Odia (ଓଡ଼ିଆ) {check_icon if curr_lang == 'or' else ''}</a>
                    </div>
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
                <a href="/" class="nav-link mobile-nav-link{' active' if current_page == 'Home' else ''}" target="_self"><i class="fa-solid fa-house" style="margin-right: 8px;"></i> {_t('Home')}</a>
                <a href="/Dataset" class="nav-link mobile-nav-link{' active' if current_page == 'Dataset' else ''}" target="_self"><i class="fa-solid fa-database" style="margin-right: 8px;"></i> {_t('Dataset')}</a>
                <a href="{history_link}" class="nav-link mobile-nav-link{' active' if current_page == 'History' else ''}"><i class="fa-solid fa-clock-rotate-left" style="margin-right: 8px;"></i> {_t('History')}</a>
                <a href="{team_link}" class="nav-link mobile-nav-link{' active' if current_page == 'Team' else ''}"><i class="fa-solid fa-users" style="margin-right: 8px;"></i> {_t('Team')}</a>
                <a href="/About" class="nav-link mobile-nav-link{' active' if current_page == 'About' else ''}" target="_self"><i class="fa-solid fa-circle-info" style="margin-right: 8px;"></i> {_t('About')}</a>
                <a href="/Admin" class="nav-link mobile-nav-link{' active' if current_page == 'Admin' else ''}" target="_self"><i class="fa-solid fa-lock" style="margin-right: 8px;"></i> {_t('Admin')}</a>

                <div style="border-top: 1px solid rgba(255,255,255,0.1); margin: 4px 0;"></div>
                <div style="padding: 4px 14px 0; font-size: 13px; color: var(--leaf-muted); font-weight: 600; text-transform: uppercase;">{_t('Language')}</div>
                <div style="display: flex; flex-direction: column; gap: 4px;">
                    <a href="?lang=en" class="nav-link mobile-nav-link" style="display: flex; justify-content: space-between; align-items: center; padding: 10px 14px; font-size: 15px; {'background: rgba(34,197,94,0.15); color: #22C55E;' if st.session_state.get('lang_code', 'en') == 'en' else ''}"><span>English</span>{check_icon if st.session_state.get('lang_code', 'en') == 'en' else ''}</a>
                    <a href="?lang=hi" class="nav-link mobile-nav-link" style="display: flex; justify-content: space-between; align-items: center; padding: 10px 14px; font-size: 15px; {'background: rgba(34,197,94,0.15); color: #22C55E;' if st.session_state.get('lang_code') == 'hi' else ''}"><span>Hindi (हिंदी)</span>{check_icon if st.session_state.get('lang_code') == 'hi' else ''}</a>
                    <a href="?lang=or" class="nav-link mobile-nav-link" style="display: flex; justify-content: space-between; align-items: center; padding: 10px 14px; font-size: 15px; {'background: rgba(34,197,94,0.15); color: #22C55E;' if st.session_state.get('lang_code') == 'or' else ''}"><span>Odia (ଓଡ଼ିଆ)</span>{check_icon if st.session_state.get('lang_code') == 'or' else ''}</a>
                </div>

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
                _t("Get Started"),
                key="get_started_navbar",
                use_container_width=True,
            ):
                st.session_state.show_auth = True
                st.rerun()
        else:
            st.html('<div class="nav-btn-marker logged-in"></div>')
            if st.button(_t("Logout"), key="logout_navbar", use_container_width=True):
                st.session_state.clear()
                st.session_state.clear_cookie = True
                st.rerun()

def restore_session_if_needed():
    """Restore username/user_id/avatar into st.session_state using browser cookie/localStorage.

    This must run before require_username checks so login doesn't appear to reset on navigation.
    """
    if st.session_state.get("username"):
        return

    if st.session_state.get("_restored_session_once"):
        return

    if st.session_state.get("clear_cookie"):
        return

    # Attempt 1: server-side native cookie (if available)
    if hasattr(st, "context") and hasattr(st.context, "cookies"):
        saved_username = st.context.cookies.get("plantexa_user")
        if saved_username:
            try:
                from backend.db import get_user_by_username
                user_data = get_user_by_username(saved_username)
                if user_data:
                    st.session_state.username = saved_username
                    st.session_state.user_id = user_data.get("id")
                    st.session_state.avatar = user_data.get("avatar") or "🧑‍🌾"
                    st.session_state.last_activity = time.time()
                    st.session_state._restored_session_once = True
                    return
            except Exception:
                pass

    # Attempt 2: localStorage is synced to query params by injected JS in render_navbar,
    # so we only need to handle the query-param restore here.
    restore_user = st.query_params.get("session_restore_user")
    if restore_user and not st.session_state.get("username"):
        st.session_state.username = restore_user
        st.session_state.user_id = st.query_params.get("session_restore_id")
        st.session_state.avatar = st.query_params.get("session_restore_avatar", "🧑‍🌾")
        st.session_state.last_activity = time.time()

        if "session_restore_user" in st.query_params:
            del st.query_params["session_restore_user"]
        if "session_restore_id" in st.query_params:
            del st.query_params["session_restore_id"]
        if "session_restore_avatar" in st.query_params:
            del st.query_params["session_restore_avatar"]

        st.session_state._restored_session_once = True
        return

    st.session_state._restored_session_once = True


def require_username(force=False):
    # Always restore session first so auth does not reset on page navigation.
    restore_session_if_needed()

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
                    <h1 style="margin: 0 0 12px 0; font-family: 'Poppins', sans-serif; font-size: 32px !important; color: var(--leaf-text);">{_t('Authentication Required')}</h1>
                    <p style="margin: 0; color: var(--leaf-muted); font-size: 18px; max-width: 600px; margin-left: auto; margin-right: auto;">{_t('You must be logged in to access this page. Please use the popup to authenticate.')}</p>
                </div>
                """
            )
            st.stop()
        else:
            st.session_state.show_auth = False



def main(active_tab: str = "all"):
    if "app_lang" not in st.session_state:
        st.session_state.app_lang = "English"
    if "lang_code" not in st.session_state:
        st.session_state.lang_code = "en"

    load_css()

    render_navbar("Home")
    require_username()
    render_header()

    image_file = render_upload_section()
    render_prediction_section(image_file)

    render_history_section()

    render_tips_section()

    render_team_section()

    render_footer()
    chatbot_ui()
