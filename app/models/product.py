from sqlalchemy import Column, Integer, String, Float

from app.models.database import Base


class Product(Base):

    __tablename__ = "products"

    id = Column(Integer, primary_key=True)

    nome = Column(String, nullable=False)

    preco = Column(Float, nullable=False)

    quantidade = Column(Integer, nullable=False)