from sqlalchemy import create_engine
import config

def get_mt_mysql_db():
    return create_engine(config.mysql_conf)

def get_mt_postgresql_db():
    return create_engine(config.postgresql_conf)