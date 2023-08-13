from flask import Blueprint, session, redirect, url_for

bp = Blueprint('signout', __name__)

@bp.route('/signout')
def signout():
    # Clear the session
    session.clear()

    # Redirect to the sign-in page
    return redirect(url_for('signin.signin'))
