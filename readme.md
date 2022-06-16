## Информация

- Фреймворк: fastapi
- База данных: SQLite.
- ORM: SQLAlchemy.

## Как запустить?
 - Убедитесь что установлен `docker` и `docker-compose`
 - Выполнить `docker-compose up`
 
## Документация API:
Для выполнения запросов нужно быть авторизованным
```
username: qummy
password: GiVEmYsecReT!
```
```json
{
  "openapi": "3.0.2",
  "info": {
    "title": "FastAPI",
    "version": "0.1.0"
  },
  "paths": {
    "/api/get_secret_data": {
      "get": {
        "summary": "Get Secret Data",
        "operationId": "get_secret_data_api_get_secret_data_get",
        "responses": {
          "201": {
            "description": "Successful Response",
            "content": {
              "application/json": {
                "schema": {
                  "title": "Response Get Secret Data Api Get Secret Data Get",
                  "type": "array",
                  "items": {
                    "type": "string"
                  }
                }
              }
            }
          }
        },
        "security": [
          {
            "HTTPBasic": [ ]
          }
        ]
      }
    },
    "/api/decrypt_secret_data": {
      "post": {
        "summary": "Decrypt Secret Data",
        "operationId": "decrypt_secret_data_api_decrypt_secret_data_post",
        "responses": {
          "201": {
            "description": "Successful Response",
            "content": {
              "application/json": {
                "schema": {
                  "title": "Response Decrypt Secret Data Api Decrypt Secret Data Post",
                  "type": "array",
                  "items": {
                    "type": "string"
                  }
                }
              }
            }
          }
        },
        "security": [
          {
            "HTTPBasic": [ ]
          }
        ]
      }
    },
    "/api/send_result": {
      "post": {
        "summary": "Result Request",
        "description": "Отправить результат.",
        "operationId": "result_request_api_send_result_post",
        "responses": {
          "200": {
            "description": "Successful Response",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/ResultIn"
                }
              }
            }
          }
        },
        "security": [
          {
            "HTTPBasic": [ ]
          }
        ]
      }
    }
  },
  "components": {
    "schemas": {
      "ResultIn": {
        "title": "ResultIn",
        "required": [
            "name",
            "repo_url",
            "result"
        ],
        "type": "object",
        "properties": {
          "name": {
            "title": "Name",
            "type": "string"
          },
          "repo_url": {
            "title": "Repo Url",
            "type": "string"
          },
          "result": {
            "title": "Result",
            "type": "array",
            "items": {
              "type": "string"
            }
          }
        }
      }
    },
    "securitySchemes": {
      "HTTPBasic": {
        "type": "http",
        "scheme": "basic"
      }
    }
  }
}
```