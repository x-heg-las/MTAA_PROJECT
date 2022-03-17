CREATE TABLE file_types (
    id integer NOT NULL,
    name character varying(32)
);

CREATE SEQUENCE file_types_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE file_types_id_seq OWNED BY file_types.id;

CREATE TABLE files (
    id integer NOT NULL,
    data bytea,
    file_type_id integer NOT NULL,
    size integer NOT NULL,
    created_at timestamp without time zone,
    updated_at timestamp without time zone
);

CREATE SEQUENCE files_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE files_id_seq OWNED BY files.id;

CREATE TABLE request_types (
    id integer NOT NULL,
    name character varying(120)
);

CREATE SEQUENCE request_types_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE request_types_id_seq OWNED BY request_types.id;

CREATE TABLE requests (
    id integer NOT NULL,
    title character varying(120) NOT NULL,
    answered_by_user_id integer,
    user_id integer NOT NULL,
    request_type_id integer NOT NULL,
    file_id integer,
    description text,
    call_requested boolean,
    created_at timestamp without time zone,
    updated_at timestamp without time zone,
    deleted_at timestamp without time zone
);

CREATE SEQUENCE requests_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE requests_id_seq OWNED BY requests.id;

CREATE TABLE user_types (
    id integer NOT NULL,
    name character varying(64)
);

CREATE SEQUENCE user_types_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE user_types_id_seq OWNED BY user_types.id;

CREATE TABLE users (
    id integer NOT NULL,
    username character varying(120) NOT NULL,
    profile_img_file_id integer,
    user_type_id integer NOT NULL,
    password character varying(64) NOT NULL,
    full_name character varying(120) NOT NULL,
    phone_number character varying(16),
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL,
    deleted_at timestamp without time zone
);

CREATE SEQUENCE users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE users_id_seq OWNED BY users.id;

ALTER TABLE ONLY file_types ALTER COLUMN id SET DEFAULT nextval('file_types_id_seq'::regclass);

ALTER TABLE ONLY files ALTER COLUMN id SET DEFAULT nextval('files_id_seq'::regclass);

ALTER TABLE ONLY request_types ALTER COLUMN id SET DEFAULT nextval('request_types_id_seq'::regclass);

ALTER TABLE ONLY requests ALTER COLUMN id SET DEFAULT nextval('requests_id_seq'::regclass);

ALTER TABLE ONLY user_types ALTER COLUMN id SET DEFAULT nextval('user_types_id_seq'::regclass);

ALTER TABLE ONLY users ALTER COLUMN id SET DEFAULT nextval('users_id_seq'::regclass);

SELECT pg_catalog.setval('file_types_id_seq', 1, false);

SELECT pg_catalog.setval('files_id_seq', 1, false);

SELECT pg_catalog.setval('request_types_id_seq', 1, false);

SELECT pg_catalog.setval('requests_id_seq', 1, false);

SELECT pg_catalog.setval('user_types_id_seq', 1, false);

SELECT pg_catalog.setval('users_id_seq', 1, false);

ALTER TABLE ONLY file_types
    ADD CONSTRAINT file_types_pkey PRIMARY KEY (id);

ALTER TABLE ONLY files
    ADD CONSTRAINT files_pkey PRIMARY KEY (id);

ALTER TABLE ONLY request_types
    ADD CONSTRAINT request_types_pkey PRIMARY KEY (id);

ALTER TABLE ONLY requests
    ADD CONSTRAINT requests_pkey PRIMARY KEY (id);

ALTER TABLE ONLY user_types
    ADD CONSTRAINT user_types_pkey PRIMARY KEY (id);

ALTER TABLE ONLY users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);

ALTER TABLE ONLY users
    ADD CONSTRAINT users_username_key UNIQUE (username);

ALTER TABLE ONLY files
    ADD CONSTRAINT files_file_type_id_fkey FOREIGN KEY (file_type_id) REFERENCES request_types(id);

ALTER TABLE ONLY requests
    ADD CONSTRAINT requests_answered_by_user_id_fkey FOREIGN KEY (answered_by_user_id) REFERENCES users(id);

ALTER TABLE ONLY requests
    ADD CONSTRAINT requests_file_id_fkey FOREIGN KEY (file_id) REFERENCES files(id);

ALTER TABLE ONLY requests
    ADD CONSTRAINT requests_request_type_id_fkey FOREIGN KEY (request_type_id) REFERENCES request_types(id);

ALTER TABLE ONLY requests
    ADD CONSTRAINT requests_user_id_fkey FOREIGN KEY (user_id) REFERENCES users(id);

ALTER TABLE ONLY users
    ADD CONSTRAINT users_profile_img_file_id_fkey FOREIGN KEY (profile_img_file_id) REFERENCES files(id);

ALTER TABLE ONLY users
    ADD CONSTRAINT users_user_type_id_fkey FOREIGN KEY (user_type_id) REFERENCES user_types(id);
