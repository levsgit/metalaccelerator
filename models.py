from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class StartupApplication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Основная информация
    name = db.Column(db.String(200), nullable=False)
    short_description = db.Column(db.Text, nullable=False)
    full_description = db.Column(db.Text, nullable=False)
    market_segment = db.Column(db.String(200))
    key_technologies = db.Column(db.Text, nullable=False)
    project_stage = db.Column(db.String(100), nullable=False)
    target_market = db.Column(db.Text, nullable=False)
    competitors = db.Column(db.Text, nullable=False)
    
    # Финансы и метрики
    monthly_revenue = db.Column(db.String(100), nullable=False)
    customers_count = db.Column(db.String(100), nullable=False)
    website = db.Column(db.String(200))
    investment_request = db.Column(db.Text, nullable=False)
    
    # Контактная информация
    email = db.Column(db.String(100), nullable=False)
    leader_name = db.Column(db.String(200), nullable=False)
    telegram = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    inn = db.Column(db.String(20), nullable=False)
    source = db.Column(db.String(200), nullable=False)
    
    def to_dict(self):
        return {
            'id': self.id,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'name': self.name,
            'short_description': self.short_description,
            'full_description': self.full_description,
            'market_segment': self.market_segment,
            'key_technologies': self.key_technologies,
            'project_stage': self.project_stage,
            'target_market': self.target_market,
            'competitors': self.competitors,
            'monthly_revenue': self.monthly_revenue,
            'customers_count': self.customers_count,
            'website': self.website,
            'investment_request': self.investment_request,
            'email': self.email,
            'leader_name': self.leader_name,
            'telegram': self.telegram,
            'phone': self.phone,
            'city': self.city,
            'inn': self.inn,
            'source': self.source
        } 