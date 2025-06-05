from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from werkzeug.utils import secure_filename
import os
import logging
from models import db, StartupApplication, User, Tag
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from dotenv import load_dotenv

# Настройка логирования
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key-here')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/uploads'

# Создаем папку для загрузок, если её нет
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Добавляем фильтр для форматирования валюты
@app.template_filter('format_currency')
def format_currency(value):
    try:
        return "{:,.0f}".format(float(value))
    except (ValueError, TypeError):
        return "0"

with app.app_context():
    db.create_all()
    
    # Create test investor
    investor = User.query.filter_by(email='investor@example.com').first()
    if not investor:
        investor = User(
            email='investor@example.com',
            user_type='investor'
        )
        investor.set_password('investor')
        db.session.add(investor)
    
    # Sample startup data
    sample_startups = [
        {
            'name': 'GreenMetall',
            'short_description': 'Инновационная технология переработки металлических отходов с использованием AI',
            'full_description': 'Разработка системы автоматической сортировки и переработки металлических отходов с использованием искусственного интеллекта',
            'market_segment': 'metallurgy',
            'key_technologies': 'AI, Computer Vision, Robotics',
            'project_stage': 'MVP',
            'target_market': 'Металлургические предприятия, перерабатывающие заводы',
            'competitors': 'Традиционные методы переработки',
            'monthly_revenue': '0',
            'customers_count': '2',
            'website': 'https://greenmetall.example.com',
            'investment_request': 'Разработка промышленного прототипа',
            'email': 'contact@greenmetall.example.com',
            'leader_name': 'Иван Петров',
            'telegram': '@greenmetall',
            'phone': '+7 (999) 123-45-67',
            'city': 'Москва',
            'inn': '1234567890',
            'source': 'Собственная разработка',
            'investment_amount': 1000000,
            'investment_raised': 250000,
            'geography': 'moscow',
            'tags': ['зеленая металлургия', 'AI', 'переработка']
        },
        {
            'name': 'SmartSteel',
            'short_description': 'Система контроля качества металлопроката на основе компьютерного зрения',
            'full_description': 'Разработка системы автоматического контроля качества металлопроката с использованием компьютерного зрения и машинного обучения',
            'market_segment': 'metallurgy',
            'key_technologies': 'Computer Vision, ML, IoT',
            'project_stage': 'working_product',
            'target_market': 'Металлургические комбинаты',
            'competitors': 'Ручной контроль качества',
            'monthly_revenue': '50000',
            'customers_count': '3',
            'website': 'https://smartsteel.example.com',
            'investment_request': 'Масштабирование на новые производства',
            'email': 'info@smartsteel.example.com',
            'leader_name': 'Анна Сидорова',
            'telegram': '@smartsteel',
            'phone': '+7 (999) 234-56-78',
            'city': 'Санкт-Петербург',
            'inn': '2345678901',
            'source': 'Университетский проект',
            'investment_amount': 2000000,
            'investment_raised': 1000000,
            'geography': 'spb',
            'tags': ['контроль качества', 'AI', 'металлургия']
        },
        {
            'name': 'EcoMetal',
            'short_description': 'Экологичная технология производства стали с нулевым выбросом CO2',
            'full_description': 'Разработка инновационной технологии производства стали с использованием водорода вместо угля',
            'market_segment': 'metallurgy',
            'key_technologies': 'Водородная энергетика, IoT',
            'project_stage': 'idea',
            'target_market': 'Крупные металлургические предприятия',
            'competitors': 'Традиционное производство стали',
            'monthly_revenue': '0',
            'customers_count': '0',
            'website': 'https://ecometal.example.com',
            'investment_request': 'Разработка пилотного проекта',
            'email': 'contact@ecometal.example.com',
            'leader_name': 'Петр Иванов',
            'telegram': '@ecometal',
            'phone': '+7 (999) 345-67-89',
            'city': 'Екатеринбург',
            'inn': '3456789012',
            'source': 'Исследовательский институт',
            'investment_amount': 5000000,
            'investment_raised': 0,
            'geography': 'other',
            'tags': ['зеленая металлургия', 'водород', 'экология']
        },
        {
            'name': 'MetalAI',
            'short_description': 'AI-система оптимизации металлургического производства',
            'full_description': 'Разработка системы искусственного интеллекта для оптимизации параметров металлургического производства',
            'market_segment': 'metallurgy',
            'key_technologies': 'AI, ML, Big Data',
            'project_stage': 'MVP',
            'target_market': 'Металлургические предприятия',
            'competitors': 'Традиционные системы управления',
            'monthly_revenue': '100000',
            'customers_count': '5',
            'website': 'https://metalai.example.com',
            'investment_request': 'Разработка новых модулей',
            'email': 'info@metalai.example.com',
            'leader_name': 'Сергей Смирнов',
            'telegram': '@metalai',
            'phone': '+7 (999) 456-78-90',
            'city': 'Москва',
            'inn': '4567890123',
            'source': 'Стартап-студия',
            'investment_amount': 1500000,
            'investment_raised': 750000,
            'geography': 'moscow',
            'tags': ['AI', 'оптимизация', 'металлургия']
        },
        {
            'name': 'RecycleTech',
            'short_description': 'Инновационная технология переработки металлических отходов',
            'full_description': 'Разработка эффективной технологии переработки сложных металлических отходов',
            'market_segment': 'recycling',
            'key_technologies': 'Химия, Физика, IoT',
            'project_stage': 'working_product',
            'target_market': 'Перерабатывающие предприятия',
            'competitors': 'Традиционные методы переработки',
            'monthly_revenue': '200000',
            'customers_count': '8',
            'website': 'https://recycletech.example.com',
            'investment_request': 'Расширение производства',
            'email': 'contact@recycletech.example.com',
            'leader_name': 'Мария Кузнецова',
            'telegram': '@recycletech',
            'phone': '+7 (999) 567-89-01',
            'city': 'Санкт-Петербург',
            'inn': '5678901234',
            'source': 'Технопарк',
            'investment_amount': 3000000,
            'investment_raised': 2000000,
            'geography': 'spb',
            'tags': ['переработка', 'экология', 'металлы']
        },
        {
            'name': 'NewMaterials',
            'short_description': 'Разработка новых композитных материалов для металлургии',
            'full_description': 'Создание инновационных композитных материалов с улучшенными характеристиками для металлургической промышленности',
            'market_segment': 'new_materials',
            'key_technologies': 'Материаловедение, Нанотехнологии',
            'project_stage': 'idea',
            'target_market': 'Металлургические предприятия',
            'competitors': 'Традиционные материалы',
            'monthly_revenue': '0',
            'customers_count': '0',
            'website': 'https://newmaterials.example.com',
            'investment_request': 'Лабораторные исследования',
            'email': 'info@newmaterials.example.com',
            'leader_name': 'Алексей Новиков',
            'telegram': '@newmaterials',
            'phone': '+7 (999) 678-90-12',
            'city': 'Новосибирск',
            'inn': '6789012345',
            'source': 'Академический институт',
            'investment_amount': 800000,
            'investment_raised': 0,
            'geography': 'other',
            'tags': ['новые материалы', 'композиты', 'инновации']
        },
        {
            'name': 'SmartFoundry',
            'short_description': 'Умная система управления литейным производством',
            'full_description': 'Разработка интеллектуальной системы управления литейным производством с использованием IoT и AI',
            'market_segment': 'metallurgy',
            'key_technologies': 'IoT, AI, Big Data',
            'project_stage': 'MVP',
            'target_market': 'Литейные производства',
            'competitors': 'Традиционные системы управления',
            'monthly_revenue': '75000',
            'customers_count': '4',
            'website': 'https://smartfoundry.example.com',
            'investment_request': 'Разработка новых модулей',
            'email': 'contact@smartfoundry.example.com',
            'leader_name': 'Дмитрий Волков',
            'telegram': '@smartfoundry',
            'phone': '+7 (999) 789-01-23',
            'city': 'Москва',
            'inn': '7890123456',
            'source': 'Индустриальный партнер',
            'investment_amount': 1200000,
            'investment_raised': 600000,
            'geography': 'moscow',
            'tags': ['литейное производство', 'IoT', 'AI']
        },
        {
            'name': 'EcoRecycle',
            'short_description': 'Экологичная переработка металлических отходов',
            'full_description': 'Разработка экологически чистой технологии переработки металлических отходов',
            'market_segment': 'recycling',
            'key_technologies': 'Химия, Экология, IoT',
            'project_stage': 'working_product',
            'target_market': 'Перерабатывающие предприятия',
            'competitors': 'Традиционные методы переработки',
            'monthly_revenue': '150000',
            'customers_count': '6',
            'website': 'https://ecorecycle.example.com',
            'investment_request': 'Масштабирование производства',
            'email': 'info@ecorecycle.example.com',
            'leader_name': 'Елена Соколова',
            'telegram': '@ecorecycle',
            'phone': '+7 (999) 890-12-34',
            'city': 'Санкт-Петербург',
            'inn': '8901234567',
            'source': 'Эко-инкубатор',
            'investment_amount': 2500000,
            'investment_raised': 1500000,
            'geography': 'spb',
            'tags': ['переработка', 'экология', 'металлы']
        },
        {
            'name': 'MetalTech',
            'short_description': 'Инновационные технологии обработки металлов',
            'full_description': 'Разработка новых технологий обработки металлов с использованием лазерных технологий',
            'market_segment': 'metallurgy',
            'key_technologies': 'Лазерные технологии, Робототехника',
            'project_stage': 'idea',
            'target_market': 'Металлообрабатывающие предприятия',
            'competitors': 'Традиционные методы обработки',
            'monthly_revenue': '0',
            'customers_count': '0',
            'website': 'https://metaltech.example.com',
            'investment_request': 'Разработка прототипа',
            'email': 'contact@metaltech.example.com',
            'leader_name': 'Николай Морозов',
            'telegram': '@metaltech',
            'phone': '+7 (999) 901-23-45',
            'city': 'Казань',
            'inn': '9012345678',
            'source': 'Технопарк',
            'investment_amount': 1800000,
            'investment_raised': 0,
            'geography': 'other',
            'tags': ['обработка металлов', 'лазерные технологии', 'робототехника']
        },
        {
            'name': 'SmartAlloy',
            'short_description': 'Разработка умных сплавов с программируемыми свойствами',
            'full_description': 'Создание новых сплавов с программируемыми свойствами для различных отраслей промышленности',
            'market_segment': 'new_materials',
            'key_technologies': 'Материаловедение, AI',
            'project_stage': 'MVP',
            'target_market': 'Металлургические предприятия',
            'competitors': 'Традиционные сплавы',
            'monthly_revenue': '50000',
            'customers_count': '3',
            'website': 'https://smartalloy.example.com',
            'investment_request': 'Разработка новых составов',
            'email': 'info@smartalloy.example.com',
            'leader_name': 'Андрей Семенов',
            'telegram': '@smartalloy',
            'phone': '+7 (999) 012-34-56',
            'city': 'Москва',
            'inn': '0123456789',
            'source': 'Исследовательский центр',
            'investment_amount': 2200000,
            'investment_raised': 1100000,
            'geography': 'moscow',
            'tags': ['новые материалы', 'сплавы', 'инновации']
        }
    ]
    
    # Create startups
    for startup_data in sample_startups:
        # Check if startup already exists
        existing_startup = StartupApplication.query.filter_by(name=startup_data['name']).first()
        if not existing_startup:
            # Create tags
            tags = []
            for tag_name in startup_data.pop('tags'):
                tag = Tag.query.filter_by(name=tag_name).first()
                if not tag:
                    tag = Tag(name=tag_name)
                    db.session.add(tag)
                tags.append(tag)
            
            # Create startup
            startup = StartupApplication(**startup_data)
            startup.tags = tags
            db.session.add(startup)
    
    db.session.commit()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        if current_user.user_type == 'investor':
            return redirect(url_for('startup_catalog'))
        return redirect(url_for('index'))
        
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        # First try to find an investor
        user = User.query.filter_by(email=email, user_type='investor').first()
        
        # If not found, try to find a startup
        if not user:
            user = User.query.filter_by(email=email, user_type='startup').first()
        
        if user and user.check_password(password):
            login_user(user)
            if user.user_type == 'investor':
                return redirect(url_for('startup_catalog'))
            return redirect(url_for('index'))
        else:
            flash('Неверный email или пароль. Пожалуйста, проверьте введенные данные.', 'error')
            
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
        
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user_type = request.form.get('user_type')
        
        if User.query.filter_by(email=email).first():
            flash('Пользователь с таким email уже существует', 'error')
            return redirect(url_for('register'))
            
        user = User(email=email, user_type=user_type)
        user.set_password(password)
        
        if user_type == 'startup':
            user.startup_name = request.form.get('startup_name')
            user.startup_description = request.form.get('startup_description')
        else:
            user.investor_name = request.form.get('investor_name')
            user.investor_company = request.form.get('investor_company')
            
        db.session.add(user)
        db.session.commit()
        
        login_user(user)
        return redirect(url_for('index'))
        
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/apply', methods=['GET', 'POST'])
def apply():
    if request.method == 'POST':
        try:
            # Логируем полученные данные
            logger.debug("Received form data: %s", request.form)
            
            # Проверяем наличие всех необходимых полей
            required_fields = [
                'name', 'short_description', 'full_description', 'key_technologies',
                'project_stage', 'target_market', 'competitors', 'monthly_revenue',
                'customers_count', 'investment_request', 'email', 'leader_name',
                'telegram', 'phone', 'city', 'inn', 'source'
            ]
            
            for field in required_fields:
                if field not in request.form or not request.form[field].strip():
                    raise ValueError(f"Missing required field: {field}")

            # Создание новой заявки
            application = StartupApplication(
                name=request.form['name'].strip(),
                short_description=request.form['short_description'].strip(),
                full_description=request.form['full_description'].strip(),
                market_segment=request.form.get('market_segment', '').strip(),
                key_technologies=request.form['key_technologies'].strip(),
                project_stage=request.form['project_stage'].strip(),
                target_market=request.form['target_market'].strip(),
                competitors=request.form['competitors'].strip(),
                monthly_revenue=request.form['monthly_revenue'].strip(),
                customers_count=request.form['customers_count'].strip(),
                website=request.form.get('website', '').strip(),
                investment_request=request.form['investment_request'].strip(),
                email=request.form['email'].strip(),
                leader_name=request.form['leader_name'].strip(),
                telegram=request.form['telegram'].strip(),
                phone=request.form['phone'].strip(),
                city=request.form['city'].strip(),
                inn=request.form['inn'].strip(),
                source=request.form['source'].strip()
            )

            db.session.add(application)
            db.session.commit()
            logger.info("Application successfully saved to database")

            flash('Спасибо за вашу заявку! Мы рассмотрим её и свяжемся с вами в ближайшее время.', 'success')
            return redirect(url_for('apply'))
        except ValueError as ve:
            logger.error("Validation error: %s", str(ve))
            flash(f'Ошибка в данных формы: {str(ve)}', 'error')
            return redirect(url_for('apply'))
        except Exception as e:
            logger.error("Error saving application: %s", str(e), exc_info=True)
            flash('Произошла ошибка при отправке заявки. Пожалуйста, попробуйте снова.', 'error')
            return redirect(url_for('apply'))

    return render_template('apply.html')

