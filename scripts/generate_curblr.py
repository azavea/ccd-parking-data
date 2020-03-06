#!/usr/bin/env python3
import json
import os
import sys
from copy import copy, deepcopy
from hashlib import md5
from os.path import join
from subprocess import call

import click
import geopandas as gpd
import pandas as pd
from curblr import (CurbLRObject, Feature, FeatureCollection, Location,
                    Manifest, Payment, Regulation, Rule, TimeSpan, UserClass)
from curblr.authority import Authority
from curblr.constants import DAYS
from curblr.time_rule import DaysOfWeek, DesignatedPeriod, TimeOfDay
from curblr.utils import time_str


def combine_linear_ref_radii(linear_ref_dir):
    files = os.listdir(linear_ref_dir)
    if 'compiled.matched.geojson' not in files:
        def filepath(x): return join(linear_ref_dir,
                                     'NEW_{}.matched.geojson'.format(x))
        def filepath_end(x): return join(
            linear_ref_dir, 'NEW_{}_ends.matched.geojson'.format(x))

        for x in range(5, 40, 5):
            with open(filepath(x)) as f:
                gj = json.load(f)
            for f in gj['features']:
                if f:
                    st, en = f['properties'].pop('section')
                    f['properties']['start'] = st
                    f['properties']['end'] = en
            with open(filepath_end(x), 'w') as f:
                json.dump(gj, f)

        matched = gpd.read_file(filepath_end(5))
        unmatched = gpd.read_file(filepath(5).replace('matched', 'unmatched'))
        radii = [(x, gpd.read_file(filepath_end(x))) for x in range(10, 40, 5)]
        for gid in unmatched['globalid_s']:
            for radius, df in radii:
                rdf = df[df['pp_globalid_s'] == gid]
                if len(rdf) > 0:
                    rdf_c = copy(rdf)
                    rdf_c['radius'] = radius
                    matched = copy(pd.concat([matched, rdf_c], sort=True))
                    break

        matched_gids = matched['pp_globalid_s'].values
        unmatched_gids = [i for i in unmatched['globalid_s']
                          if i not in matched_gids]
        matched.to_file(
            join(linear_ref_dir, 'compiled.matched.geojson'), driver='GeoJSON')
        unmatched = unmatched[unmatched['globalid_s'].isin(unmatched_gids)]
        unmatched.to_file(
            join(linear_ref_dir, 'compiled.unmatched.geojson'), driver='GeoJSON')
        return matched
    else:
        return gpd.read_file(join(linear_ref_dir, 'compiled.matched.geojson'))


