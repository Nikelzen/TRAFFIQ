-- Run as a PostgreSQL administrator. Replace the password before use.
CREATE ROLE traffiq LOGIN PASSWORD 'REPLACE_WITH_A_LONG_RANDOM_PASSWORD';
CREATE DATABASE traffiq OWNER traffiq;
GRANT ALL PRIVILEGES ON DATABASE traffiq TO traffiq;
