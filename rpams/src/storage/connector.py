import config as config
# import sqlalchemy
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import (
    String,
    Integer,
    Column,
    create_engine,
    exc
)

Base = declarative_base()


class WebsiteTable(Base):
    """
    Website table scheme for SQLite.


    Attributes:
        id             ID of row in table
        scrubber       Scrubber name
        requests_count Requests count
    """
    __tablename__ = 'website'

    id = Column('id', Integer(), primary_key=True, autoincrement=True)
    scrubber = Column('scrubber', String(2000), unique=False)
    requests_count = Column('requests_count', Integer(), unique=False)

    def __repr__(self):
        return f"<Website(" \
               f"id='{self.id}', " \
               f"scrubber='{self.scrubber}', " \
               f"requests_count='{self.requests_count}'" \
               f")>"


class ProcessTable(Base):
    """
    Process table scheme for SQLite.

    Attributes:
        pid            Process ID of row in table
        scrubber       Scrubber name
    """
    __tablename__ = 'process'

    pid = Column('pid', Integer(), unique=False, primary_key=True)
    scrubber = Column('scrubber', String(2000), unique=False)

    def __repr__(self):
        return f"<class Process(" \
               f"pid='{self.pid}', " \
               f"scrubber='{self.scrubber}', " \
               f")>"


class StorageORM:
    """
    Connection setup.

    Attributes:
    engine  SQLite engine instance
    session Session instance
    """

    def __init__(self):
        # create connection
        self.engine = create_engine(config.SQLITE_PATH)

        # create tables
        Base.metadata.create_all(self.engine)

        Session = sessionmaker(bind=self.engine)
        self.session = Session()


class Website:
    """
    Driver for table and manage data.

    Attributes:
    session Session instance
    """
    __session__ = None

    @classmethod
    def set_session(cls, session) -> None:
        """
        Set session.

        :param session: Session instance
        :return:
        """
        cls.__session__ = session

    @classmethod
    def get(cls, column='', value=''):
        """
        Get data from table by column name and value.

        :param column: Column name in table
        :param value: Value
        :return: row from table
        """
        try:
            get_by_dict = {
                'id': cls.__session__.query(WebsiteTable).filter_by(id=value).one,
                'scrubber': cls.__session__.query(WebsiteTable).filter_by(scrubber=value).one,
                'requests_count': cls.__session__.query(WebsiteTable).filter_by(requests_count=value).one,
            }

            if column in get_by_dict.keys():
                return get_by_dict[column]()
        except exc.NoResultFound:
            pass

        return None

    @classmethod
    def add(cls, scrubber='') -> bool:
        """
        Add new row to table.

        :param scrubber: Scrubber name
        :return: bool result, if return True means success update else False means that error update
        """
        requests_count_default_value: int = 0

        try:
            website: WebsiteTable = WebsiteTable(
                scrubber=scrubber,
                requests_count=requests_count_default_value
            )

            cls.__session__.add(website)
            cls.__session__.commit()

            return True
        except exc.IntegrityError:
            cls.__session__.rollback()

        return False

    @classmethod
    def update(cls, website_id='', column='', value='') -> bool:
        """
        Update row in table by id, column name and value.

        :param website_id: ID of row in table
        :param column: Column name
        :param value: Value
        :return: bool result, if return True means success update else False means that error update
        """
        try:
            cls.__session__.query(WebsiteTable).filter_by(id=website_id).update({column: value})
            cls.__session__.commit()

            return True
        except exc.NoResultFound:
            pass

        return False

    @classmethod
    def delete(cls, website_id='') -> bool:
        """
        Delete row in table by id.

        :param website_id:
        :return: bool result, if return True means success delete else False means that error delete
        """
        try:
            cls.__session__.query(WebsiteTable).filter_by(id=website_id).delete()
            cls.__session__.commit()

            return True
        except exc.NoResultFound:
            pass

        return False


class Process:
    """
    Driver for table and manage data.

    Attributes:
    session Session instance
    """
    __session__ = None

    @classmethod
    def set_session(cls, session) -> None:
        """
        Set session.

        :param session: Session instance
        :return:
        """
        cls.__session__ = session

    @classmethod
    def get(cls, column='', value=''):
        """
        Get data from table by column name and value.

        :param column: Column name in table
        :param value: Value
        :return: row from table
        """
        try:
            get_by_dict = {
                'pid': cls.__session__.query(ProcessTable).filter_by(pid=value).one,
                'scrubber': cls.__session__.query(ProcessTable).filter_by(scrubber=value).one,
            }

            if column in get_by_dict.keys():
                return get_by_dict[column]()
        except exc.NoResultFound:
            pass

        return None

    @classmethod
    def add(cls, pid=0, scrubber='') -> bool:
        """
        Add new row to table.

        :param pid: Process ID
        :param scrubber: Scrubber name
        :return: bool result, if return True means success update else False means that error update
        """
        try:
            process: ProcessTable = ProcessTable(
                pid=pid,
                scrubber=scrubber
            )

            cls.__session__.add(process)
            cls.__session__.commit()

            return True
        except exc.IntegrityError:
            cls.__session__.rollback()

        return False

    @classmethod
    def delete(cls, scrubber='') -> bool:
        """
        Delete row in table by id.

        :param website_id:
        :return: bool result, if return True means success delete else False means that error delete
        """
        try:
            cls.__session__.query(ProcessTable).filter_by(scrubber=scrubber).delete()
            cls.__session__.commit()

            return True
        except exc.NoResultFound:
            pass

        return False
