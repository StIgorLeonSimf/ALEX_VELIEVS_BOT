from sqlalchemy.orm import (DeclarativeBase, Mapped, mapped_column,
                            relationship)
from sqlalchemy import BigInteger, String, ForeignKey, Table, Column
from sqlalchemy.ext.asyncio import (AsyncAttrs, async_sessionmaker,
                                    create_async_engine)

engine = create_async_engine(url='sqlite+aiosqlite:///db.sqlite3')
async_session = async_sessionmaker(engine)

class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger)


class Category(Base):
    __tablename__ = 'categories'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(40))


class Item(Base):
    __tablename__ = 'items'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(25))
    description: Mapped[str] = mapped_column(String(100))
    price: Mapped[int] = mapped_column()
    category: Mapped[int] = mapped_column(ForeignKey('categories.id'))


async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

"""one to one"""
# class Parent(Base):
#     __tablename__ = 'parent'
#     id: Mapped[int] = mapped_column(primary_key=True)
#     child: Mapped['Child'] = relationship('Child', back_populates='parent',
#                                           uselist=False)
#
# class Child(Base):
#     __tablename__ = 'child'
#     id: Mapped[int] = mapped_column(primary_key=True)
#     parent_id: Mapped[int] = mapped_column(ForeignKey('parent.id'))
#     parent: Mapped['Parent'] = relationship('Parent', back_populates='child')

"""one to many"""
# class Parent(Base):
#     __tablename__ = 'parent'
#     id: Mapped[int] = mapped_column(primary_key=True)
#     children: Mapped[list['Child']] = relationship('Child',
#                                                    back_populates='parent')
#
#
# class Child(Base):
#     __tablename__ = 'child'
#     id: Mapped[int] = mapped_column(primary_key=True)
#     parent_id: Mapped[int] = mapped_column(ForeignKey('parent.id'))
#     parent: Mapped['Parent'] = relationship('Parent', back_populates='children')


"""many to many """
# association_table = Table('association',
#                           Base.metadata,
#                           Column('left_id', ForeignKey('left.id'),
#                                  primary_key=True),
#                           Column('right_id', ForeignKey('right.id'),
#                                  primary_key=True)
#                           )
# class Left(Base):
#     __tablename__ = 'left'
#     id: Mapped[int] = mapped_column(primary_key=True)
#     rights: Mapped[list['Right']] = relationship('Right',
#                                                 secondary=association_table,
#                                                 back_populates='lefts')
#
# class Right(Base):
#     __tablename__ = 'right'
#     id: Mapped[int] = mapped_column(primary_key=True)
#     lefts: Mapped[list['Left']] = relationship('Left',
#                                                 secondary=association_table,
#                                                 back_populates='rights')