def curb_id_to_regulations(pzr, curb_id, reg_lookup, payment=None):
    one_reg = pzr[pzr['globalid_static'] == curb_id]

    # timing needs to be cleaned up
    reg_combos = list(set(zip(one_reg['reg_is'], one_reg['time_limit'])))

    df_regs = []

    for ur, time_limit in reg_combos:
        if ur != 'None':
            df_regs.append((ur.lower(),
                            one_reg[(one_reg['reg_is'] == ur) & (
                                one_reg['time_limit'] == time_limit)],
                            time_limit))
    for ur in one_reg['reg_is_not'].unique():
        if ur != 'None' and ur != 'Other (See Notes)':
            df_regs.append((ur.lower(),
                            one_reg[one_reg['reg_is_not'] == ur],
                            None))
    contractor_df = one_reg[one_reg['contractor'] != 'Valid']
    if len(contractor_df) > 0:
        df_regs.append(('contractor placard not valid',
                        contractor_df,
                        None))

    reg_objs = []
    for reg, df, time_limit in df_regs:
        time_spans = {}
        day = None
        start_hour = None
        end_hour = None

        for _, r in df.iterrows():
            if not day:
                pass
            elif (day != r['day_str']) | (end_hour != int(r['hour'])):
                if (start_hour, end_hour) in time_spans:
                    time_spans[(start_hour, end_hour)].append(day)
                else:
                    time_spans[(start_hour, end_hour)] = [day]
            else:
                end_hour += 1
                continue

            day = r['day_str']
            start_hour = int(r['hour'])
            end_hour = start_hour + 1

        if (start_hour, end_hour) in time_spans:
            time_spans[(start_hour, end_hour)].append(day)
        else:
            time_spans[(start_hour, end_hour)] = [day]

        reg_c = reg.lower().strip()

        s = reg_lookup.get(reg_c)

        # priority
        priority = s.get('priority', 4)

        # max stay
        if not time_limit or time_limit == 'None':
            max_stay = None
        else:
            time_limit = float(time_limit)
            if time_limit == 0:
                max_stay = None
            elif time_limit == 0.3:
                max_stay = 20
            else:
                max_stay = int(time_limit * 60)

        clr_rule = Rule(activity=s['activity'],
                        reason=s['reason'],
                        max_stay=max_stay,
                        payment=True if payment and s['activity'] == 'parking' else False)

        clr_userclasses = None
        classes = [c for c in s.get('classes') if c]

        if len(classes) > 0:
            clr_userclasses = [UserClass(classes)]

        time_span_objs = []
        for se, days in time_spans.items():
            if len(days) < 7:
                days_of_week = DaysOfWeek(days)
            else:
                days_of_week = None

            if se == (0, 24):
                time_of_day = None
            else:
                time_of_day = TimeOfDay(se[0], se[1])

            designated_period = None
            if curb_id == '{713C8CDA-12A4-4243-A2F6-E6954AF16AB3}':
                designated_period = DesignatedPeriod(
                    'school hours', 'only during')
            if s.get('designated period'):
                designated_period = DesignatedPeriod(
                    **s.get('designated period'))
            ts = TimeSpan(days_of_week=days_of_week,
                          times_of_day=[
                              time_of_day] if time_of_day else time_of_day,
                          designated_periods=[designated_period] if designated_period else designated_period)

            if not ts.is_empty():
                time_span_objs.append(ts)

        if time_span_objs == []:
            time_span_objs = None

        if clr_rule.activity != 'parking':
            payment = None

        reg_obj = Regulation(clr_rule,
                             clr_userclasses,
                             time_span_objs,
                             payment=payment,
                             priority=priority)

        reg_objs.append(reg_obj)

    return reg_objs


def generate_curblr(segments, regulation_table, reg_lookup, original_geoms=False):
    phila = Authority('ppa', 'http://www.philapark.org/', '1-888-591-3636')
    manifest = Manifest(time_zone='EET', currency='USD', authority=phila)
    unlimited_parking = Rule('parking', 'no regulations listed')
    fc = FeatureCollection(manifest=manifest)

    for i, seg in segments.iterrows():
        gid = seg['globalid_s']
        iid = gid.replace('{', '').replace('}', '')
        images = [join('img', i) for i in os.listdir('img') if iid in i]

        if not isinstance(seg['shstReferenceId'], str):
            loc = Location('unmatched', 'unmatched',
                           'unmatched', 'unmatched',
                           object_id=gid, marker='sign',
                           street_name=seg['Street'])
            geom = seg['geometry_y']
        else:
            loc = Location(
                seg['shstReferenceId'],
                seg['sideOfStreet'],
                seg['start'],
                seg['end'],
                object_id=seg['pp_globalid_s'],
                marker='sign',
                street_name=seg['pp_street'])
            geom = seg['geometry_x']

        if original_geoms:
            geom = seg['geometry_y']

        feature = Feature(geom, loc, images=images)

        # get all regulations for this segment
        regs_gdf = regulation_table[regulation_table['globalid_static'] == gid]

        # payment
        m = seg['Metering']
        payment = Payment(methods=[m.lower().strip()]) if m not in (
            None, 'No Meters') else None

        reg_objs = curb_id_to_regulations(
            regulation_table, gid, reg_lookup, payment)
        for ro in reg_objs:
            feature.add_regulation(ro)

        feature.fill_unregulated_time(unlimited_parking)

        if seg['PermitZone']:
            feature.add_regulation(permit_regulation(seg['PermitZone']))

        fc.add_feature(feature)

        if (i + 1) % 500 == 0:
            print('Completed [{}] of {}'.format(i+1, len(segments)))

    print('Completed [{}] of {}'.format(i+1, len(segments)))

    return fc


