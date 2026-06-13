# TODO

## Auth reset fix (session drops on navigation)
- [x] Ensure session restoration runs early on every rerun in `frontend/ui.py` (`restore_session_if_needed()` at start of `render_navbar`).
- [x] Consolidate query-param auth handling by calling `_handle_auth_query_params()` from inside `render_navbar`.
- [ ] Next: verify pages consistently call `render_navbar()` + `require_username()` and do not clear `st.session_state` unexpectedly.
- [ ] Next: review the inactivity timeout behavior (`require_username` clears session after 30 minutes) and make it configurable / disable for debugging.
- [ ] Next: fix duplicate/restored auth logic so we don’t rely on `st.query_params` + JS routing simultaneously.

## Quick test checklist
1. Login → navigate to Dataset/History/Profile → confirm username persists.
2. Refresh browser tab → confirm username persists.
3. Wait ~30 minutes (or shorten timer for test) → confirm expected logout/reauth behavior.

