-- Table: public.catalogs_financed_entity

-- DROP TABLE IF EXISTS public.catalogs_financed_entity;

CREATE TABLE IF NOT EXISTS public.catalogs_financed_entity
(
    id uuid NOT NULL,
    name character varying(255) COLLATE pg_catalog."default" NOT NULL,
    listed boolean NOT NULL,
    description character varying(500) COLLATE pg_catalog."default",
    contact_name character varying(255) COLLATE pg_catalog."default",
    contact_email character varying(255) COLLATE pg_catalog."default" NOT NULL,
    internal_id character varying(255) COLLATE pg_catalog."default" NOT NULL,
    country_id bigint NOT NULL,
    state_id bigint NOT NULL,
    city_id bigint NOT NULL,
    created_by uuid,
    updated_by uuid,
    deleted_by uuid,
    created_at timestamp with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp with time zone,
    deleted_at timestamp with time zone,
    industry_sector_id bigint,
    industry_id bigint,
    sub_industry_id bigint,
    CONSTRAINT catalogs_financed_entity_pkey PRIMARY KEY (id),
    CONSTRAINT catalogs_financed_entity_city_id_fkey FOREIGN KEY (city_id)
        REFERENCES public.general_cities (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT catalogs_financed_entity_country_id_fkey FOREIGN KEY (country_id)
        REFERENCES public.general_countries (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT catalogs_financed_entity_created_by_fkey FOREIGN KEY (created_by)
        REFERENCES public.users (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT catalogs_financed_entity_deleted_by_fkey FOREIGN KEY (deleted_by)
        REFERENCES public.users (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT catalogs_financed_entity_industry_id_fkey FOREIGN KEY (industry_id)
        REFERENCES public.industry (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT catalogs_financed_entity_industry_sector_id_fkey FOREIGN KEY (industry_sector_id)
        REFERENCES public.industry_sector (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT catalogs_financed_entity_state_id_fkey FOREIGN KEY (state_id)
        REFERENCES public.general_states (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT catalogs_financed_entity_sub_industry_id_fkey FOREIGN KEY (sub_industry_id)
        REFERENCES public.sub_industry (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT catalogs_financed_entity_updated_by_fkey FOREIGN KEY (updated_by)
        REFERENCES public.users (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.catalogs_financed_entity
    OWNER to postgres;