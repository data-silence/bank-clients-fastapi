"""
This is Fast API app for BankClients application: https://banks-clients.streamlit.app
Contains app endpoints
"""

from fastapi import FastAPI, Depends, status

from sqlalchemy.orm import Session

from .models import Base, TableClient, TableY, SingleClientTable, TableSelectedModel
from .schemas import Client, Y, ModelNames, ClientShort, SelectedModel
from .db import SessionLocal, engine
from .imports import models_schema, pd, ohe_enc, scaler, model_regular, model_tuned
from .scripts import transform_df_regular_to_tuned, get_single_prediction, get_single_frame, \
    get_metrics_score_thr, get_user_selection

Base.metadata.create_all(bind=engine)

app = FastAPI()

api_url = "http://127.0.0.1:8000/"


def get_session() -> None:
    """Manages connection sessions for working with the database"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def root():
    """Returns greeting during root user request"""
    return {"message": "This is API for BankClients application: https://banks-clients.streamlit.app/"}


@app.get("/get/clients", response_model=list[Client])
def get_clients(db: Session = Depends(get_session)):
    """Get all clients in the database"""
    return db.query(TableClient).all()


@app.get("/get/targets", response_model=list[Y])
def get_target(db: Session = Depends(get_session)):
    """Get all predictions in the database"""
    return db.query(TableY).all()


@app.get("/get/single_df", response_model=list[ClientShort])
def get_single_df(db: Session = Depends(get_session)):
    """Get single client record in the database"""
    return db.query(SingleClientTable).all()


@app.get("/get/selected", response_model=SelectedModel)
def get_selected_options(db: Session = Depends(get_session)):
    """Get user selected options"""
    return db.query(TableSelectedModel).first()


@app.patch("/update/selected/model_name", response_model=SelectedModel)
def update_selected_by_model_type(model_name: ModelNames, db: Session = Depends(get_session)):
    """Updates information about the User's selected model"""
    updated_selected = db.query(TableSelectedModel).first()
    if updated_selected and updated_selected.type_model != model_name:
        updated_selected.type_model = model_name
        db.add(updated_selected)
        db.commit()
        db.refresh(updated_selected)

    return updated_selected


@app.patch("/update/selected/threshold", response_model=SelectedModel)
def update_selected_by_threshold(threshold: float, db: Session = Depends(get_session)):
    """Updates information about the User's selected threshold"""
    updated_selected = db.query(TableSelectedModel).first()
    if updated_selected and updated_selected.threshold != threshold:
        updated_selected.threshold = threshold
        db.add(updated_selected)
        db.commit()
        db.refresh(updated_selected)

    return updated_selected


@app.get("/get/user_params", response_model=dict)
def get_user_params():
    """Get user selectioned params"""
    model_type, threshold, best_thr = get_user_selection()

    user_params_dict = {
        'model_type': model_type,
        'threshold': threshold,
        'best_thr': best_thr
    }

    return user_params_dict


@app.get("/get/predictions", response_model=dict)
def get_predict():
    """Get single client record in the database"""
    single_df = get_single_frame()
    single_df = single_df.reset_index(drop=True).set_index('ID')
    single_df_regular = single_df.iloc[0].to_frame().T

    model_type, threshold, best_thr = get_user_selection()

    match model_type:
        case 'regular':
            single_pred, is_recommend_thr, is_recommend_best_thr = get_single_prediction(single_df_regular, threshold,
                                                                                         best_thr, model_type)
        case 'tuned':
            single_df_tuned = transform_df_regular_to_tuned(single_df_regular=single_df_regular)
            single_pred, is_recommend_thr, is_recommend_best_thr = get_single_prediction(single_df_tuned, threshold,
                                                                                         best_thr, model_type)
    answers_dict = {
        'single_pred': single_pred,
        'is_recommend_thr': int(is_recommend_thr),
        'is_recommend_best_thr': int(is_recommend_best_thr)
    }

    return answers_dict


@app.get("/get/metrics_score", response_model=dict)
def get_metrics():
    """Get metrics score for current user selection or db state"""
    metrics = get_metrics_score_thr()
    return metrics


@app.get("/{model_name}/params", response_model=dict)
def get_model_params(model_name: ModelNames):
    """Get model params"""
    model_name_rus = models_schema[model_name]['russian_name']
    model_type = models_schema[model_name]['type']
    params = models_schema[model_name]['params']
    best_thr = models_schema[model_name]['best_thr']

    model_params_dict = {
        model_name_rus:
            {
                'type': model_name,
                'params': params,
                'name': model_type,
                'best_thr': best_thr
            }
    }

    return model_params_dict


@app.post("/{model_name}/fit")
def fit_models(model_name: str, fit_data: list[Client]) -> str:
    """Fit models"""
    fit_df = pd.DataFrame([i.fit_data.model_dump() for i in fit_data])
    X = fit_df.drop(columns=['TARGET', 'AGREEMENT_RK']).reset_index(drop=True).set_index('ID')
    y = fit_df.TARGET
    X = pd.DataFrame(ohe_enc.transform(X), index=X.index)
    X = pd.DataFrame(scaler.fit_transform(X), columns=X.columns, index=X.index)
    match model_name:
        case 'regular':
            model_regular.fit(X, y)
        case 'tuned':
            model_tuned.fit(X, y)
    return 'Success'


@app.post("/write/single_df", response_model=ClientShort)
def write_single_df_to_db(single_df_dict: ClientShort, db: Session = Depends(get_session)):
    """Takes a single frame as a dictionary and writes it to the temporary database"""
    data_dict = SingleClientTable(**single_df_dict.model_dump())
    db.add(data_dict)
    db.commit()
    db.refresh(data_dict)
    return data_dict


@app.delete("/delete/single_df", status_code=status.HTTP_204_NO_CONTENT)
def delete_single_df(db: Session = Depends(get_session)):
    """Deletes a single frame from temporary database after usage"""
    single_df = db.query(SingleClientTable).first()
    if single_df:
        db.delete(single_df)
        db.commit()
    return None


if __name__ == "__main__":
    pass
