ALTER TABLE public.history DROP CONSTRAINT history_pkey, ADD PRIMARY KEY (itemid, clock, ns);
ALTER TABLE public.history_log DROP CONSTRAINT history_log_pkey, ADD PRIMARY KEY (itemid, clock, ns);
ALTER TABLE public.history_str DROP CONSTRAINT history_str_pkey, ADD PRIMARY KEY (itemid, clock, ns);
ALTER TABLE public.history_text DROP CONSTRAINT history_text_pkey, ADD PRIMARY KEY (itemid, clock, ns);
ALTER TABLE public.history_uint DROP CONSTRAINT history_uint_pkey, ADD PRIMARY KEY (itemid, clock, ns);
ALTER TABLE public.trends DROP CONSTRAINT trends_pkey, ADD PRIMARY KEY (itemid, clock);
ALTER TABLE public.trends_uint DROP CONSTRAINT trends_uint_pkey, ADD PRIMARY KEY (itemid, clock);
ALTER TABLE public.proxy_history DROP CONSTRAINT proxy_history_pkey, ADD PRIMARY KEY (id, itemid, clock, ns);

select create_hypertable('history', 'clock', chunk_time_interval => 86400, migrate_data => true);
select create_hypertable('history_log', 'clock', chunk_time_interval => 86400, migrate_data => true);
select create_hypertable('history_str', 'clock', chunk_time_interval => 86400, migrate_data => true);
select create_hypertable('history_text', 'clock', chunk_time_interval => 86400, migrate_data => true);
select create_hypertable('history_uint', 'clock', chunk_time_interval => 86400, migrate_data => true);
select create_hypertable('trends', 'clock', chunk_time_interval => 86400, migrate_data => true);
select create_hypertable('trends_uint', 'clock', chunk_time_interval => 86400, migrate_data => true);
select create_hypertable('proxy_history', 'clock', chunk_time_interval => 86400, migrate_data => true);

DROP FUNCTION IF EXISTS zbx_ts_unix_now();
CREATE OR REPLACE FUNCTION zbx_ts_unix_now()
RETURNS INTEGER AS 
$$
BEGIN
    RETURN EXTRACT(EPOCH FROM NOW())::INTEGER;
END;
$$
LANGUAGE plpgsql STABLE;

SELECT set_integer_now_func('history', 'zbx_ts_unix_now');
SELECT set_integer_now_func('history_log', 'zbx_ts_unix_now');
SELECT set_integer_now_func('history_str', 'zbx_ts_unix_now');
SELECT set_integer_now_func('history_text', 'zbx_ts_unix_now');
SELECT set_integer_now_func('history_uint', 'zbx_ts_unix_now');
SELECT set_integer_now_func('trends', 'zbx_ts_unix_now');
SELECT set_integer_now_func('trends_uint', 'zbx_ts_unix_now');
SELECT set_integer_now_func('proxy_history', 'zbx_ts_unix_now');

SELECT remove_retention_policy('history', true);
SELECT add_retention_policy('history', 
                            EXTRACT(epoch FROM CAST(to_char(CURRENT_DATE - INTERVAL'89 day' + TIME'23:59:59', 'yyyy-mm-dd hh24:mi:ss') AS TIMESTAMPTZ))::INTEGER,
                            true,
                            justify_interval(interval '24 hours'),
                            to_char(CURRENT_DATE + INTERVAL'1 day' + TIME'00:01:00', 'yyyy-mm-dd hh24:mi:ss')::TIMESTAMPTZ,
                           'Asia/Shanghai');

SELECT remove_retention_policy('history_uint', true);
SELECT add_retention_policy('history_uint', 
                            EXTRACT(epoch FROM CAST(to_char(CURRENT_DATE - INTERVAL'89 day' + TIME'23:59:59', 'yyyy-mm-dd hh24:mi:ss') AS TIMESTAMPTZ))::INTEGER,
                            true,
                            justify_interval(interval '24 hours'),
                            to_char(CURRENT_DATE + INTERVAL'1 day' + TIME'00:01:00', 'yyyy-mm-dd hh24:mi:ss')::TIMESTAMPTZ,
                           'Asia/Shanghai');

SELECT remove_retention_policy('history_log', true);
SELECT add_retention_policy('history_log', 
                            EXTRACT(epoch FROM CAST(to_char(CURRENT_DATE - INTERVAL'89 day' + TIME'23:59:59', 'yyyy-mm-dd hh24:mi:ss') AS TIMESTAMPTZ))::INTEGER,
                            true,
                            justify_interval(interval '24 hours'),
                            to_char(CURRENT_DATE + INTERVAL'1 day' + TIME'00:01:00', 'yyyy-mm-dd hh24:mi:ss')::TIMESTAMPTZ,
                           'Asia/Shanghai');

