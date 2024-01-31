"""
Module responsible for content and display of the "Прогнозы" tab in streamlit application
"""

from imports import st, pd, choice, confusion_matrix
from imports import y_test, models_params, df
from scripts import get_metrics_score, update_threshold, update_model_name, get_user_params_dict, get_thresh_preds, \
    write_single_dict_to_db, get_prediction, erase_singl_df


def draw_model_select() -> None:
    """
    Responsible for displaying the predictive model selection box
    """
    st.divider()
    st.info('Постановка задачи: выявить для Банка-заказчика как можно больше потенциальных клиентов его '
            'будущих продуктов. Для минимизации расходов сделать это с максимально возможной точностью.')
    st.caption('Возможной целью такой задачи является формирование перечня получателей рекламных звонков о новом '
               'продукте Банка')
    st.divider()
    st.subheader('🔎 Выбор модели')
    st.info('Выбери предсказательную модель (они имеют разные особенности и дают разный прогноз)')
    model_name = st.radio(
        "",
        [name.title() for name in models_params],
        captions=[(models_params[name]['name'] + ': ' + models_params[name]['params']) for name in models_params],
        horizontal=True
    )
    model_type = models_params[model_name.lower()]['type']
    update_model_name(model_type)


def draw_thrash_select() -> None:
    """
    Responsible for displaying items by selecting a probability threshold
    """
    user_params_dict = get_user_params_dict()
    best_thr = user_params_dict['best_thr']
    st.divider()
    st.subheader('🎚️ Выбор порога')
    st.info('Продемонстрируем влияние выбранного вероятностного порога на точность определения поведения клиентов')
    st.write('')
    thr_prob = st.slider('Выбери порог (шкала приведена в проценты для удобства, правильно указывать в диапазоне '
                         'от 0 до 1):', min_value=0, max_value=100, value=50, step=1)
    thr = round((thr_prob / 100), 2)
    update_threshold(thr)
    st.write(
        "Мы подобрали для этой модели оптимальный порог для достижения максимальной точности при соблюдении заданной "
        "полноты охвата, он составляет",
        best_thr)
    st.write("Вы выбрали порог", thr)


def draw_metrics() -> None:
    """
    Responsible for displaying the calculated quality metrics and comparing them to a benchmark
    """
    st.divider()
    st.subheader('⛳ Влияние порога на метрики качества')
    st.info(
        f'Посмотрим как изменяется качество метрик для выбранного вами порога по сравнению с эталонным решением:')
    metrics = get_metrics_score()
    col1, col2, col3, col4 = st.columns(4)
    mets_name = list(metrics['user'].keys())
    pairs = zip(mets_name, [col1, col2, col3, col4])

    for mets, col in pairs:
        col.metric(mets, metrics['user'][mets], round((metrics['user'][mets] - metrics['best'][mets]), 4))
    st.caption(
        'Но что значат эти цифры на практике?')


def draw_confusion_matrix() -> None:
    """
    Responsible for building the confusion matrix based on user and reference thresholds
    """
    y_thr_tuple = get_thresh_preds()

    st.divider()
    st.subheader('🫰 Влияние порога на затраты Банка')
    st.info('Продемонстрируем влияние выбранного порога на практические аспекты реальной жизни')

    col1, col2 = st.columns(2)
    pairs = zip([0, 1], ['тобой', 'нами'], [col1, col2])

    for thr_num, me, col in pairs:
        matrix = pd.DataFrame(confusion_matrix(y_test, y_thr_tuple[thr_num]))
        st.write(f'Это результат подобранного {me} порога:')
        st.dataframe(matrix.style.background_gradient(cmap='YlGnBu', axis=None))
        st.write(f'Здесь удастся правильно дозвониться {matrix[1][1]} клиентам, но мы не сделаем необходимые '
                 f'звонки {matrix[0][1]} потенциальным клиентам')
    matrix_user = confusion_matrix(y_test, y_thr_tuple[0])[1][1] + confusion_matrix(y_test, y_thr_tuple[0])[0][1]
    matrix_tuned = confusion_matrix(y_test, y_thr_tuple[1])[1][1] + confusion_matrix(y_test, y_thr_tuple[1])[0][1]
    delta = round(matrix_tuned / matrix_user, 1)
    st.write(f'Правильная для поставленной задачи тонкая настройка порога имеет свою материальную цену: нам придётся '
             f'заставить колл-центр Банка обзванивать в {delta} раз больше клиентов. Поэтому придётся считать, '
             f'что выгоднее: упустить потенциальных клиентов и недополучить доход, или нарастить себестоимость за счет '
             f'увеличения оплаты колл-центру')


