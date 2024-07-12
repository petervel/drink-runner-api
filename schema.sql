-- To (re)create a database with this schema, use the following shell command:
-- poetry run postgresqlite < schema.sql 

DROP SCHEMA public CASCADE;
CREATE SCHEMA public;


CREATE TABLE games (
    id serial NOT NULL,
    user_id integer NOT NULL,
    secret text NOT NULL,
    "time" timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    result integer
);


CREATE TABLE guesses (
    id serial NOT NULL,
    game_id integer NOT NULL,
    word text NOT NULL,
    "time" timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL
);


CREATE TABLE users (
    id serial NOT NULL,
    name text NOT NULL,
    password text NOT NULL
);
