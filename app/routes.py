from app import app, db
import os
from flask import render_template, flash, redirect, url_for, request
from . import analytic_grade as ag
from app.forms import LoginForm, RegistrationForm, GradeReportForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, GradeReport
from werkzeug.urls import url_parse
from werkzeug.utils import secure_filename


@app.route('/')
@app.route('/index')
@login_required
def index():
    posts = [
        {'author': {'username': 'Hinahin', 'age': '23'},
         'text': 'Это небольшой сервис для обработки выгрузок с оценками'
         },
    ]
    return render_template('index.html', title='My site', posts=posts)


@app.route('/chart/<int:report_id>')
@login_required
def chart(report_id):
    report = GradeReport.query.filter_by(id=report_id).first_or_404()

    categories = ag.name_from_str(report.tests_names)
    excellent = ag.grade_from_str(report.a_grade)
    good = ag.grade_from_str(report.b_grade)
    bad = ag.grade_from_str(report.c_grade)
    fail = ag.grade_from_str(report.f_grade)
    x_title = report.course_name
    title = 'Chart'

    return render_template('chart.html',
                           categories=categories,
                           excellent=excellent,
                           good=good,
                           bad=bad,
                           fail=fail,
                           x_title=x_title,
                           title=title,
                           )


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data.lower()).first()
        if user is None or not user.check_password(form.password.data):
            flash('Промазал. Попробуй еще раз.', 'warning')
            return redirect(url_for('index'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/reg_on_flask', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User()
        user.username = form.username.data.lower()
        user.email = form.email.data.lower()
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Поздравляем с успешной регистрацией!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/add_report', methods=['GET', 'POST'])
def add_report():
    form = GradeReportForm()
    if form.validate_on_submit():
        report = GradeReport()

        file_report = secure_filename(form.file_report.data.filename)   # получаем имя файла
        file_dir = os.path.join(app.root_path, 'uploads', file_report)  # получаем путь для сохранения
        form.file_report.data.save(file_dir)                            # сохраняем файл

        try:
            data_list = ag.data_from_filename(file_report)

            report.course_name = data_list[0]           # Название курса
            report.session_course = data_list[1]        # Название сессии
            report.date_report = data_list[2]           # Дата выгрузки объект Date, не строка
        except:
            flash('Неправильное имя файла', 'danger')
            os.remove(file_dir)
            return redirect(url_for('add_report'))

        try:
            grade_dict = ag.fillinig_dict(os.path.join(app.root_path, 'uploads', file_report))
            categories = []
            excellent = []
            good = []
            bad = []
            fail = []
            for test in grade_dict.keys():
                categories.append(test)
                excellent.append(grade_dict[test]['Отлично'])
                good.append(grade_dict[test]['Хорошо'])
                bad.append(grade_dict[test]['Удовлетворительно'])
                fail.append(grade_dict[test]['Неудовлетворительно'])

            report.tests_names = str(categories)
            report.a_grade = str(excellent)
            report.b_grade = str(good)
            report.c_grade = str(bad)
            report.f_grade = str(fail)
        except:
            flash('Нарушена структура файла', 'danger')
            os.remove(file_dir)
            return redirect(url_for('add_report'))

        report.user_id = current_user.id

        db.session.add(report)
        db.session.commit()

        flash('Данные успешно добавлены', 'success')
        return redirect(url_for('reports'))

    return render_template('add_report.html', title='Добавить отчет', form=form)


@app.route('/reports/')
@login_required
def reports():
    reports_per_page = 10
    q = request.args.get('q')
    page = request.args.get('page')

    if page and page.isdigit():
        page = int(page)
    else:
        page = 1

    if q:
        q = q.lower()
        my_reports = GradeReport.query.filter(GradeReport.course_name.contains(q) |
                                              GradeReport.session_course.contains(q)).orede_by(GradeReport.date_report.desc())
    else:
        my_reports = GradeReport.query.order_by(GradeReport.date_creation.desc())

    page_reports = my_reports.paginate(page, reports_per_page, False)

    return render_template('reports.html', reports=page_reports)


@app.route('/del_nah_report/<int:report_id>')
@login_required
def del_report(report_id):
    report = GradeReport.query.filter_by(id=report_id).first_or_404()
    db.session.delete(report)
    db.session.commit()
    flash('Запись успешно удалена', 'success')
    return redirect(url_for('reports'))
