import streamlit as st
import joblib
import pickle
import numpy
from catboost import CatBoostRegressor
from sklearn.preprocessing import LabelEncoder


def name_job_parse(name):
    retVal = ""
    if ("курьер" in name.lower() or "достав" in name.lower()):
        retVal += "курьер"
    elif ("экспедитор" in name.lower()):
        retVal += "экспедитор"
    elif ("кладов" in name.lower()):
        retVal += "кладовщик"

    if ("груз" in name.lower()):
        if len(retVal) != 0:
            retVal += " "
        retVal += "грузовой"

    if ("легк" in name.lower()):
        if len(retVal) != 0:
            retVal += " "
        retVal += "легковой"

    if ("на личном" in name.lower() or "на своем" in name.lower()):
        if len(retVal) != 0:
            retVal += " "
        retVal += "свое авто"

    if ("авто комп" in name.lower() or "на наше" in name.lower()):
        if len(retVal) != 0:
            retVal += " "
        retVal += "авто компании"

    if len(retVal) == 0 and "водитель" in name.lower():
        retVal = "Водитель"
    if len(retVal) == 0:
        retVal = name
    return retVal


def shedule_job_parse(text):
    retVal = ""
    time = ["5/2", "2/2", "6/1", "3/1", "4/2", "3/2"]
    for t in time:
        if t in text:

            retVal = t
    return retVal


st.title("Определение релевантности кандидата для компании \n darthhack")


col1, col2 = st.columns(2)
col1.title("Кандидат")
col2.title("Вакансия")
# должность
sex_input = col1.text_input("Пол кандидата","2")
age_input = col1.text_input("Возраст кандидата","30")
salary_input = col1.text_input("Предпологаемая зарплата","40000")
employment_input = col1.text_input("Нагрузка кандидата","Full")
shedule_input = col1.text_input("Занятость кандидата","Full")
position_input = col1.text_input("Желаемая должность кандидата","водитель")
drive_input = col1.text_input("Права кандидата","A1")
work_period_input = col1.text_input("Стаж кандидата (в месяцах)","12")
educ_num_input = col1.text_input("Количество образований","1")
works_num_input = col1.text_input("Количество прошлых работ кандидата","2")
year_educ_input = col1.text_input("Года выпуска кандидата (если много, то через запятую)","1999")
cand_region_input = col1.text_input("Регион кандидата","Москва")
work_name_input = col2.text_input("Название вакансии","Водитель")
work_region_input = col2.text_input("Регион публикации вакансии","Москва")
work_describe_input = col2.text_input("Описание вакансии","Работа водителем, москва, 5/2")


result = st.button("Посчитать релевантность")

if result:
    # with open('finalized_model.sav', 'rb') as handle:
        # model = pickle.load(handle)
    # loaded_model = joblib.load('finalized_model.sav')
    load_model = pickle.load(open("finalized_model.pkl", "rb"))
    drive_A = 0
    drive_B = 0
    drive_C = 0
    drive_D = 0
    if len(drive_input) != 0:
        drive_A = 1 if "A" in drive_input else 0
        drive_B = 1 if "B" in drive_input or "E" in drive_input else 0
        drive_C = 1 if "C" in drive_input or "E" in drive_input else 0
        drive_D = 1 if "D" in drive_input or "E" in drive_input else 0
    graphic = shedule_job_parse(str(work_describe_input))
    job_pos_name = name_job_parse(str(work_name_input))
    lst = str(year_educ_input).split(",")
    res = [eval(i) for i in lst]
    median_year = numpy.median(res)
    last_year = res[-1]
    input_data = [
        int(sex_input),int(age_input),
        int(salary_input),
        str(employment_input),
        str(shedule_input),
        str(cand_region_input),
        drive_A, drive_B, drive_C, drive_D,
        int(work_period_input),
        int(works_num_input),
        int(educ_num_input),
        median_year,
        last_year,
        str(work_region_input),
        job_pos_name,
        str(graphic)
    ]
    prediction = load_model.predict(input_data)
    if prediction > 1:
        prediction = 1
    elif prediction < 0:
        prediction = 0
    # prediction = 1
    st.write("Релевантность: ", prediction)
