import os
import logging
import datetime
import jwt
from functools import wraps

from flask import Flask, request, jsonify, g
import joblib
import numpy as np
from sqlalchemy import create_engine, Column, Integer, Float, String, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker


JWT_SECRET = "MEUSEGREDO"
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION = 3600  # 1 hour
TESTE_USERNAME = "admin"
TESTE_PASSWORD = "admin123"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DB_URL = "sqlite:///predictions.db"
engine = create_engine(DB_URL, echo=False)
Base = declarative_base()
SessionLocal = sessionmaker(bind=engine)


class Prediction(Base):
    __tablename__ = "predictions"
    id = Column(Integer, primary_key=True, autoincrement=True)
    sepal_length = Column(Float, nullable=False)
    sepal_width = Column(Float, nullable=False)
    petal_length = Column(Float, nullable=False)
    petal_width = Column(Float, nullable=False)
    predicted_class = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


Base.metadata.create_all(bind=engine)

model = joblib.load("iris_model.pkl")
logger.info("Model loaded successfully")

app = Flask(__name__)
predictions_cache = {}


def create_token(username):
    payload = {
        "username": username,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(seconds=JWT_EXPIRATION)
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("Authorization")
        if not token:
            return jsonify({"error": "Token is missing"}), 401
        try:
            if token.startswith("Bearer "):
                token = token[7:]
            data = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
            g.current_user = data["username"]
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token has expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Token is invalid"}), 401
        return f(*args, **kwargs)
    return decorated


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json(force=True)
    username = data.get("username")
    password = data.get("password")
    if username == TESTE_USERNAME and password == TESTE_PASSWORD:
        token = create_token(username)
        return jsonify({"token": token})
    else:
        return jsonify({"error": "Invalid username or password"}), 401


@app.route("/predict", methods=["POST"])
@token_required
def predict():
    try:
        data = request.get_json(force=True)
        sepal_length = data.get("sepal_length")
        sepal_width = data.get("sepal_width")
        petal_length = data.get("petal_length")
        petal_width = data.get("petal_width")
        
        if not all(isinstance(x, (int, float)) for x in [sepal_length, sepal_width, petal_length, petal_width]):
            return jsonify({"error": "Invalid input data"}), 400
        
        features = [sepal_length, sepal_width, petal_length, petal_width]
        
        # Verificar cache
        features_tuple = tuple(features)
        if features_tuple in predictions_cache:
            logger.info(f"Prediction cached for features: {features}")
            predicted_class = predictions_cache[features_tuple]
        else:
            input_data = np.array([features])
            prediction = model.predict(input_data)
            predicted_class = int(prediction[0])
            predictions_cache[features_tuple] = predicted_class
            logger.info(f"Prediction made for features: {features}")
        
        # Mapear classe numérica para nome
        class_names = {0: "setosa", 1: "versicolor", 2: "virginica"}
        predicted_class_name = class_names.get(predicted_class, "unknown")
        
        # Salvar no banco de dados
        db = SessionLocal()
        new_prediction = Prediction(
            sepal_length=sepal_length,
            sepal_width=sepal_width,
            petal_length=petal_length,
            petal_width=petal_width,
            predicted_class=predicted_class_name
        )
        db.add(new_prediction)
        db.commit()
        db.close()
        
        return jsonify({
            "predicted_class": predicted_class,
            "predicted_class_name": predicted_class_name
        })
    
    except Exception as e:
        logger.error(f"Error in prediction: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500


@app.route("/predictions", methods=["GET"])
@token_required
def list_predictions():
    limit = request.args.get("limit", 10, type=int)
    offset = request.args.get("offset", 0, type=int)
    db = SessionLocal()
    predictions = db.query(Prediction).order_by(Prediction.created_at.desc()).offset(offset).limit(limit).all()
    db.close()
    results = []
    for prediction in predictions:
        results.append({
            "id": prediction.id,
            "sepal_length": prediction.sepal_length,
            "sepal_width": prediction.sepal_width,
            "petal_length": prediction.petal_length,
            "petal_width": prediction.petal_width,
            "predicted_class": prediction.predicted_class,
            "created_at": prediction.created_at.isoformat()
        })
    return jsonify(results)


# Handler para Vercel
handler = app

if __name__ == "__main__":
    app.run(debug=True)
