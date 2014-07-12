CREATE TABLE prohibited_words (
    pwid serial,
    wid integer,
    word character varying(255),
    rank integer not null default 1
);
ALTER TABLE public.prohibited_words OWNER TO prod;

CREATE TABLE words (
    wid serial,
    word character varying(255) UNIQUE,
    skipped integer NOT NULL DEFAULT 0,
    correct integer NOT NULL DEFAULT 0,
    verified boolean NOT NULL DEFAULT FALSE,
    source character varying(255)
);
ALTER TABLE public.words OWNER TO prod;
CREATE INDEX wordid ON prohibited_words USING btree (wordid);

CREATE TYPE client_type AS ENUM ('web', 'iOS');
CREATE TABLE sessions (
    id serial,
    key character varying(255),
    source client_type,
    started_time timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
    ipaddress bigint NOT NULL
);
CREATE INDEX key ON sessions USING btree (key);
ALTER TABLE public.sessions OWNER TO prod;

CREATE TABLE installs (
    id serial,
    key character varying(255),
    install_time timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
);
ALTER TABLE public.installs OWNER TO prod;

CREATE TABLE word_interactions (
    id serial,
    wordid integer,
    installid integer,
    skipped boolean NOT NULL DEFAULT FALSE,
    save_date timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
);
ALTER TABLE public.word_interactions OWNER TO prod;
