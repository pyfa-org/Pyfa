# Decided to put this in it's own file so that we can easily choose not to import it (thanks to mac-deprecated builds =/)

import datetime
from sqlalchemy.event import listen

from eos.saveddata.fit import Fit
from eos.saveddata.module import Module


def update_fit_modified(target, value, oldvalue, initiator):
    if not target.owner:
        return

    if value != oldvalue:
        print "{} had a change via {}".format(target.owner, target)
        target.owner.modified = datetime.datetime.now()


def apply_col_listeners(target, context):
    # We only want to se these events when the module is first loaded (otherwise events will fire during the initial
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
            listen(rel, 'append', rel_listener)
            listen(rel, 'remove', rel_listener)

listen(Fit, 'load', apply_rel_listeners)
listen(Module, 'load', apply_col_listeners)