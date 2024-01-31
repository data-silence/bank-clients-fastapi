"""
This module contains functions for working with FastApi endpoints
"""

from .imports import pd, json, requests, StringIO, Any
from .imports import accuracy_score, precision_score, recall_score, f1_score
from .imports import ohe_enc, scaler, model_regular, model_tuned

api_url = "https://bank-clients.onrender.com/"


def get_df_from_handlers_response(handler: str) -> pd.DataFrame:
    """Converts json received from API to dataframe"""
    handler_url = f"{api_url}get/{handler}"
    response = requests.get(handler_url).json()
    json_dump = json.dumps(response)
    df = pd.read_json(StringIO(json_dump))
    return df


def get_targets_df() -> tuple[Any, pd.DataFrame, pd.DataFrame]:
    """Converts different targets json received from API to different dataframes"""
    all_df = get_df_from_handlers_response(handler="targets")
    y_test = all_df['TARGET']
    prediction_regular = pd.DataFrame({'predictions': all_df['prediction_regular'].tolist()}, index=all_df.ID)
    prediction_tuned = pd.DataFrame({'predictions': all_df['prediction_tuned'].tolist()}, index=all_df.ID)
    return y_test, prediction_regular, prediction_tuned


def get_single_frame() -> pd.DataFrame:
    """Gets a record of the selected dataframe from the temporary database"""
    df = get_df_from_handlers_response(handler="single_df")
    return df


def get_user_choise() -> dict:
    """Gets a record of the current user's selections from the database"""
    handler_url = f"{api_url}get/selected"
    response = requests.get(handler_url).json()
    return response


def get_user_selection():
    """Gets a advanced version of the current user's selections from the database"""
    user_selections = get_user_choise()
    model_type = user_selections['type_model']
    threshold = user_selections['threshold']

    model_params = get_single_model_params_dict(model_type)
    best_thr = list(model_params.values())[0]['best_thr']
    return model_type, threshold, best_thr


def get_metrics_score(y_test, y_pred) -> dict:
    """
    Computes quality metrics for the passed true class values and their predictions, and stores them in a dictionary

    :param y_test: pandas.series containing test values of targets
    :param y_pred: pandas.series containing predictions  of targets
    :return: a dictionary of quality metrics
    """

    accuracy = round(accuracy_score(y_test, y_pred), 4)
    precision = round(precision_score(y_test, y_pred), 4)
    recall = round(recall_score(y_test, y_pred), 4)
    f1 = round(f1_score(y_test, y_pred), 4)
    return {'accuracy': accuracy, 'precision': precision, 'recall': recall, 'f1': f1}


def get_metrics_score_thr() -> dict:
    """
    Computes a set of metrics for the optimal and user thresholds, returns dictionaries of the computed metrics
    """
    model_type, threshold, best_thr = get_user_selection()
    y_test, prediction_regular, prediction_tuned = get_targets_df()
    pred_probability = prediction_regular if model_type == 'regular' else prediction_tuned
    y_thr = pred_probability > threshold
    y_best_thr = pred_probability > best_thr
    metrics = {'user': get_metrics_score(y_test, y_thr), 'best': get_metrics_score(y_test, y_best_thr)}
    return metrics


def transform_df_regular_to_tuned(single_df_regular: pd.DataFrame) -> pd.DataFrame:
    """
    Transform the frame to the required format for the piplane of the customized logistic regression model
    """
    single_df_tuned = pd.DataFrame(ohe_enc.transform(single_df_regular))
    single_df_tuned = pd.DataFrame(scaler.transform(single_df_tuned), columns=single_df_tuned.columns,
                                   index=single_df_tuned.index)
    return single_df_tuned


def get_single_prediction(single_df: pd.DataFrame, threshhold: float, best_thr: float, model_type) -> \
        tuple[float, bool, bool]:
    """
    Applies trained classification models to a single user's data, organized as a dataframe, and returns a
    prediction. Depending on the model type, different preprocessing of the dataset is performed.
    """

    if model_type == 'regular':
        predict_model = model_regular
        single_pred_positive = predict_model.predict_proba(single_df)[:, 1][0]
    else:
        predict_model = model_tuned
        single_pred_positive = predict_model.predict_proba(single_df)[:, 1][0]
    is_recommend_thr = single_pred_positive >= threshhold
    is_recommend_best_thr = single_pred_positive >= best_thr

    return single_pred_positive, is_recommend_thr, is_recommend_best_thr


def get_single_model_params_dict(model_name: str) -> dict:
    """Fetches the parameters of a specific model from the database"""
    handler_url = f"{api_url}{model_name}/params"
    model_params_dict = requests.get(handler_url).json()
    return model_params_dict