def permit_regulation(permit_no):
    return Regulation(
        Rule('parking', 'permitted parking'),
        [UserClass(['permit holders'], [permit_no])],
        priority=4
    )


def read(segment_uri, hour_table_uri, linear_ref_dir, reg_lookup_uri):
    segments = gpd.read_file(segment_uri)  # pz
    hour_table = pd.read_csv(hour_table_uri, dtype=str,
                             keep_default_na=False)  # pzr
    hour_table['time_limit'] = hour_table['time_limit'].apply(
        lambda x: 'None' if x == '' else x)

    linear_ref = combine_linear_ref_radii(linear_ref_dir)

    with open(reg_lookup_uri) as f:
        reg_lookup = json.load(f)

    return (segments, hour_table, linear_ref, reg_lookup)


def to_relational(fc):
    lines = []
    regulations = []
    time_spans = []

    for feature in fc.features:

        loc = feature.location

        curb_id = md5('{} {} {} {}'.format(loc.object_id, loc.shst_ref_id, loc.shst_location_start, loc.shst_location_end).encode()).hexdigest()

        feature_d = {
            'curb_id': curb_id,
            'type': feature.type,
            'geometry': feature.geometry
        }

        if feature.images:
            feature_d['images'] = ';'.join(feature.images)

        shp_field_names = {
            'shst_ref_id': 'shst_ref',
            'side_of_street': 'strt_side',
            'shst_location_start': 'shst_loc_s',
            'shst_location_end': 'shst_loc_e',
            'derived_from': 'derived_fr',
            'object_id': 'object_id',
            'marker': 'marker',
            'bays_angle': 'bays_angle',
            'bays_count': 'bays_count',
            'street_name': 'strt_name'}

        for f in loc.fields:
            a = loc.__getattribute__(f)
            if a != None:
                feature_d[shp_field_names.get(f)] = a

        lines.append(feature_d)

        for reg in feature.regulations:
            reg_id = md5('{} {}'.format(curb_id, str(reg.to_dict())).encode()).hexdigest()

            reg_d = {
                'curb_id': curb_id,
                'regulation_id': reg_id,
                'priority': reg.priority
            }

            for attr in ('rule', 'payment'):
                obj = reg.__getattribute__(attr)
                if obj:
                    for f in obj.fields:
                        a = obj.__getattribute__(f)
                        if a:
                            if isinstance(a, list):
                                a = ';'.join(a)
                            reg_d['{}/{}'.format(attr, f)] = a

            if reg.user_classes:
                uc_str = ';'.join([';'.join(x.classes)
                                   for x in reg.user_classes])
                reg_d['user_classes/classes'] = uc_str

                subclasses_str = ''
                for uc in reg.user_classes:
                    if uc.subclasses:
                        subclasses_str += ';'.join([str(x)
                                                    for x in uc.subclasses])
                if subclasses_str != '':
                    reg_d['user_classes/subclasses'] = subclasses_str

            regulations.append(reg_d)

            if not reg.time_spans:
                ts_id = md5('{} {}'.format(reg_id, 'all time').encode()).hexdigest()

                ts_d = {
                        'curb_id': curb_id,
                        'regulation_id': reg_id,
                        'timespan_id': ts_id,
                        'days': ';'.join(DAYS),
                        'from_str': '0:00',
                        'to_str': '24:00',
                        'from_num': 0,
                        'to_num': 24
                }

                for d in DAYS:
                    ts_d[d] = 1

                time_spans.append(ts_d)
            else:
                for ts in reg.time_spans:
                    ts_id = md5('{} {}'.format(reg_id, str(ts.to_dict())).encode()).hexdigest()

                    ts_d = {
                        'curb_id': curb_id,
                        'regulation_id': reg_id,
                        'timespan_id': ts_id,
                        'days': ';'.join(ts.days_of_week.days if ts.days_of_week else DAYS)
                    }

                    for d in DAYS:
                        ts_d[d] = 1
                        if ts.days_of_week:
                            if d not in ts.days_of_week.days:
                                ts_d[d] = 0

                    if not ts.times_of_day:
                        ts_d['from_str'] = '0:00'
                        ts_d['to_str'] = '24:00'
                        ts_d['from_num'] = 0
                        ts_d['to_num'] = 24
                        time_spans.append(ts_d)
                    else:
                        for tod in ts.times_of_day:

                            ts_d_c = copy(ts_d)

                            ts_d_c['timespan_id'] = hash('{} {}'.format(reg_id, str(tod.to_dict())))
                            ts_d_c['from_str'] = tod.to_dict()['from']
                            ts_d_c['to_str'] = '24:00' if tod.to_dict()['to'] == '23:59' else tod.to_dict()['to']

                            def decimal_time(time):
                                hour = time.hour
                                minute = 60 if time.minute == 59 else time.minute
                                return hour + (minute / 60)

                            ts_d_c['from_num'] = decimal_time(tod.time_from)
                            ts_d_c['to_num'] = decimal_time(tod.time_to)

                            time_spans.append(ts_d_c)

    line_gdf = gpd.GeoDataFrame(lines, crs={'init': 'epsg:4326'})
    reg_df = pd.DataFrame(regulations)
    ts_df = pd.DataFrame(time_spans)

    return (line_gdf, reg_df, ts_df)