def draw_forecast() -> None:
    """
    Calculates predictions for a randomly selected random user and displays them
    """

    single_pred, is_recommend_thr, is_recommend_best_thr = get_prediction()
    erase_singl_df()

    st.write('Вероятность сотрудничества этого клиента согласно прогноза модели:', round(single_pred, 2))
    text_best_thr = 'Целесообразность отработки данного клиента согласно настроенного порога:'
    text_thr = 'Целесообразность отработки данного клиента согласно установленного тобой порога:'

    if is_recommend_thr:
        st.write(text_thr, ':green[необходимо отработать]')
    else:
        st.write(text_thr, ':red[не трать время]')

    if is_recommend_best_thr:
        st.write(text_best_thr, ':green[необходимо отработать]')
    else:
        st.write(text_best_thr, ':red[не трать время]')


def draw_choise_df() -> None:
    """
    Provides selection and display of data from a random user of the Bank
    """
    st.divider()
    st.subheader('1️⃣ Влияние порога на единичный прогноз')

    X = df.drop(columns=['TARGET', 'AGREEMENT_RK']).reset_index(drop=True).set_index('ID')
    st.info('Нажми кнопку и выбери случайного клиента, изучи полученные результаты')
    result = st.button('Жми')
    if result:
        ind = choice(X.index.tolist())
        single_df_regular = X.loc[ind].to_frame().T
    else:
        single_df_regular = X.iloc[0].to_frame().T
    # draw the resulting dataframe in the application
    st.dataframe(single_df_regular)

    # transforming df into dict to write into temporary db
    temp_single_df = single_df_regular.iloc[0].to_frame().T
    temp_single_df.index.rename('ID', inplace=True)
    single_df_dict = temp_single_df.reset_index().to_dict(orient='records')[0]
    write_single_dict_to_db(single_df_dict)

    # calculate forecasts based on temp records in the database and draw them in the application
    draw_forecast()


