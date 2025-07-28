from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models.user import User

profile_bp = Blueprint('profile', __name__)

@profile_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        current_user.name = request.form.get('name')
        current_user.company_name = request.form.get('company_name')
        current_user.employee_count = request.form.get('employee_count')
        current_user.website = request.form.get('website')
        current_user.phone_number = request.form.get('phone_number')
        
        db.session.commit()
        flash('Profile updated successfully')
        return redirect(url_for('profile.profile'))
        
    return render_template('profile/profile.html') 