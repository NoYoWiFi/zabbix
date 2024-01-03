### syntax=docker/dockerfile:1
FROM timescale/timescaledb:2.13.0-pg15
RUN set -eux && \
echo "sed -i -e \"/^max_connections/s/=.*/= 2000/\" /var/lib/postgresql/data/postgresql.conf" >> /docker-entrypoint-initdb.d/001_timescaledb_tune.sh && \
echo "sed -i -e \"/^log_timezone/s/=.*/= 'Asia\/Shanghai'/\" /var/lib/postgresql/data/postgresql.conf >> /docker-entrypoint-initdb.d/001_timescaledb_tune.sh && \
echo "sed -i -e \"/^timezone/s/=.*/= 'Asia\/Shanghai'/\" /var/lib/postgresql/data/postgresql.conf >> /docker-entrypoint-initdb.d/001_timescaledb_tune.sh && \
echo "sed -i -e \"/^lc_messages/s/=.*/= 'en_US.utf8'/\" /var/lib/postgresql/data/postgresql.conf >> /docker-entrypoint-initdb.d/001_timescaledb_tune.sh && \
echo "sed -i -e \"/^lc_monetary/s/=.*/= 'en_US.utf8'/\" /var/lib/postgresql/data/postgresql.conf >> /docker-entrypoint-initdb.d/001_timescaledb_tune.sh && \
echo "sed -i -e \"/^lc_numeric/s/=.*/= 'en_US.utf8'/\" /var/lib/postgresql/data/postgresql.conf >> /docker-entrypoint-initdb.d/001_timescaledb_tune.sh && \
echo "sed -i -e \"/^lc_time/s/=.*/= 'en_US.utf8'/\" /var/lib/postgresql/data/postgresql.conf EOF >> /docker-entrypoint-initdb.d/001_timescaledb_tune.sh