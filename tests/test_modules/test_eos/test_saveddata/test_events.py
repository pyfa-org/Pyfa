# Add root folder to python paths
# This must be done on every test in order to pass in Travis
import os
import sys
import warnings
from types import SimpleNamespace

from sqlalchemy import create_engine, select
from sqlalchemy.exc import SAWarning
from sqlalchemy.orm import Session

script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.realpath(os.path.join(script_dir, '..', '..', '..', '..')))
sys._called_from_test = True


def test_owner_sync_does_not_modify_fit_during_flush(monkeypatch):
    import eos.config

    monkeypatch.setattr(eos.config, 'gamedata_connectionstring', 'sqlite:///:memory:')
    import eos.events
    from eos.db.saveddata.fit import fits_table
    from eos.saveddata.cargo import Cargo
    from eos.saveddata.fit import Fit

    item = SimpleNamespace(ID=1, attributes={}, overrides={})
    monkeypatch.setattr(eos.db, 'getItem', lambda itemID: item)
    engine = create_engine('sqlite:///:memory:')
    eos.db.saveddata_meta.create_all(engine)
    with Session(engine, expire_on_commit=False) as session:
        source, destination = Fit(), Fit()
        for fit in (source, destination):
            fit.shipID = 1
            fit.implantLocation = 0
        cargo = Cargo(item)
        source.cargo.append(cargo)
        session.add_all((source, destination))
        session.commit()
        cargo_id = cargo.ID
        session.expunge(cargo)
        cargo = session.get(Cargo, cargo_id)

        # Ordinary cargo edits must still update and persist the fit's timestamp.
        original_modified = source.modified
        cargo.amount = 2
        session.flush()
        assert source.modified > original_modified
        assert session.scalar(select(fits_table.c.modified).where(fits_table.c.ID == source.ID)) == source.modified

        cargo.owner = destination
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter('always', SAWarning)
            session.flush()

        assert cargo.fitID == destination.ID
        assert not [warning for warning in caught if issubclass(warning.category, SAWarning)]
    engine.dispose()