SELECT remove_retention_policy('history_text', true);
SELECT add_retention_policy('history_text', 
                            EXTRACT(epoch FROM CAST(to_char(CURRENT_DATE - INTERVAL'89 day' + TIME'23:59:59', 'yyyy-mm-dd hh24:mi:ss') AS TIMESTAMPTZ))::INTEGER,
                            true,
                            justify_interval(interval '24 hours'),
                            to_char(CURRENT_DATE + INTERVAL'1 day' + TIME'00:01:00', 'yyyy-mm-dd hh24:mi:ss')::TIMESTAMPTZ,
                           'Asia/Shanghai');

SELECT remove_retention_policy('history_str', true);
SELECT add_retention_policy('history_str', 
                            EXTRACT(epoch FROM CAST(to_char(CURRENT_DATE - INTERVAL'89 day' + TIME'23:59:59', 'yyyy-mm-dd hh24:mi:ss') AS TIMESTAMPTZ))::INTEGER,
                            true,
                            justify_interval(interval '24 hours'),
                            to_char(CURRENT_DATE + INTERVAL'1 day' + TIME'00:01:00', 'yyyy-mm-dd hh24:mi:ss')::TIMESTAMPTZ,
                           'Asia/Shanghai');

SELECT remove_retention_policy('trends', true);
SELECT add_retention_policy('trends', 
                            EXTRACT(epoch FROM CAST(to_char(CURRENT_DATE - INTERVAL'89 day' + TIME'23:59:59', 'yyyy-mm-dd hh24:mi:ss') AS TIMESTAMPTZ))::INTEGER,
                            true,
                            justify_interval(interval '24 hours'),
                            to_char(CURRENT_DATE + INTERVAL'1 day' + TIME'00:01:00', 'yyyy-mm-dd hh24:mi:ss')::TIMESTAMPTZ,
                           'Asia/Shanghai');
SELECT remove_retention_policy('trends_uint', true);
SELECT add_retention_policy('trends_uint', 
                            EXTRACT(epoch FROM CAST(to_char(CURRENT_DATE - INTERVAL'89 day' + TIME'23:59:59', 'yyyy-mm-dd hh24:mi:ss') AS TIMESTAMPTZ))::INTEGER,
                            true,
                            justify_interval(interval '24 hours'),
                            to_char(CURRENT_DATE + INTERVAL'1 day' + TIME'00:01:00', 'yyyy-mm-dd hh24:mi:ss')::TIMESTAMPTZ,
                           'Asia/Shanghai');
SELECT remove_retention_policy('proxy_history', true);
SELECT add_retention_policy('proxy_history', 
                            EXTRACT(epoch FROM CAST(to_char(CURRENT_DATE - INTERVAL'89 day' + TIME'23:59:59', 'yyyy-mm-dd hh24:mi:ss') AS TIMESTAMPTZ))::INTEGER,
                            true,
                            justify_interval(interval '24 hours'),
                            to_char(CURRENT_DATE + INTERVAL'1 day' + TIME'00:01:00', 'yyyy-mm-dd hh24:mi:ss')::TIMESTAMPTZ,
                           'Asia/Shanghai'
);

ALTER TABLE history SET (timescaledb.compress = true, timescaledb.compress_orderby = 'clock,ns ASC', timescaledb.compress_segmentby = 'itemid');
ALTER TABLE history_log SET (timescaledb.compress = true, timescaledb.compress_orderby = 'clock,ns ASC', timescaledb.compress_segmentby = 'itemid');
ALTER TABLE history_str SET (timescaledb.compress = true, timescaledb.compress_orderby = 'clock,ns ASC', timescaledb.compress_segmentby = 'itemid');
ALTER TABLE history_text SET (timescaledb.compress = true, timescaledb.compress_orderby = 'clock,ns ASC', timescaledb.compress_segmentby = 'itemid');
ALTER TABLE history_uint SET (timescaledb.compress = true, timescaledb.compress_orderby = 'clock,ns ASC', timescaledb.compress_segmentby = 'itemid');
ALTER TABLE trends SET (timescaledb.compress = true, timescaledb.compress_orderby = 'clock ASC', timescaledb.compress_segmentby = 'itemid');
ALTER TABLE trends_uint SET (timescaledb.compress = true, timescaledb.compress_orderby = 'clock ASC', timescaledb.compress_segmentby = 'itemid');
ALTER TABLE proxy_history SET (timescaledb.compress = true, timescaledb.compress_orderby = 'id,clock,ns ASC', timescaledb.compress_segmentby = 'itemid');

