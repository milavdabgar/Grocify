from flask import Blueprint

bp = Blueprint('admin', __name__)

from app.admin import (
    admin_signin, 
    admin, 
    admin_signout,
    admin_forms_product,
    admin_forms_location,
    admin_forms_other
)