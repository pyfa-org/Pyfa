# -*- coding: utf-8 -*-
#!/usr/bin/env python
if __name__ == "__main__":
    import argparse
    import json
    import os.path
    import sys
    sys.path.append(os.getcwd())

    from eos import *
    from eos.data.data_handler import JsonDataHandler
    from eos.const.eos import *

    json_path = r"/path/to/Phobos/dump"

    parser = argparse.ArgumentParser(description="Figure out what actually effect does")
    parser.add_argument("-e", "--effect", type=str, required=True, help="effect name")
    args = parser.parse_args()

    # open a few files to get human-readable names for data (EOS strictly works with numerical identifiers)
    with open(os.path.join(json_path, "dgmattribs.json"), mode='r', encoding="utf8") as file:
        dgmattribs = json.load(file)

    with open(os.path.join(json_path, 'dgmeffects.json'), mode='r', encoding="utf8") as file:
        dgmeffects = json.load(file)

    with open(os.path.join(json_path, 'invtypes.json'), mode='r', encoding="utf8") as file:
        invtypes = json.load(file)

    with open(os.path.join(json_path, 'invgroups.json'), mode='r', encoding="utf8") as file:
        invgroups = json.load(file)

    attr_id_name = {}
    attr_id_penalized = {}
    for row in dgmattribs:
        attr_id_name[row['attributeID']] = row['attributeName']
        attr_id_penalized[row['attributeID']] = 'not penalized' if row['stackable'] else 'penalized'

    effect_id_name = {}
    for row in dgmeffects:
        effect_id_name[row['effectID']] = row['effectName']
        if row['effectName'] == args.effect:
            effect_id = row['effectID']
            break

    type_id_name = {}
    for _, row in invtypes.items():
        name = row.get("typeName_en-us", None)
        if name:
            type_id_name[row['typeID']] = name

    group_id_name = {}
    for _, row in invgroups.items():
        group_id_name[row['groupID']] = row['groupName_en-us']

    data_handler = JsonDataHandler(json_path)   # Folder with Phobos data dump
    cache_handler = JsonCacheHandler(os.path.join(json_path, "cache", "eos_tq.json.bz2"))
    SourceManager.add('evedata', data_handler, cache_handler, make_default=True)

    effect = cache_handler.get_effect(effect_id)
    modifiers = effect.modifiers
    mod_counter = 1
    indent = '  '
    print('effect {}.py (id: {}) - build status is {}'.format(args.effect.lower(), effect_id, EffectBuildStatus(effect.build_status).name))
    for modifier in modifiers:
        print('{}Modifier {}:'.format(indent, mod_counter))
        print('{0}{0}state: {1}'.format(indent, State(modifier.state).name))
        print('{0}{0}scope: {1}'.format(indent, Scope(modifier.scope).name))
        print('{0}{0}srcattr: {1} {2}'.format(indent, attr_id_name[modifier.src_attr], modifier.src_attr))
        print('{0}{0}operator: {1} {2}'.format(indent, Operator(modifier.operator).name, modifier.operator))
        print('{0}{0}tgtattr: {1} ({2}) {3}'.format(
            indent,
            attr_id_name[modifier.tgt_attr],
            attr_id_penalized[modifier.tgt_attr],modifier.tgt_attr)
        )
        print('{0}{0}location: {1}'.format(indent, Domain(modifier.domain).name))
        try:
            filter_type = FilterType(modifier.filter_type).name
        except ValueError:
            filter_type = None
        print('{0}{0}filter type: {1}'.format(indent, filter_type))
        if modifier.filter_type is None or modifier.filter_type in (FilterType.all_, FilterType.skill_self):
            pass
        elif modifier.filter_type == FilterType.skill:
            print('{0}{0}filter value: {1}'.format(indent, type_id_name[modifier.filter_value]))
        elif modifier.filter_type == FilterType.group:
            print('{0}{0}filter value: {1}'.format(indent, group_id_name[modifier.filter_value]))
        mod_counter += 1
