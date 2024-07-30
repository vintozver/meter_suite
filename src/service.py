import dateutil.tz
import datetime
import re
import sqlite3


re_latest = re.compile(r'^/\blatest\b/?')


def handle_default(env, responder):
    try:
        raw = open("meter.raw", "rt")
        buffer = raw.read()
    except OSError:
        buffer = None

    if buffer is not None:
        writer = responder('200 OK', [('Content-Type', 'application/json')])
        return (buffer).encode('utf-8'),
    else:
        responder('404 No data', [])
        return ('No meter raw data').encode('utf-8'),


def handle_latest(env, responder):
    writer = responder('200 OK', [('Content-Type', 'text/plain')])
    tz = dateutil.tz.gettz('US/Pacific')

    with sqlite3.connect("meter.db") as db_connection:
        def dict_factory(cursor, row):
            fields = [column[0] for column in cursor.description]
            return {key: value for key, value in zip(fields, row)}
        db_connection.row_factory = dict_factory
        
        any_data = False
        db_cursor = db_connection.cursor()
        db_cursor.execute(
            "SELECT * FROM instant_reads WHERE dt > ? ORDER BY dt DESC",
            (
                (datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(hours=24)).strftime("%Y-%m-%d %H:%M:%S"),
            )
        )
        for db_row in db_cursor:
            if not any_data:
                yield 'DT\t\tP\tVAR\n'.encode('utf-8')
                any_data = True
            dt = datetime.datetime.fromisoformat(db_row["dt"])
            dt = dt.replace(tzinfo=datetime.timezone.utc)
            dt = dt.astimezone(tz)
            yield ('%s\t%s\t%s\n' % (dt.strftime("%H:%M:%S"), db_row["P"], db_row["VAR"])).encode('utf-8')
        if not any_data:
            yield 'Nothing found'.encode('utf-8')


def application(env, responder):
    path = env['PATH_INFO']

    if re_latest.match(path) is not None:
        return handle_latest(env, responder)
    else:
        return handle_default(env, responder)

