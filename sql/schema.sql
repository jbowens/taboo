SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

CREATE TABLE prohibited_words (
    id integer NOT NULL,
    wordid integer,
    word character varying(255)
);

ALTER TABLE public.prohibited_words OWNER TO taboo;

CREATE SEQUENCE prohibited_words_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.prohibited_words_id_seq OWNER TO taboo;

ALTER SEQUENCE prohibited_words_id_seq OWNED BY prohibited_words.id;

CREATE TABLE words (
    id integer NOT NULL,
    word character varying(255),
    skipped integer NOT NULL,
    correct integer NOT NULL
);

ALTER TABLE public.words OWNER TO taboo;

CREATE SEQUENCE words_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER TABLE public.words_id_seq OWNER TO taboo;

ALTER SEQUENCE words_id_seq OWNED BY words.id;

ALTER TABLE ONLY prohibited_words ALTER COLUMN id SET DEFAULT nextval('prohibited_words_id_seq'::regclass);

ALTER TABLE ONLY words ALTER COLUMN id SET DEFAULT nextval('words_id_seq'::regclass);


CREATE INDEX wordid ON prohibited_words USING btree (wordid);

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM taboo;
GRANT ALL ON SCHEMA public TO taboo;
GRANT ALL ON SCHEMA public TO PUBLIC;

REVOKE ALL ON TABLE prohibited_words FROM PUBLIC;
REVOKE ALL ON TABLE prohibited_words FROM taboo;
GRANT ALL ON TABLE prohibited_words TO taboo;

REVOKE ALL ON TABLE words FROM PUBLIC;
REVOKE ALL ON TABLE words FROM taboo;
GRANT ALL ON TABLE words TO taboo;
