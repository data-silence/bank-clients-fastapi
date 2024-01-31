"""
Module contains functions to work with API endpoints
"""

from imports import st, pd, json, requests, StringIO, Any

api_url = "http://127.0.0.1:8000/"


@st.cache_data
def get_df_from_handlers_response(handler: str) -> pd.DataFrame:
    """Converts json received from API to dataframe"""
    handler_url = f"{api_url}get/{handler}"
    response = requests.get(handler_url).json()
    json_dump = json.dumps(response)
    df = pd.read_json(StringIO(json_dump))
    return df


@st.cache_data
def get_clients_df() -> pd.DataFrame:
    """Converts clients json received from API to dataframe"""
    df = get_df_from_handlers_response(handler="clients")
    return df


@st.cache_data
def get_targets_df() -> tuple[Any, pd.DataFrame, pd.DataFrame]:
    """Converts different targets json received from API to different dataframes"""
    all_df = get_df_from_handlers_response(handler="targets")
    y_test = all_df['TARGET']
    prediction_regular = pd.DataFrame({'predictions': all_df['prediction_regular'].tolist()}, index=all_df.ID)
    prediction_tuned = pd.DataFrame({'predictions': all_df['prediction_tuned'].tolist()}, index=all_df.ID)
    return y_test, prediction_regular, prediction_tuned


def get_single_model_params_dict(model_name: str) -> dict:
    """Gets the parameters of the selected model"""
    handler_url = f"{api_url}{model_name}/params"
    model_params_dict = requests.get(handler_url).json()
    return model_params_dict


def get_user_params_dict() -> dict:
    """Gets the dict of user parameters"""
    handler_url = f"{api_url}get/user_params"
    model_params_dict = requests.get(handler_url).json()
    return model_params_dict


def get_thresh_preds() -> tuple[bool, bool]:
    """Gives the results of applying models on optimal and user thresholds"""
    user_params_dict = get_user_params_dict()
    model_type = user_params_dict['model_type']
    threshold = user_params_dict['threshold']
    best_thr = user_params_dict['best_thr']

    _, prediction_regular, prediction_tuned = get_targets_df()

    pred_probability = prediction_regular if model_type == 'regular' else prediction_tuned
    y_thr = pred_probability > threshold
    y_best_thr = pred_probability > best_thr
    y_thr_tuple = (y_thr, y_best_thr)

    return y_thr_tuple


def get_all_models_params_dict() -> dict:
    """Gets the common dict of model's parameters"""
    models = {}
    models.update(get_single_model_params_dict('regular'))
    models.update(get_single_model_params_dict('tuned'))
    return models


def get_metrics_score():
    """Get metrics score for chosen model and threshold"""
    handler_url = f"{api_url}get/metrics_score"
    response = requests.get(handler_url).json()
    return response


def get_prediction() -> tuple[float, bool, bool]:
    """Gets the model prediction for selected params"""
    handler_url = f"{api_url}get/predictions"
    response = requests.get(handler_url).json()
    single_pred = response['single_pred']
    is_recommend_thr = bool(response['is_recommend_thr'])
    is_recommend_best_thr = bool(response['is_recommend_best_thr'])
    return single_pred, is_recommend_thr, is_recommend_best_thr


def update_model_name(new_value) -> dict:
    """Updates the selected model - makes a record to db"""
    handler_url = f"{api_url}update/selected/model_name?model_name={new_value}"
    response = requests.patch(handler_url).json()
    return response


def update_threshold(new_value) -> dict:
    """Updates the selected threshold - makes a record to db"""
    handler_url = f"{api_url}update/selected/threshold?threshold={new_value}"
    response = requests.patch(handler_url).json()
    return response


def write_single_dict_to_db(single_dict) -> None:
    """Write the selected dict dataframe to temporary db"""
    handler_url = f"{api_url}write/single_df"
    requests.post(handler_url, json=single_dict)
    return None


def erase_singl_df() -> None:
    """Erase records from temporary db after work with it"""
    handler_url = f"{api_url}delete/single_df"
    requests.delete(handler_url)
    return None


if __name__ == "__main__":
    pass
