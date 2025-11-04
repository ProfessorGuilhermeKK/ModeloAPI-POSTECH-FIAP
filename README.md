# 🌸 API de Classificação de Flores Iris com Machine Learning

API REST desenvolvida em Flask para classificação de flores Iris usando Machine Learning. O projeto inclui autenticação JWT, cache de predições e persistência de dados em SQLite.

## 📋 Índice

- [Sobre o Projeto](#sobre-o-projeto)
- [Tecnologias](#tecnologias)
- [Funcionalidades](#funcionalidades)
- [Pré-requisitos](#pré-requisitos)
- [Instalação](#instalação)
- [Uso](#uso)
- [Endpoints](#endpoints)
- [Exemplos de Uso](#exemplos-de-uso)
- [Estrutura do Projeto](#estrutura-do-projeto)

## 🎯 Sobre o Projeto

Este projeto implementa uma API REST para classificação de flores Iris usando Regressão Logística. O modelo é treinado com o dataset Iris clássico e pode prever três espécies diferentes:
- **Setosa** (classe 0)
- **Versicolor** (classe 1)
- **Virginica** (classe 2)

A API inclui:
- Autenticação JWT para segurança
- Cache de predições para melhor performance
- Persistência de todas as predições no banco de dados
- Logging de operações

## 🛠 Tecnologias

- **Python 3.x**
- **Flask** - Framework web
- **Scikit-learn** - Machine Learning
- **SQLAlchemy** - ORM para banco de dados
- **PyJWT** - Autenticação JWT
- **NumPy** - Operações numéricas
- **Joblib** - Serialização de modelos
- **SQLite** - Banco de dados

## ✨ Funcionalidades

- ✅ Treinamento de modelo de classificação Iris
- ✅ API REST com autenticação JWT
- ✅ Predição de espécies de flores Iris
- ✅ Cache de predições para otimização
- ✅ Histórico de predições no banco de dados
- ✅ Logging de operações

## 📦 Pré-requisitos

- Python 3.7 ou superior
- pip (gerenciador de pacotes Python)

## 🚀 Instalação

1. **Clone o repositório:**
```bash
git clone https://github.com/seu-usuario/nome-do-repositorio.git
cd nome-do-repositorio
```

2. **Crie um ambiente virtual (recomendado):**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

3. **Instale as dependências:**
```bash
pip install -r requirements.txt
```

4. **Adicione também o scikit-learn:**
```bash
pip install scikit-learn
```

## 📝 Uso

### 1. Treinar o Modelo

Primeiro, treine o modelo executando:

```bash
python petals.py
```

Isso irá:
- Carregar o dataset Iris
- Treinar o modelo de Regressão Logística
- Exibir a acurácia do modelo
- Salvar o modelo em `iris_model.pkl`

### 2. Iniciar a API

Execute o servidor Flask:

```bash
python api.py
```

A API estará disponível em `http://localhost:5000`

## 🔌 Endpoints

### POST `/login`
Autentica o usuário e retorna um token JWT.

**Request Body:**
```json
{
  "username": "admin",
  "password": "admin123"
}
```

**Response:**
```json
{
  "token": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### POST `/predict`
Faz a predição da espécie de flor Iris baseada nas características fornecidas.

**Headers:**
```
Authorization: Bearer <token>
Content-Type: application/json
```

**Request Body:**
```json
{
  "sepal_length": 5.1,
  "sepal_width": 3.5,
  "petal_length": 1.4,
  "petal_width": 0.2
}
```

**Response:**
```json
{
  "predicted_class": 0,
  "predicted_class_name": "setosa"
}
```

### GET `/predictions`
Lista todas as predições salvas no banco de dados.

**Headers:**
```
Authorization: Bearer <token>
```

**Query Parameters:**
- `limit` (opcional): Número máximo de resultados (padrão: 10)
- `offset` (opcional): Número de resultados para pular (padrão: 0)

**Response:**
```json
[
  {
    "id": 1,
    "sepal_length": 5.1,
    "sepal_width": 3.5,
    "petal_length": 1.4,
    "petal_width": 0.2,
    "predicted_class": "setosa",
    "created_at": "2025-11-03T15:30:00"
  }
]
```

## 📖 Exemplos de Uso

### Usando cURL

**1. Fazer login:**
```bash
curl -X POST http://localhost:5000/login \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}'
```

**2. Fazer predição:**
```bash
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer SEU_TOKEN_AQUI" \
  -d '{
    "sepal_length": 6.5,
    "sepal_width": 3.0,
    "petal_length": 4.5,
    "petal_width": 1.5
  }'
```

**3. Listar predições:**
```bash
curl -X GET "http://localhost:5000/predictions?limit=5" \
  -H "Authorization: Bearer SEU_TOKEN_AQUI"
```

### Usando Python

```python
import requests

# 1. Login
login_response = requests.post(
    "http://localhost:5000/login",
    json={"username": "admin", "password": "admin123"}
)
token = login_response.json()["token"]

# 2. Fazer predição
predict_response = requests.post(
    "http://localhost:5000/predict",
    headers={"Authorization": f"Bearer {token}"},
    json={
        "sepal_length": 5.1,
        "sepal_width": 3.5,
        "petal_length": 1.4,
        "petal_width": 0.2
    }
)

print(predict_response.json())
# {"predicted_class": 0, "predicted_class_name": "setosa"}

# 3. Listar predições
predictions_response = requests.get(
    "http://localhost:5000/predictions",
    headers={"Authorization": f"Bearer {token}"}
)

print(predictions_response.json())
```

### Usando Postman

1. **Login:**
   - Método: `POST`
   - URL: `http://localhost:5000/login`
   - Body (raw JSON):
     ```json
     {
       "username": "admin",
       "password": "admin123"
     }
     ```

2. **Predição:**
   - Método: `POST`
   - URL: `http://localhost:5000/predict`
   - Headers:
     - `Authorization`: `Bearer <token_obtido_no_login>`
     - `Content-Type`: `application/json`
   - Body (raw JSON):
     ```json
     {
       "sepal_length": 6.5,
       "sepal_width": 3.0,
       "petal_length": 4.5,
       "petal_width": 1.5
     }
     ```

## 📁 Estrutura do Projeto

```
ML/
│
├── api.py                 # API Flask principal
├── petals.py             # Script de treinamento do modelo
├── iris_model.pkl        # Modelo treinado (gerado após treinar)
├── predictions.db        # Banco de dados SQLite (criado automaticamente)
├── requirements.txt      # Dependências do projeto
└── README.md            # Este arquivo
```

## 🔐 Credenciais Padrão

**Username:** `admin`  
**Password:** `admin123`

⚠️ **Importante:** Altere essas credenciais em produção!

## 📊 Dataset

O projeto utiliza o dataset Iris clássico do scikit-learn, que contém:
- 150 amostras
- 4 características: sepal_length, sepal_width, petal_length, petal_width
- 3 classes: Setosa, Versicolor, Virginica

## 🤝 Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para abrir uma issue ou enviar um pull request.

## 📄 Licença

Este projeto está sob a licença MIT.

## 👨‍💻 Autor

Desenvolvido como parte do programa POSTECH-FIAP.

---

⭐ Se este projeto foi útil para você, considere dar uma estrela no repositório!

