import requests
import json
import base64
import secrets

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel
from sqlalchemy.orm import sessionmaker

from database_setup import SecretData, engine


app = FastAPI()
security = HTTPBasic()
DBSession = sessionmaker(bind=engine)
session = DBSession()


class ResultIn(BaseModel):
    name: str
    repo_url: str
    result: list[str]


def get_authorization_header(username: str = 'qummy', password: str = 'GiVEmYsecReT!') -> dict[str, str]:
    auth = base64.b64encode(f'{username}:{password}'.encode()).decode("ascii")
    return {
        'Authorization': f'Basic {auth}',
        'Content-Type': 'application/json'
    }


def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, "qummy")
    correct_password = secrets.compare_digest(credentials.password, "GiVEmYsecReT!")
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username


@app.get('/api/get_secret_data', status_code=201, response_model=list[str])
def get_secret_data(credentials: HTTPBasicCredentials = Depends(get_current_username)):
    headers = get_authorization_header()
    response_json = requests.request("GET", 'http://yarlikvid.ru:9999/api/top-secret-data', headers=headers)
    response = json.loads(response_json.text)
    for mes in response:
        row = SecretData(encrypted_text=mes)
        session.add(row)
    session.commit()
    return response


@app.post('/api/decrypt_secret_data', status_code=201, response_model=list[str])
def decrypt_secret_data(credentials: HTTPBasicCredentials = Depends(get_current_username)):
    all_row = session.query(SecretData).all()
    first_id = all_row[0].id
    list_of_encrypted_data = []
    for row in all_row:
        list_of_encrypted_data.append(row.encrypted_text)
    payload = json.dumps(list_of_encrypted_data)

    headers = get_authorization_header()

    response = requests.request("POST", "http://yarlikvid.ru:9999/api/decrypt", headers=headers, data=payload)
    message = json.loads(response.text)
    for mes in message:
        row = session.query(SecretData).filter(SecretData.id == first_id).first()
        row.decrypted_text = mes
        first_id += 1
    session.commit()
    return message


@app.post('/api/send_result', response_model=ResultIn, description='Отправить результат.')
def result_request(credentials: HTTPBasicCredentials = Depends(get_current_username)):
    all_row = session.query(SecretData).all()
    list_of_decrypted_data = []
    for row in all_row:
        list_of_decrypted_data.append(row.decrypted_text)
    payload = ResultIn(
        name='Андреев Стас',
        repo_url='https://github.com/lifest01/fastapi-docker',
        result=list_of_decrypted_data
    )
    headers = get_authorization_header()
    response = requests.request("POST", "http://yarlikvid.ru:9999/api/result", headers=headers, data=payload)

    return payload
