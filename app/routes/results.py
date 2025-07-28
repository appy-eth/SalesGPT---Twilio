from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.models.campaign import Campaign, Lead
from sqlalchemy import func

results_bp = Blueprint('results', __name__)

@results_bp.route('/results')
@login_required
def results():
    # Get all campaigns for the current user
    campaigns = Campaign.query.filter_by(user_id=current_user.id).all()
    
    # Calculate campaign statistics
    campaign_stats = []
    for campaign in campaigns:
        total_leads = Lead.query.filter_by(campaign_id=campaign.id).count()
        contacted_leads = Lead.query.filter_by(campaign_id=campaign.id, status='called').count()
        meetings = Lead.query.filter_by(campaign_id=campaign.id, outcome='book meeting').count()
        emails = Lead.query.filter_by(campaign_id=campaign.id, outcome='send more info').count()
        
        stats = {
            'campaign': campaign,
            'total_leads': total_leads,
            'contacted_percentage': (contacted_leads / total_leads * 100) if total_leads > 0 else 0,
            'meetings': meetings,
            'emails': emails
        }
        campaign_stats.append(stats)
    
    # Get all leads for the current user
    leads = Lead.query.join(Campaign).filter(Campaign.user_id == current_user.id).all()
    
    return render_template('results/results.html', 
                         campaign_stats=campaign_stats,
                         leads=leads) 