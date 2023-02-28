import os

import sqlalchemy as sa


url = sa.engine.URL.create(
    drivername="postgresql+psycopg2",
    username=os.getenv("POSTGRES_USERNAME", ""),
    password=os.getenv("POSTGRES_PASSWORD", ""),
    host=os.getenv("POSTGRES_HOST", ""),
    port=int(os.getenv("POSTGRES_PORT", 5432)) if os.getenv("POSTGRES_PORT", "").isnumeric() else 5432,
    database=os.getenv("POSTGRES_NAME", ""),
)

engine = sa.create_engine(url)
meta_data = sa.MetaData()
