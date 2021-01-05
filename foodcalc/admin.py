from flask import redirect, url_for, request
from flask_security import current_user
from flask_admin.contrib.sqla import ModelView


class SecureModelView(ModelView):
    """A secured model-view."""

    def is_accessible(self):
        """Check the current user is logged in."""
        return current_user.has_role('admin')

    def inaccessible_callback(self, name, **kwargs):
        """Redirect to login page."""
        return redirect(url_for('security.login', next=request.url))
