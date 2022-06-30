import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

bp = Blueprint('computer', __name__, url_prefix='/a')


@bp.route('/compute', methods=('GET', 'POST'))
def register():
    return render_template("distantreps.html")
