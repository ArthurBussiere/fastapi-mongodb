## 🚀 FastAPI with MongoDB - Template

### 🏗️ Tech Stack

- **🐍 FastAPI** – High-performance Python web framework
- **🌱 MongoDB** – NoSQL database for scalable storage
- **🔍 Pydantic** – Data validation and serialization
- **🐋 Docker Compose** – Simplified containerized deployment
- **📓 Mongo Express** – Web-based MongoDB admin interface

### 🎯 Features

- Easy integration of FastAPI with MongoDB
- Pydantic-powered request validation
- Dockerized setup for seamless development and deployment
- Built-in Mongo Express for database management

### 🚀 Get Started

1. Clone the repository

   ```sh
   git clone https://github.com/ArthurBussiere/fastapi-mongodb.git
   cd fastapi-mongodb
   ```

2. Create a .env file and copy the content of .env.template

   ```bash
   cp .env.template .env
   ```

3. Edit .env file and define at least theses variables

   ```properties
   MONGO_DB_USERNAME="<username>"
   MONGO_DB_PASSWORD="<password>"
   SECRET_KEY="<secret_key>" # command to generate: openssl rand -hex 32
   ```

4. Use uv to create venv and manage packages & dependencies

   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   uv sync
   ```

5. Run Docker Compose to install MongoDB & MongoExpress services

   ```bash
   docker compose --profile database up -d
   ```

6. Run fast-api as development
   ```bash
   source .venv/bin/activate
   fastapi dev app/main.py
   ```


### 🚀 Deployment

⚠️ Work in Progress – Stay tuned!WIP
