CREATE TABLE public.catalogs_locations
(
    id uuid NOT NULL,
    name character varying(255) NOT NULL,
    address character varying(255) NOT NULL,
    aptsuite character varying(255) NOT NULL,
    country_id bigint NOT NULL,
    state_id bigint NOT NULL,
    city_id bigint NOT NULL,
    zip_code character varying(50) NOT NULL,
    description character varying(255) NOT NULL,
    PRIMARY KEY (id),
    CONSTRAINT country_id_fk FOREIGN KEY (country_id)
        REFERENCES public.general_countries (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID,
    CONSTRAINT state_id_fk FOREIGN KEY (state_id)
        REFERENCES public.general_states (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID,
    CONSTRAINT city_id_fk FOREIGN KEY (city_id)
        REFERENCES public.general_cities (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID
);

ALTER TABLE IF EXISTS public.catalogs_locations
    ADD COLUMN created_at timestamp with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP;

ALTER TABLE IF EXISTS public.catalogs_locations
    ADD COLUMN created_by uuid;

ALTER TABLE IF EXISTS public.catalogs_locations
    ADD COLUMN updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP;

ALTER TABLE IF EXISTS public.catalogs_locations
    ADD COLUMN updated_by uuid;

ALTER TABLE IF EXISTS public.catalogs_locations
    ADD COLUMN deleted_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP;

ALTER TABLE IF EXISTS public.catalogs_locations
    ADD COLUMN deleted_by uuid;

ALTER TABLE IF EXISTS public.catalogs_locations
    RENAME updatedby TO updated_by;
ALTER TABLE IF EXISTS public.catalogs_locations
    ADD CONSTRAINT created_at_user_fk FOREIGN KEY (created_by)
    REFERENCES public.users (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;

ALTER TABLE IF EXISTS public.catalogs_locations
    ADD CONSTRAINT updated_by_user_fk FOREIGN KEY (updated_by)
    REFERENCES public.users (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;

ALTER TABLE IF EXISTS public.catalogs_locations
    ADD CONSTRAINT deleted_by_user_fk FOREIGN KEY (deleted_by)
    REFERENCES public.users (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;

ALTER TABLE IF EXISTS public.catalogs_locations
    OWNER to postgres;

