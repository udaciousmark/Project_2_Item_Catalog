from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

DB_NAME = 'catalog'

class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)


class Item(Base):
    __tablename__ = 'item'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(String(500))
    category_id = Column(Integer, ForeignKey('category.id'), nullable=False)
    category = relationship(Category)


engine = create_engine('postgresql+psycopg2:///' + DB_NAME)

Base.metadata.create_all(engine)
