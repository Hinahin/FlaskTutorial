import csv
from datetime import date


def stud_counts(file_name):
    with open(file_name, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        st_count = 0
        st_vf = 0
        st_st = 0
        for row in reader:
            st_count += 1
            if row['Enrollment Track'] == 'verified':
                st_vf += 1
            if row['Cohort Name'] != 'Default Group' and\
                    row['Cohort Name'] != 'verified' and\
                    row['Cohort Name'] != 'Группа по умолчанию':   # or 'verified' or 'Группа по умолчанию'
                st_st += 1

        # print('Количество слушателей на курсе:', st_count)
        # print('Количество слушателей на треке с прокторингом:', st_vf)
        # print('Количество студентов УрФУ:', st_st)

        return [st_count, st_vf, st_st]


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


def data_from_filename(file_name):

    # urfu_INTROBE_spring_2018_grade_report_2018-07-03-0643.csv
    # urfu_Inclus_M1_fall_2019_test_grade_report_2020-02-03-0713.csv
    data_list = file_name.split(sep='_')
    final_list = list()
    if data_list[2] == "spring" or data_list[2] == "fall":
        final_list.append(data_list[1].lower())  # шифр курса
        final_list.append((data_list[2] + '_' + data_list[3]).lower())  # сессия курса
        data_list = data_list[-1].split(sep='-')
        data_report = date(int(data_list[0]), int(data_list[1]), int(data_list[2]))  # создаем объект Date
        final_list.append(data_report)
    elif data_list[3] == "spring" or data_list[3] == "fall":
        final_list.append(data_list[1].lower() + "_" + data_list[2].lower())  # шифр курса
        final_list.append((data_list[3] + '_' + data_list[4]).lower())  # сессия курса
        data_list = data_list[-1].split(sep='-')
        data_report = date(int(data_list[0]), int(data_list[1]), int(data_list[2]))  # создаем объект Date
        final_list.append(data_report)

    return final_list

# stud_counts('engm.csv')