@click.command()
@click.option('--segment_uri', help='URI for original segment geometries')
@click.option('--hour_table_uri', help='URI for hour table of regulations')
@click.option('--linear_ref_dir', help='Directory with linear reference output')
@click.option('--reg_lookup_uri', help='URI for regulation lookup JSON')
@click.option('--output_key', default=None, help='Directory for all output')
@click.option('--original_geoms', is_flag=True)
def main(segment_uri, hour_table_uri, linear_ref_dir, reg_lookup_uri, output_key, original_geoms):
    if not output_key:
        output_key = time_str()

    output_dir = join('data/output/', output_key)
    if not os.path.isdir(output_dir):
        os.makedirs(output_dir)

    segments, hour_table, linear_ref, reg_lookup = read(
        segment_uri, hour_table_uri, linear_ref_dir, reg_lookup_uri)

    call('cp {} {}'.format(join(linear_ref_dir, 'compiled.matched.geojson'), join(
        output_dir, '{}_LR.matched.geojson').format(output_key)), shell=True)

    df = pd.merge(linear_ref, segments, 'outer',
                  left_on='pp_globalid_s', right_on='globalid_s')

    fc = generate_curblr(df, hour_table, reg_lookup,
                         original_geoms=original_geoms)
    fc.save(join(output_dir, '{}.curblr.json'.format(output_key)))

    # fc = FeatureCollection.from_file('/home/simon/files/client/ccd-curbs/ccd/data/output/non_offset_03-02_09-45/non_offset_03-02_09-45.curblr.json')

    fc_null_removed = deepcopy(fc)
    fc_null_removed.features = []
    for f in fc.features:
        if f.location.shst_ref_id != 'unmatched':
            fc_null_removed.features.append(f)
    fc_null_removed.save(join(output_dir, '{}_null-removed.curblr.json'.format(output_key)))

    lines, regs, timespans = to_relational(fc)
    lines.to_file(join(output_dir, '{}_segments'.format(output_key)))
    regs.to_csv(
        join(output_dir, '{}_regulations.csv'.format(output_key)), index=False)
    timespans.to_csv(
        join(output_dir, '{}_timespans.csv'.format(output_key)), index=False)
    
    joined = pd.merge(lines, regs, 'right', 'curb_id')
    joined = pd.merge(joined, timespans, 'right', ['curb_id', 'regulation_id'])
    joined.to_file(join(output_dir, '{}_segments_with_regs'.format(output_key)))


# write fc
if __name__ == "__main__":
    main()
