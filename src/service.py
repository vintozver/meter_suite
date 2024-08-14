import dateutil.tz
import datetime
import re
import sqlite3
from . import config


re_latest = re.compile(r'^/\blatest\b/?')


def format_cos_theta(value: int) -> str:
    if value == 100:
        return ' 1.00'
    elif value > 100:
        return 'C' + ('%3.2f' % ((200 - value) / 100.))
    elif value < 100:
        return 'L' + ('%3.2f' % (value / 100.))


def handle_default(env, responder):
    try:
        raw = open("meter.raw", "rt")
        buffer = raw.read()
    except OSError:
        buffer = None

    if buffer is not None:
        writer = responder('200 OK', [('Content-Type', 'application/json')])
        yield buffer
    else:
        responder('404 No data', [])
        yield 'No meter raw data'


def handle_latest(env, responder):
    writer = responder('200 OK', [('Content-Type', 'text/plain')])
    tz = dateutil.tz.gettz('US/Pacific')

    with sqlite3.connect("meter.db") as db_connection:
        def dict_factory(cursor, row):
            fields = [column[0] for column in cursor.description]
            return {key: value for key, value in zip(fields, row)}
        db_connection.row_factory = dict_factory
        
        now = datetime.datetime.now(datetime.timezone.utc)

        any_data = False
        db_cursor = db_connection.cursor()
        db_cursor.execute(
            "SELECT * FROM instant_reads WHERE dt > ? ORDER BY dt DESC",
            (
                (now - datetime.timedelta(hours=24)).strftime("%Y-%m-%d %H:%M:%S"),
            )
        )
        for db_row in db_cursor:
            if not any_data:
                yield 'Now: %s\n\n' % now.astimezone(tz).strftime('%Y-%m-%d %H:%M:%S')
                yield 'DT               P       VAR%s%s%s%s%s%s\n' % (
                    '    PF1' if config.display_line1 else '',
                    '    PF2' if config.display_line2 else '',
                    '    PF3' if config.display_line3 else '',
                    '     V1 ' if config.display_line1 else '',
                    '     V2 ' if config.display_line2 else '',
                    '     V3 ' if config.display_line3 else '',
                )
                any_data = True
            dt = datetime.datetime.fromisoformat(db_row["dt"])
            dt = dt.replace(tzinfo=datetime.timezone.utc)
            dt = dt.astimezone(tz)
            yield '%s  %s  %s%s%s%s%s%s%s\n' % (
                dt.strftime("%H:%M:%S"),
                '%8.0f' % float(db_row["P"]),
                '%8.0f' % float(db_row["VAR"]),
                '  %s' % format_cos_theta(int(db_row["PF_1"])) if config.display_line1 else '',
                '  %s' % format_cos_theta(int(db_row["PF_2"])) if config.display_line2 else '',
                '  %s' % format_cos_theta(int(db_row["PF_3"])) if config.display_line3 else '',
                '  %5.2f' % float(db_row["V_1"]) if config.display_line1 else '',
                '  %5.2f' % float(db_row["V_2"]) if config.display_line2 else '',
                '  %5.2f' % float(db_row["V_3"]) if config.display_line3 else '',
            )
        if not any_data:
            yield 'Nothing found'


def application(env, responder):
    path = env['PATH_INFO']

    if re_latest.match(path) is not None:
        for buf in handle_latest(env, responder):
            yield buf.encode('utf-8')
    else:
        for buf in handle_default(env, responder):
            yield buf.encode('utf-8')

