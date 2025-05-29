from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from werkzeug.utils import secure_filename
import os
import logging
from models import db, StartupApplication

# Настройка логирования
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'  # Замените на реальный секретный ключ
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///startups.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/uploads'

# Создаем папку для загрузок, если её нет
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

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

if __name__ == '__main__':
    app.run(debug=True) 