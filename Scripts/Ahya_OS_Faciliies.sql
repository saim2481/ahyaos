CREATE TABLE public.catalogs_facilities
(
    id uuid NOT NULL,
    name character varying(255) NOT NULL,
    category_id bigint NOT NULL,
    sub_category_id bigint NOT NULL,
    location_id uuid NOT NULL,
    internal_id character varying(255) NOT NULL,
    description character varying(500),
    refrigrant_remaining_at_disposal numeric(5, 2) NOT NULL,
    gross_area_id bigint NOT NULL,
    gross_area_unit_id bigint NOT NULL,
    occupancy numeric(5, 2) NOT NULL,
    created_at timestamp with time zone NOT NULL,
    created_by uuid,
    updated_at timestamp with time zone,
    updated_by uuid,
    deleted_at timestamp with time zone,
    deleted_by uuid,
    PRIMARY KEY (id),
    CONSTRAINT category_fk FOREIGN KEY (category_id)
        REFERENCES public.category (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID,
    CONSTRAINT sub_category_fk FOREIGN KEY (sub_category_id)
        REFERENCES public.sub_categories (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID,
    CONSTRAINT location_fk FOREIGN KEY (location_id)
        REFERENCES public.catalogs_locations (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID,
    CONSTRAINT gross_area_fk FOREIGN KEY (gross_area_id)
        REFERENCES public.gross_area (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID,
    CONSTRAINT gross_area_unit_fk FOREIGN KEY (gross_area_unit_id)
        REFERENCES public.gross_area_unit (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID,
    CONSTRAINT created_by_user_fk FOREIGN KEY (created_by)
        REFERENCES public.users (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID,
    CONSTRAINT updated_by_user_fk FOREIGN KEY (updated_by)
        REFERENCES public.users (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID,
    CONSTRAINT deleted_by_user_fk FOREIGN KEY (deleted_by)
        REFERENCES public.users (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID
);

ALTER TABLE IF EXISTS public.catalogs_facilities
    OWNER to postgres;