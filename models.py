from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()

# Association table for startup tags
startup_tags = db.Table('startup_tags',
    db.Column('startup_id', db.Integer, db.ForeignKey('startup_application.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True)
)

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    
    def __repr__(self):
        return f'<Tag {self.name}>'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    user_type = db.Column(db.String(20), nullable=False)  # 'investor' or 'startup'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.email}>'

class StartupApplication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Основная информация
    name = db.Column(db.String(200), nullable=False)
    short_description = db.Column(db.Text, nullable=False)
    full_description = db.Column(db.Text, nullable=False)
    market_segment = db.Column(db.String(200))
    key_technologies = db.Column(db.Text, nullable=False)
    project_stage = db.Column(db.String(100), nullable=False)  # idea, MVP, working product
    target_market = db.Column(db.Text, nullable=False)
    competitors = db.Column(db.Text, nullable=False)
    
    # Финансы и метрики
    monthly_revenue = db.Column(db.String(100), nullable=False)
    customers_count = db.Column(db.String(100), nullable=False)
    website = db.Column(db.String(200))
    investment_request = db.Column(db.Text, nullable=False)
    investment_amount = db.Column(db.Float, nullable=False)  # Required investment amount
    investment_raised = db.Column(db.Float, default=0.0)  # Amount raised so far
    
    # Контактная информация
    email = db.Column(db.String(100), nullable=False)
    leader_name = db.Column(db.String(200), nullable=False)
    telegram = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    inn = db.Column(db.String(20), nullable=False)
    source = db.Column(db.String(200), nullable=False)
    
    # Additional fields for catalog
    logo_url = db.Column(db.String(500))  # URL to startup logo
    geography = db.Column(db.String(200))  # Geographic location
    tags = db.relationship('Tag', secondary=startup_tags, lazy='subquery',
                          backref=db.backref('startups', lazy=True))
    
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
            'investment_amount': self.investment_amount,
            'investment_raised': self.investment_raised,
            'email': self.email,
            'leader_name': self.leader_name,
            'telegram': self.telegram,
            'phone': self.phone,
            'city': self.city,
            'inn': self.inn,
            'source': self.source,
            'logo_url': self.logo_url,
            'geography': self.geography,
            'tags': [tag.name for tag in self.tags]
        } 