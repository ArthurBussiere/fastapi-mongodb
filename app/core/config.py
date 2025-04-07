from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
	model_config = SettingsConfigDict(
		env_file='.env',  # fix to handle different env depending on ENVIRONMENT
		env_ignore_empty=True,
		extra='ignore',
		env_file_encoding='utf-8',
	)

	MONGO_DB_SERVER: str
	MONGO_DB_PORT: str
	MONGO_DB_USERNAME: str
	MONGO_DB_PASSWORD: str
	MONGO_BD_TIMEOUT: int = 2500

	ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
	SECRET_KEY: str  # openssl rand -hex 32
	ALGORITHM: str

	TAGS_METADATA: list = [
		{'name': 'Auth', 'descritpion': ''},
		{
			'name': 'Users',
			'description': 'CRUD Operations with users. Login is handled by these endpoint',
		},
		{
			'name': 'Items',
			'description': 'Manage items. So _fancy_ they have their own docs.',
			'externalDocs': {
				'description': 'Items external docs',
				'url': 'https://fastapi.tiangolo.com/',
			},
		},
	]


settings = Settings()
