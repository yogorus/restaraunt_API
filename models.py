from sqlalchemy import Column, ForeignKey, Integer, Float, String
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid

from database import Base

class Menu(Base):
    __tablename__ = "menus"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    title = Column(String)
    description = Column(String)

    submenus = relationship("Submenu", back_populates='menu', cascade='all,delete', passive_deletes=True)

    def submenus_count(self) -> int:
        return len(self.submenus)
    
    def dishes_count(self) -> int:
        return sum(submenu.dishes_count() for submenu in self.submenus)


class Submenu(Base):
    __tablename__ = 'submenus'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    title = Column(String)
    description = Column(String)
    menu_id = Column(UUID(as_uuid=True), ForeignKey('menus.id', ondelete="CASCADE"))

    menu = relationship("Menu", back_populates='submenus')
    dishes = relationship('Dish', back_populates='submenu', cascade='all,delete', passive_deletes=True)

    def dishes_count(self) -> int:
        return len(self.dishes)


class Dish(Base):
    __tablename__ = 'dishes'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    title = Column(String)
    description = Column(String)
    price = Column(Float)
    submenu_id = Column(UUID(as_uuid=True), ForeignKey('submenus.id', ondelete="CASCADE"))

    submenu = relationship('Submenu', back_populates='dishes')
