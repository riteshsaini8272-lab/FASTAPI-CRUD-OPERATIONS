from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base

MYSQL_USER="root"
MYSQL_PASSWORD="pied9034P"
MYSQL_HOST= "localhost"
MYSQL_PORT=3306
MYSQL_DATABASE="fastapi"
DATABASE_URL=f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}"
#CONNECTON 
engine= create_engine(DATABASE_URL)

#SESSION 
SessionLocal =sessionmaker(autoflush=False,autocommit=False,bind=engine)
def get_db():
    db=SessionLocal()
    try:
        yield(db)
    finally:
        db.close()
Base = declarative_base()