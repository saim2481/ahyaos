ALTER TABLE IF EXISTS public."User_Personal_Files" DROP COLUMN IF EXISTS user_personal_info_id;





ALTER TABLE IF EXISTS public."User_Personal_Files"
    ADD COLUMN user_id uuid NOT NULL;
ALTER TABLE IF EXISTS public."User_Personal_Files"
    ADD CONSTRAINT user_id_fk FOREIGN KEY (user_id)
    REFERENCES public."Users" (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;

ALTER TABLE IF EXISTS public."User_Personal_Files"
    ADD COLUMN screen_name character varying;

ALTER TABLE IF EXISTS public."User_Personal_Files"
    ADD COLUMN screen_uuid uuid;