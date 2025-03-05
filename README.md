# Setup Environments

## Python

> Install Python from **[python.org](https://www.python.org/downloads/)**

### Virtual Environment

- Setup Virtual Environment

```bash
python -m venv $(VENV_NAME)
```

- Activate Virtual Environment

```bash
source $(PATH_TO_BIN)/activate
```

- Deactivate Virtual Environment

```bash
deactivate
```

### Dependencies

- Export Dependencies to requirements.txt

```bash
pip freeze > $(FILENAME)
```

- Install Dependencies in requirements.txt

```bash
pip install -r $(FILENAME)
```

### Alembic

디비를 처음 생성하거나 업데이트 사항이 있을경우

```bash
alembic revision --autogenerate -m "message" # SQL 자동 생성 // DB 갱신은 별도로 진행
```

```bash
alembic upgrade head   # 가장 최신 버전으로 DB를 갱신
alembic downgrade base # 가장 예전 버전으로 DB를 갱신
```

### Run

```bash
fastapi dev
```
