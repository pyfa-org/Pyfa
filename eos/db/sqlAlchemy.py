
import threading

from sqlalchemy import MetaData, create_engine
from sqlalchemy.orm import sessionmaker

import config
from eos import config as e_config


class sqlAlchemy:
    gamedata_connectionstring = e_config.gamedata_connectionstring
    if callable(gamedata_connectionstring):
        gamedata_engine = create_engine("sqlite://", creator=gamedata_connectionstring, echo=config.debug)
    else:
        gamedata_engine = create_engine(gamedata_connectionstring, echo=config.debug)

    gamedata_meta = MetaData()
    gamedata_meta.bind = gamedata_engine
    gamedata_session = sessionmaker(bind=gamedata_engine, autoflush=False, expire_on_commit=False)()

    # This should be moved elsewhere, maybe as an actual query. Current, without try-except, it breaks when making a new
    # game db because we haven't reached gamedata_meta.create_all()
    try:
        config.gamedata_version = gamedata_session.execute(
            "SELECT `field_value` FROM `metadata` WHERE `field_name` LIKE 'client_build'"
        ).fetchone()[0]
    except:
        config.gamedata_version = None

    saveddata_connectionstring = e_config.saveddata_connectionstring
    if saveddata_connectionstring is not None:
        if callable(saveddata_connectionstring):
            saveddata_engine = create_engine(creator=saveddata_connectionstring, echo=config.debug)
        else:
            saveddata_engine = create_engine(saveddata_connectionstring, echo=config.debug)

        saveddata_meta = MetaData()
        saveddata_meta.bind = saveddata_engine
        saveddata_session = sessionmaker(bind=saveddata_engine, autoflush=False, expire_on_commit=False)()

    # Lock controlling any changes introduced to session
    sd_lock = threading.Lock()

    # If using in memory saveddata, you'll want to reflect it so the data structure is good.
    if e_config.saveddata_connectionstring == "sqlite:///:memory:":
        saveddata_meta.create_all()


def rollback():
    with sqlAlchemy.sd_lock:
        sqlAlchemy.saveddata_session.rollback()