def collect_dataframe() -> pd.DataFrame:
    """
    Provides input of user questionnaire data to build a customized forecast and turns it into a dataframe
    """
    with st.expander('Разверни кат для ввода анкеты'):
        st.subheader('Общие сведения о клиенте:')
        GENDER = st.radio("Пол", ("Мужской", "Женский"), horizontal=True)
        AGE = st.slider("Возраст", min_value=1, max_value=80, value=39, step=1)
        FACT_ADDRESS_PROVINCE = st.selectbox("Регион проживания", tuple(df.FACT_ADDRESS_PROVINCE.unique().tolist()))
        EDUCATION = st.radio("Образование", tuple(df.EDUCATION.unique().tolist()), horizontal=True)
        SOCSTATUS_WORK_FL = st.radio("Наличие работы", ("Есть", "Нет"), horizontal=True)
        SOCSTATUS_PENS_FL = st.radio("Наличие пенсии", ("Есть", "Нет"), horizontal=True)

        st.divider()
        st.subheader('Сведения о семье:')
        MARITAL_STATUS = st.radio("Семейное положение:", tuple(df.MARITAL_STATUS.unique().tolist()), horizontal=True)
        CHILD_TOTAL = st.slider("Количество детей", min_value=0, max_value=10, value=2, step=1)
        DEPENDANTS = st.slider("Количество иждивенцев", min_value=0, max_value=10, value=1, step=1)

        st.divider()
        st.subheader('Сведения о работе:')
        GEN_INDUSTRY = st.selectbox("Отрасль", tuple(df.GEN_INDUSTRY.unique().tolist()))
        JOB_DIR = st.selectbox("Направление работы", tuple(df.JOB_DIR.unique().tolist()))
        GEN_TITLE = st.selectbox("Должность", tuple(df.GEN_TITLE.unique().tolist()))
        WORK_TIME = st.number_input("Время работы в текущей должности, мес", value=36)

        st.divider()
        st.subheader('Сведения о доходах:')
        PERSONAL_INCOME = st.slider("Личный доход", min_value=0, max_value=300_000, value=15_000, step=1)
        FAMILY_INCOME = st.radio("Доход семьи", tuple(df.FAMILY_INCOME.unique().tolist()), horizontal=True)
        FL_PRESENCE_FL = st.radio("Наличие квартиры", ("Есть", "Нет"), horizontal=True)
        OWN_AUTO = st.radio("Количество автомобилей в семье", tuple(df.OWN_AUTO.unique().tolist()), horizontal=True)

        st.divider()
        st.subheader('Сведения о кредите:')
        CREDIT = st.slider("Размер кредита", min_value=1_000, max_value=100_000, value=15_000, step=1)
        TERM = st.slider("Срок кредита, мес", min_value=1, max_value=36, value=8, step=1)
        FST_PAYMENT = st.slider("Размер первоначального взноса, в % от суммы кредита", min_value=1, max_value=100,
                                value=23, step=1) * CREDIT / 100

    translatetion = {
        "Мужской": 1,
        "Женский": 0,
        "Есть": 1,
        'Нет': 0,
    }

    custom_dict = {
        "AGE": AGE,
        "GENDER": translatetion[GENDER],
        "EDUCATION": EDUCATION,
        "MARITAL_STATUS": MARITAL_STATUS,
        "CHILD_TOTAL": CHILD_TOTAL,
        "DEPENDANTS": DEPENDANTS,
        "SOCSTATUS_WORK_FL": translatetion[SOCSTATUS_WORK_FL],
        "SOCSTATUS_PENS_FL": translatetion[SOCSTATUS_PENS_FL],
        "FACT_ADDRESS_PROVINCE": FACT_ADDRESS_PROVINCE,
        "FL_PRESENCE_FL": translatetion[FL_PRESENCE_FL],
        "OWN_AUTO": OWN_AUTO,
        "CREDIT": CREDIT,
        "TERM": TERM,
        "FST_PAYMENT": FST_PAYMENT,
        "GEN_INDUSTRY": GEN_INDUSTRY,
        "GEN_TITLE": GEN_TITLE,
        "JOB_DIR": JOB_DIR,
        "WORK_TIME": WORK_TIME,
        "FAMILY_INCOME": FAMILY_INCOME,
        "PERSONAL_INCOME": PERSONAL_INCOME,
    }
    # build a dataframe from the dictionary to display in the application
    result_df = pd.DataFrame(custom_dict, index=[0])

    # The id-extended dictionary is used to record a single record into the temporary database for forecast calculation
    custom_dict["ID"] = 0
    write_single_dict_to_db(custom_dict)

    return result_df


def draw_custom_df() -> None:
    """
    Displays the custom user inputs and predict results for him
    """
    st.divider()
    st.header('🥅 Кастомный прогноз')
    st.info('Заполни анкету виртуального клиента и получи наш прогноз о его готовности сотрудничать с Банком.')

    # collect and draw the dataframe in a separate function collect_dataframe
    result_df_regular = collect_dataframe()
    st.caption('Полученный портрет клиента:')
    st.dataframe(result_df_regular)

    # calculate forecasts based on temp records in the database and draw them in the application
    draw_forecast()
