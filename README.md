# oshaberi-web-backend
Windowsの例で記載

## 環境構築
```
> python -m venv venv
> .\venv\Scripts\activate
> pip install -r requirements.txt
```

## 開発環境の起動
```
python main.py
```

## 本番環境の起動
```
> uvicorn main:app --host=0.0.0.0
```
