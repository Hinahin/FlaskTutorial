import csv
from datetime import date


def get_empty_dict(file_name):
    with open(file_name, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        row = next(reader)
        if 'Grade' in row:
            start_col = row.index('Grade')
        else:
            start_col = row.index('grade')
        # start_col = row.index('Grade')
        if 'Cohort Name' in row:
            end_col = row.index('Cohort Name')
        else:
            end_col = row.index('Enrollment Track')
        course_dict = {}
        for i in range(start_col, end_col):
            if row[i] == 'Grade Percent' or 'Avg' in row[i] or 'None' in row[i]:
                continue
            else:
                course_dict[row[i]] = {
                    'Не приступал': 0,
                    'Неудовлетворительно': 0,
                    'Удовлетворительно': 0,
                    'Хорошо': 0,
                    'Отлично': 0,
            }
    return course_dict


def fillinig_dict(file_name, dict_name='none'):
    if dict_name == 'none':
        dict_name1 = get_empty_dict(file_name)
    else:
        dict_name1 = dict_name

    with open(file_name, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            for i in dict_name1:
                if row[i] == 'Not Available' or row[i] == 'Not Attempted' or row[i] == 'None':
                    dict_name1[i]['Не приступал'] -= 1
                elif float(row[i]) > 0.0 and float(row[i]) < 0.4:
                    dict_name1[i]['Неудовлетворительно'] += 1
                elif float(row[i]) >= 0.4 and float(row[i]) < 0.6:
                    dict_name1[i]['Удовлетворительно'] += 1
                elif float(row[i]) >= 0.6 and float(row[i]) < 0.8:
                    dict_name1[i]['Хорошо'] += 1
                elif float(row[i]) >= 0.8:
                    dict_name1[i]['Отлично'] += 1
        return dict_name1


def name_from_str(str_list):
    new_str = str_list[1:-1]
    new_list = new_str.split(sep=', ')
    final_list = []

    for name in new_list:
        final_list.append(name[1:-1])

    return final_list


def grade_from_str(str_list):
    new_str = str_list[1:-1]
    new_list = new_str.split(sep=', ')
    final_list = []

    for name in new_list:
        final_list.append(int(name))

    return final_list


# urfu_INTROBE_spring_2018_grade_report_2018-07-03-0643.csv
def data_from_filename(file_name):
    course_dict = {'ENGM': 'Инженерная механика',
                   'METR': 'Основы метрологии, стандартизация и оценка соответствия',
                   'GEOM': 'Начертательная геометрия и инженерная графика',
                   'TEPL': 'Теплотехника',
                   'CALC': 'Математический анализ',
                   'ARCHC': 'Основы архитектуры и строительных конструкций',
                   'ELB': 'Основы электротехники и электроники',
                   'SMNGM': 'Самоменеджмент',
                   'TRIZ': 'Теория решения изобретательских задач',
                   'TECO': 'Технологии конструкционных материалов',
                   'PHILS': 'Философия и история науки и техники',
                   'RUBSCULT': 'Культура русской деловой речи',
                   'ECOS': 'Системная динамика устойчивого развития (Системная экология)',
                   'ELECD': 'Электродинамика',
                   'CSHARP': 'Программирование на C#',
                   'PRGRMM': 'Технологии программирования',
                   'INTPR': 'Управление интеллектуальной собственностью',
                   'PHILSCI': 'Философия и методология науки',
                   'INTROBE': 'Введение в биологию и экологию',
                   'CHEMSO': 'Введение в химические источники тока',
                   'INFENG': 'Информационные сервисы в управлении инженерной деятельностью',
                   'METHODS': 'Методы анализа и прогнозирования временных рядов',
                   'BIOECO': 'Основные концепции биологии и экологии',
                   'SYSTENG': 'Практики системной инженерии',
                   'ECOEFF': 'Основы экономической эффективности производства',
                   'DATAINF': 'Методы доступа к данным и информационного поиска',
                   'TELECOM': 'Беспроводные телекоммуникационные системы',
                   'SIGPROC': 'Основы цифровой обработки сигналов',
                   'EDUBASE': 'Основы педагогической деятельности',
                   }

    data_list = file_name.split(sep='_')
    final_list = list()
    final_list.append(course_dict[data_list[1]])                                    # название курса
    final_list.append(data_list[2] + '_' + data_list[3])                            # сессия курса
    data_list = data_list[-1].split(sep='-')
    data_report = date(int(data_list[0]), int(data_list[1]), int(data_list[2]))
    final_list.append(data_report)
    return final_list

