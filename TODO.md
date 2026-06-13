# TODO - Get Started / Logout toggle

## Step 1
- Update `frontend/ui.py` to add a toggle-style button in the navbar:
  - Logged out: show button text **"Get Started"**.
  - Logged in: show **"Logout"**.
- Ensure only button text/content and logout theme color are changed (red theme for logout).

## Step 2
- Keep existing login flow (`require_username()`) intact.

## Step 3
- Verify app renders correctly on desktop:
  - Logged out user sees Get Started button.
  - Clicking it triggers the authentication UI (or sets `st.session_state.show_auth=True`).
  - Logged in user sees red Logout button.

