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
                elif 0.0 < float(row[i]) < 0.4:
                    dict_name1[i]['Неудовлетворительно'] += 1
                elif 0.4 <= float(row[i]) < 0.6:
                    dict_name1[i]['Удовлетворительно'] += 1
                elif 0.6 <= float(row[i]) < 0.8:
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
    course_dict = {'ENGM': 'инженерная механика',
                   'METR': 'основы метрологии, стандартизация и оценка соответствия',
                   'GEOM': 'начертательная геометрия и инженерная графика',
                   'TEPL': 'теплотехника',
                   'CALC': 'математический анализ',
                   'ARCHC': 'основы архитектуры и строительных конструкций',
                   'ELB': 'основы электротехники и электроники',
                   'SMNGM': 'самоменеджмент',
                   'TRIZ': 'теория решения изобретательских задач',
                   'TECO': 'технологии конструкционных материалов',
                   'PHILS': 'философия и история науки и техники',
                   'RUBSCULT': 'культура русской деловой речи',
                   'ECOS': 'системная динамика устойчивого развития (Системная экология)',
                   'ELECD': 'электродинамика',
                   'CSHARP': 'программирование на с#',
                   'PRGRMM': 'технологии программирования',
                   'INTPR': 'управление интеллектуальной собственностью',
                   'PHILSCI': 'философия и методология науки',
                   'INTROBE': 'введение в биологию и экологию',
                   'CHEMSO': 'введение в химические источники тока',
                   'INFENG': 'информационные сервисы в управлении инженерной деятельностью',
                   'METHODS': 'методы анализа и прогнозирования временных рядов',
                   'BIOECO': 'основные концепции биологии и экологии',
                   'SYSTENG': 'практики системной инженерии',
                   'ECOEFF': 'основы экономической эффективности производства',
                   'DATAINF': 'методы доступа к данным и информационного поиска',
                   'TELECOM': 'беспроводные телекоммуникационные системы',
                   'SIGPROC': 'основы цифровой обработки сигналов',
                   'EDUBASE': 'основы педагогической деятельности',
                   }

    data_list = file_name.split(sep='_')
    final_list = list()
    final_list.append(course_dict[data_list[1]].lower())                                    # название курса
    final_list.append((data_list[2] + '_' + data_list[3]).lower())                          # сессия курса
    data_list = data_list[-1].split(sep='-')
    data_report = date(int(data_list[0]), int(data_list[1]), int(data_list[2]))             # создаем объект Date
    final_list.append(data_report)
    return final_list
