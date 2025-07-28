from app import db
from datetime import datetime

class Campaign(db.Model):
    __tablename__ = 'campaigns'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    campaign_type = db.Column(db.String(20), nullable=False)  # inbound or outbound
    lead_type = db.Column(db.String(20), nullable=False)  # warm or cold
    product_name = db.Column(db.String(100))
    product_info = db.Column(db.Text)
    main_outcome = db.Column(db.String(50))
    fallback_outcome = db.Column(db.String(50))
    sales_script_intro = db.Column(db.Text)
    sales_script_opening = db.Column(db.Text)
    sales_script_close = db.Column(db.Text)
    value_propositions = db.Column(db.Text)
    known_objections = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='draft')  # draft, active, completed
    
    # Relationships
    leads = db.relationship('Lead', backref='campaign', lazy=True)
    
    def __repr__(self):
        return f'<Campaign {self.name}>'

class Lead(db.Model):
    __tablename__ = 'leads'
    
    id = db.Column(db.Integer, primary_key=True)
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaigns.id'), nullable=False)
    company_or_individual = db.Column(db.String(100))
    prospect_name = db.Column(db.String(100))
    company_name = db.Column(db.String(100))
    phone_number = db.Column(db.String(20))
    email = db.Column(db.String(120))
    company_type = db.Column(db.String(50))
    status = db.Column(db.String(20), default='new')  # new, called, converted, failed
    call_transcript = db.Column(db.Text)
    outcome = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_contacted = db.Column(db.DateTime)
    
    def __repr__(self):
        return f'<Lead {self.prospect_name}>' 