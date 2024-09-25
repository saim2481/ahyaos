CREATE TABLE public."Industry_Sector"
(
    id serial NOT NULL,
    name character varying,
    PRIMARY KEY (id)
);
ALTER TABLE IF EXISTS public."Industry"
    RENAME company_name TO name;