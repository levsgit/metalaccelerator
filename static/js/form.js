document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('.startup-form');
    const submitButton = form.querySelector('.cta-button');
    const hintsContainer = form.querySelector('.form-hints');
    const requiredFields = form.querySelectorAll('[required]');
    
    // Объект для хранения подсказок
    const fieldLabels = {
        name: 'Название',
        short_description: 'Короткое описание',
        full_description: 'Полное описание',
        key_technologies: 'Ключевые технологии',
        project_stage: 'Стадия проекта',
        target_market: 'Целевой рынок',
        competitors: 'Конкуренты',
        monthly_revenue: 'Среднемесячная выручка',
        customers_count: 'Количество клиентов',
        investment_request: 'Инвестиционный запрос',
        email: 'Email',
        leader_name: 'ФИО лидера',
        telegram: 'Telegram',
        phone: 'Телефон',
        city: 'Город',
        inn: 'ИНН',
        source: 'Источник информации'
    };

    // Функция для проверки заполнения всех полей
    function checkFormValidity() {
        let isValid = true;
        const emptyFields = [];

        requiredFields.forEach(field => {
            if (!field.value.trim()) {
                isValid = false;
                emptyFields.push({
                    id: field.id,
                    label: fieldLabels[field.id]
                });
            }
        });

        // Обновляем состояние кнопки
        submitButton.disabled = !isValid;

        // Обновляем подсказки
        updateHints(emptyFields);
    }

    // Функция для обновления подсказок
    function updateHints(emptyFields) {
        hintsContainer.innerHTML = '';
        
        if (emptyFields.length > 0) {
            const hintText = document.createElement('p');
            hintText.textContent = 'Заполните обязательные поля: ';
            hintsContainer.appendChild(hintText);

            emptyFields.forEach((field) => {
                const hint = document.createElement('span');
                hint.className = 'form-hint';
                hint.textContent = field.label;
                hint.onclick = () => {
                    const targetField = document.getElementById(field.id);
                    targetField.focus();
                    targetField.scrollIntoView({ behavior: 'smooth', block: 'center' });
                };

                hintsContainer.appendChild(hint);
                hintsContainer.appendChild(document.createTextNode(' '));
            });
        }
    }

    // Добавляем обработчики событий для всех полей
    requiredFields.forEach(field => {
        field.addEventListener('input', checkFormValidity);
        field.addEventListener('change', checkFormValidity);
    });

    // Проверяем форму при загрузке
    checkFormValidity();

    // Обработка отправки формы
    form.addEventListener('submit', function(e) {
        if (!submitButton.disabled) {
            return true;
        }
        e.preventDefault();
    });
}); 