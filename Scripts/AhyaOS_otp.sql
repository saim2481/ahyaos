ALTER TABLE IF EXISTS public."Settings_Session"
    ADD COLUMN otp_max_count integer;

ALTER TABLE IF EXISTS public."Settings_Session"
    ADD COLUMN otp_resend_time integer;

ALTER TABLE IF EXISTS public."Settings_Session"
    ADD COLUMN otp_resend_count_reset_time integer;


-- Table: public.User_Salutation

-- DROP TABLE IF EXISTS public."User_Salutation";

CREATE TABLE IF NOT EXISTS public."User_Salutation"
(
    id integer NOT NULL DEFAULT nextval('user_salutation_id_seq'::regclass),
    salutation character varying(100) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT user_salutation_pkey PRIMARY KEY (id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public."User_Salutation"
    OWNER to postgres;