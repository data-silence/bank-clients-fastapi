"""
Entry point for streamlit application Banks Cients
Contains sequences functions to draw Bank Clients app interface
"""

import streamlit as st

st.set_page_config(
    layout="wide",
    initial_sidebar_state="auto",
    page_title="Banks Clients EDA and prediction",
    page_icon='💰',
)

# set_page_config goes before importing from eda module due to streamlit library requirements.
from tab_eda import draw_barchart, draw_pie, draw_num_distribution, draw_categorical_distribution, \
    draw_nun_distribution, draw_pearson_correlation, draw_target_correlation
from tab_preds import (draw_model_select, draw_thrash_select, draw_metrics, draw_confusion_matrix,
                       draw_choise_df, draw_custom_df)


def process_main_page() -> None:
    """
    Sets the required structure of elements arrangement on the main page of the application
    """
    st.title('Изучение клиентов банка и предсказание их поведения с помощью ML')
    st.image('https://github.com/data-silence/banks-clients/blob/master/img/bgr.png?raw=true', use_column_width='auto',
             caption='Исследуем данные, предсказываем готовность клиентов к сотрудничеству: enjoy-ds@pm.me')
    tab_eda, tab_preds = st.tabs(["Анализ", "Прогнозы"])

    with tab_eda:
        st.header("Exploratory Data Analysis")
        draw_barchart()
        draw_pie()
        draw_num_distribution()
        draw_categorical_distribution()
        draw_nun_distribution()
        draw_pearson_correlation()
        draw_target_correlation()

    with tab_preds:
        st.header('Предсказываем поведение клиентов')
        draw_model_select()
        draw_thrash_select()
        draw_metrics()
        draw_confusion_matrix()
        draw_choise_df()
        draw_custom_df()


if __name__ == '__main__':
    process_main_page()
