-- Table: public.User_Role

-- DROP TABLE IF EXISTS public."User_Role";

CREATE TABLE IF NOT EXISTS public."User_Role"
(
    id uuid NOT NULL DEFAULT uuid_generate_v4(),
    "typeName" character varying(50) COLLATE pg_catalog."default",
    description character varying(255) COLLATE pg_catalog."default",
    CONSTRAINT "User_Role_pkey" PRIMARY KEY (id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public."User_Role"
    OWNER to postgres;
	
-------------------- Insert statement for all users
INSERT INTO public."User_Role" ("typeName", description) 
VALUES 
    ('Admin', 'Administrative user with full access'),
    ('SuperAdmin', 'Super user with highest privileges'),
    ('User', 'Standard user with basic access');
	