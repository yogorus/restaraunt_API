"""All of the models for the app"""
import uuid

from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, validates

from .database import Base

# pylint: disable=too-few-public-methods


class Menu(Base):
    """Menu table"""

    __tablename__ = 'menus'

    id = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False
    )
    title = Column(String)
    description = Column(String)

    submenus = relationship(
        'Submenu',
        back_populates='menu',
        cascade='all,delete',
        passive_deletes=True,
        lazy='selectin',
    )


class Submenu(Base):
    """Submenu Table"""

    __tablename__ = 'submenus'

    id = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False
    )
    title = Column(String)
    description = Column(String)
    menu_id = Column(UUID(as_uuid=True), ForeignKey('menus.id', ondelete='CASCADE'))

    menu = relationship('Menu', back_populates='submenus', lazy='selectin')
    dishes = relationship(
        'Dish',
        back_populates='submenu',
        cascade='all,delete',
        passive_deletes=True,
        lazy='selectin',
    )


class Dish(Base):
    """Dish Table"""

    __tablename__ = 'dishes'

    id = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False
    )
    title = Column(String)
    description = Column(String)
    price = Column(String)
    submenu_id = Column(
        UUID(as_uuid=True), ForeignKey('submenus.id', ondelete='CASCADE')
    )

    submenu = relationship('Submenu', back_populates='dishes', lazy='selectin')

    @validates('price')
    def validate_price(self, key, value):
        # pylint: disable=unused-argument
        """Validate price to be no less than len 4"""
        if len(value) < 4:
            raise ValueError('Price length must be at least 4 characters!')
        return value