SELECT remove_compression_policy('history', true);
SELECT add_compression_policy('history', 
                            date_part('epoch', justify_interval(INTERVAL '7d'))::INTEGER,
                            true,
                            justify_interval(interval '24 hours'),
                            to_char(CURRENT_DATE + INTERVAL'1 day' + TIME'00:01:00', 'yyyy-mm-dd hh24:mi:ss')::TIMESTAMPTZ,
                            'Asia/Shanghai'
);
SELECT remove_compression_policy('history_log', true);
SELECT add_compression_policy('history_log', 
                            date_part('epoch', justify_interval(INTERVAL '7d'))::INTEGER,
                            true,
                            justify_interval(interval '24 hours'),
                            to_char(CURRENT_DATE + INTERVAL'1 day' + TIME'00:01:00', 'yyyy-mm-dd hh24:mi:ss')::TIMESTAMPTZ,
                            'Asia/Shanghai'
);
SELECT remove_compression_policy('history_str', true);
SELECT add_compression_policy('history_str', 
                            date_part('epoch', justify_interval(INTERVAL '7d'))::INTEGER,
                            true,
                            justify_interval(interval '24 hours'),
                            to_char(CURRENT_DATE + INTERVAL'1 day' + TIME'00:01:00', 'yyyy-mm-dd hh24:mi:ss')::TIMESTAMPTZ,
                            'Asia/Shanghai'
);
SELECT remove_compression_policy('history_text', true);
SELECT add_compression_policy('history_text', 
                            date_part('epoch', justify_interval(INTERVAL '7d'))::INTEGER,
                            true,
                            justify_interval(interval '24 hours'),
                            to_char(CURRENT_DATE + INTERVAL'1 day' + TIME'00:01:00', 'yyyy-mm-dd hh24:mi:ss')::TIMESTAMPTZ,
                            'Asia/Shanghai'
);
SELECT remove_compression_policy('history_uint', true);
SELECT add_compression_policy('history_uint', 
                            date_part('epoch', justify_interval(INTERVAL '7d'))::INTEGER,
                            true,
                            justify_interval(interval '24 hours'),
                            to_char(CURRENT_DATE + INTERVAL'1 day' + TIME'00:01:00', 'yyyy-mm-dd hh24:mi:ss')::TIMESTAMPTZ,
                            'Asia/Shanghai'
);
SELECT remove_compression_policy('trends', true);
SELECT add_compression_policy('trends', 
                            date_part('epoch', justify_interval(INTERVAL '7d'))::INTEGER,
                            true,
                            justify_interval(interval '24 hours'),
                            to_char(CURRENT_DATE + INTERVAL'1 day' + TIME'00:01:00', 'yyyy-mm-dd hh24:mi:ss')::TIMESTAMPTZ,
                            'Asia/Shanghai'
);
SELECT remove_compression_policy('trends_uint', true);
SELECT add_compression_policy('trends_uint', 
                            date_part('epoch', justify_interval(INTERVAL '7d'))::INTEGER,
                            true,
                            justify_interval(interval '24 hours'),
                            to_char(CURRENT_DATE + INTERVAL'1 day' + TIME'00:01:00', 'yyyy-mm-dd hh24:mi:ss')::TIMESTAMPTZ,
                            'Asia/Shanghai'
);
SELECT remove_compression_policy('proxy_history', true);
SELECT add_compression_policy('proxy_history', 
                            date_part('epoch', justify_interval(INTERVAL '7d'))::INTEGER,
                            true,
                            justify_interval(interval '24 hours'),
                            to_char(CURRENT_DATE + INTERVAL'1 day' + TIME'00:01:00', 'yyyy-mm-dd hh24:mi:ss')::TIMESTAMPTZ,
                            'Asia/Shanghai'
);

UPDATE config SET db_extension='timescaledb',hk_history_global=1,hk_trends_global=1;
UPDATE config SET compression_status=1,compress_older='7d';

ALTER SYSTEM SET max_connections = '2000';
alter SYSTEM SET log_timezone='Asia/Shanghai';
alter SYSTEM SET timezone='Asia/Shanghai';
alter SYSTEM SET lc_messages='en_US.utf8';
alter SYSTEM SET lc_monetary='en_US.utf8';
alter SYSTEM SET lc_numeric='en_US.utf8';
alter SYSTEM SET lc_time='en_US.utf8';
SELECT pg_reload_conf();