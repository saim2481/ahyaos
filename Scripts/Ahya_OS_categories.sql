-- Table: public.category

-- DROP TABLE IF EXISTS public.category;

CREATE TABLE IF NOT EXISTS public.category
(
    id integer NOT NULL DEFAULT nextval('category_id_seq'::regclass),
    name character varying(50) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT category_pkey PRIMARY KEY (id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.category
    OWNER to postgres;


CREATE TABLE public.sub_categories
(
    id serial NOT NULL,
    name character varying(50) NOT NULL,
    category_id serial NOT NULL,
    PRIMARY KEY (id),
    CONSTRAINT category_fk FOREIGN KEY (category_id)
        REFERENCES public.category (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID
);

ALTER TABLE IF EXISTS public.sub_categories
    OWNER to postgres;


ALTER TABLE IF EXISTS public.category
    ADD COLUMN created_at timestamp with time zone NOT NULL;

ALTER TABLE IF EXISTS public.category
    ADD COLUMN created_by uuid;

ALTER TABLE IF EXISTS public.category
    ADD COLUMN updated_at timestamp with time zone;

ALTER TABLE IF EXISTS public.category
    ADD COLUMN updated_by uuid;

ALTER TABLE IF EXISTS public.category
    ADD COLUMN deleted_at timestamp with time zone;

ALTER TABLE IF EXISTS public.category
    ADD COLUMN deleted_by uuid;
ALTER TABLE IF EXISTS public.category
    ADD CONSTRAINT created_by_fk_user FOREIGN KEY (created_by)
    REFERENCES public.users (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;

ALTER TABLE IF EXISTS public.category
    ADD CONSTRAINT updated_by_fk_user FOREIGN KEY (updated_by)
    REFERENCES public.users (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;

ALTER TABLE IF EXISTS public.category
    ADD CONSTRAINT deleted_by_fk_user FOREIGN KEY (deleted_by)
    REFERENCES public.users (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;