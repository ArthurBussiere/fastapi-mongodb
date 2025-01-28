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

1. Clone the repository:

   ```sh
   git clone https://github.com/ArthurBussiere/fastapi-mongodb.git
   cd fastapi-mongodb
   ```

2. Create a .env file and copy the content of .env.template:

   ```bash
   cp .env.template .env
   ```

3. Edit .env file and define at least theses variables:

   ```properties
   MONGO_DB_USERNAME="<username>"
   MONGO_DB_PASSWORD="<password>"
   SECRET_KEY="<secret_key>"
   ```

4. 