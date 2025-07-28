from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from app import db
from app.models.campaign import Campaign, Lead
import csv
from io import StringIO

campaigns_bp = Blueprint('campaigns', __name__)

@campaigns_bp.route('/campaigns')
@login_required
def campaigns():
    user_campaigns = Campaign.query.filter_by(user_id=current_user.id).all()
    return render_template('campaigns/campaigns.html', campaigns=user_campaigns)

@campaigns_bp.route('/campaigns/new', methods=['GET', 'POST'])
@login_required
def new_campaign():
    if request.method == 'POST':
        campaign = Campaign(
            user_id=current_user.id,
            name=request.form.get('campaign_name'),
            campaign_type=request.form.get('campaign_type'),
            lead_type=request.form.get('lead_type'),
            product_name=request.form.get('product_name'),
            product_info=request.form.get('product_info'),
            main_outcome=request.form.get('main_outcome'),
            fallback_outcome=request.form.get('fallback_outcome'),
            sales_script_intro=request.form.get('sales_script_intro'),
            sales_script_opening=request.form.get('sales_script_opening'),
            sales_script_close=request.form.get('sales_script_close'),
            value_propositions=request.form.get('value_propositions'),
            known_objections=request.form.get('known_objections')
        )
        
        db.session.add(campaign)
        db.session.commit()
        
        flash('Campaign created successfully')
        return redirect(url_for('campaigns.campaigns'))
        
    return render_template('campaigns/new_campaign.html')

@campaigns_bp.route('/campaigns/<int:campaign_id>/upload-leads', methods=['POST'])
@login_required
def upload_leads(campaign_id):
    campaign = Campaign.query.get_or_404(campaign_id)
    
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
        
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
        
    if not file.filename.endswith('.csv'):
        return jsonify({'error': 'File must be CSV'}), 400
    
    try:
        stream = StringIO(file.stream.read().decode("UTF8"), newline=None)
        csv_data = csv.DictReader(stream)
        
        for row in csv_data:
            lead = Lead(
                campaign_id=campaign.id,
                company_or_individual=row['Company or Individual'],
                prospect_name=row['Prospect name'],
                company_name=row['Company name'],
                phone_number=row['phone number'],
                email=row['email'],
                company_type=row['company type']
            )
            db.session.add(lead)
            
        db.session.commit()
        return jsonify({'message': 'Leads uploaded successfully'}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400 