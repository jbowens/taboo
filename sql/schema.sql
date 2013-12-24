CREATE TABLE prohibited_words (
    id serial,
    wordid integer,
    word character varying(255)
);
ALTER TABLE public.prohibited_words OWNER TO prod;

CREATE TABLE words (
    id serial,
    word character varying(255) UNIQUE,
    skipped integer NOT NULL DEFAULT 0,
    correct integer NOT NULL DEFAULT 0,
    verified boolean NOT NULL DEFAULT FALSE
);
ALTER TABLE public.words OWNER TO prod;

CREATE INDEX wordid ON prohibited_words USING btree (wordid);
