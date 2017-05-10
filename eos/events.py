# Decided to put this in it's own file so that we can easily choose not to import it (thanks to mac-deprecated builds =/)

import datetime
from sqlalchemy.event import listen
from sqlalchemy.orm.collections import InstrumentedList

from eos.db.saveddata.fit import projectedFitSourceRel, boostedOntoRel

from eos.saveddata.fit import Fit
from eos.saveddata.module import Module
from eos.saveddata.drone import Drone
from eos.saveddata.fighter import Fighter
from eos.saveddata.cargo import Cargo
from eos.saveddata.implant import Implant
from eos.saveddata.booster import Booster

ignored_rels = [
    projectedFitSourceRel,
    boostedOntoRel
]


def update_fit_modified(target, value, oldvalue, initiator):
    if not target.owner:
        return

    if value != oldvalue:
        # some things (like Implants) have a backref to the fit, which actually produces a list.
        # In this situation, simply take the 0 index to get to the fit.
        # There may be cases in the future in which there are multiple fits, so this should be
        # looked at more indepth later
        if isinstance(target.owner, InstrumentedList):
            parent = target.owner[0]
        else:
            parent = target.owner

        # ensure this is a fit we're dealing with
        if isinstance(parent, Fit):
            parent.modified = datetime.datetime.now()


def apply_col_listeners(target, context):
    # We only want to set these events when the module is first loaded (otherwise events will fire during the initial
    # population of data). This runs through all columns and sets up "set" events on each column. We do it with each
    # column because the alternative would be to do a before/after_update for the Mapper itself, however we're only
    # allowed to change the local attributes during those events as that's inter-flush.
    # See http://docs.sqlalchemy.org/en/rel_1_0/orm/session_events.html#mapper-level-events

    # @todo replace with `inspect(Module).column_attrs` when mac binaries are updated

    manager = getattr(target.__class__, "_sa_class_manager", None)
    if manager:
        for col in manager.mapper.column_attrs:
            listen(col, 'set', update_fit_modified)


def rel_listener(target, value, initiator):
    if not target or (isinstance(value, Module) and value.isEmpty):
        return

    print "{} has had a relationship change :D".format(target)
    target.modified = datetime.datetime.now()


def apply_rel_listeners(target, context):
    # We only want to see these events when the fit is first loaded (otherwise events will fire during the initial
    # population of data). This sets listeners for all the relationships on fits. This allows us to update the fit's
    # modified date whenever something is added/removed from fit
    # See http://docs.sqlalchemy.org/en/rel_1_0/orm/events.html#sqlalchemy.orm.events.InstanceEvents.load

    # todo: when we can, move over to `inspect(es_Fit).relationships` (when mac binaries are updated)
    manager = getattr(target.__class__, "_sa_class_manager", None)
    if manager:
        for rel in manager.mapper.relationships:
            if rel in ignored_rels:
                continue
            listen(rel, 'append', rel_listener)
            listen(rel, 'remove', rel_listener)


listen(Fit, 'load', apply_rel_listeners)
listen(Module, 'load', apply_col_listeners)
listen(Drone, 'load', apply_col_listeners)
listen(Fighter, 'load', apply_col_listeners)
listen(Cargo, 'load', apply_col_listeners)
listen(Implant, 'load', apply_col_listeners)
listen(Booster, 'load', apply_col_listeners)