@app.route('/applications')
def applications():
    applications = StartupApplication.query.order_by(StartupApplication.created_at.desc()).all()
    return render_template('applications.html', applications=applications)

@app.route('/startup-catalog')
@login_required
def startup_catalog():
    if current_user.user_type != 'investor':
        flash('Доступ к каталогу стартапов разрешен только инвесторам', 'error')
        return redirect(url_for('index'))
    
    startups = StartupApplication.query.all()
    return render_template('startup_catalog.html', startups=startups)

@app.route('/startup/<int:startup_id>')
@login_required
def startup_detail(startup_id):
    if current_user.user_type != 'investor':
        flash('Доступ к деталям стартапов разрешен только инвесторам', 'error')
        return redirect(url_for('index'))
    
    startup = StartupApplication.query.get_or_404(startup_id)
    return render_template('startup_detail.html', startup=startup)

@app.route('/api/startups/filter')
@login_required
def filter_startups():
    if current_user.user_type != 'investor':
        return jsonify({'error': 'Unauthorized'}), 403
    
    stage = request.args.get('stage')
    niche = request.args.get('niche')
    investment = request.args.get('investment')
    geography = request.args.get('geography')
    
    query = StartupApplication.query
    
    if stage:
        query = query.filter(StartupApplication.project_stage == stage)
    if niche:
        query = query.filter(StartupApplication.market_segment == niche)
    if geography:
        query = query.filter(StartupApplication.geography == geography)
    if investment:
        min_amount, max_amount = map(float, investment.split('-'))
        query = query.filter(StartupApplication.investment_amount >= min_amount)
        if max_amount:
            query = query.filter(StartupApplication.investment_amount <= max_amount)
    
    startups = query.all()
    return jsonify([startup.to_dict() for startup in startups])

if __name__ == '__main__':
    app.run(debug=True) 