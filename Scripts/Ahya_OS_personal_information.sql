ALTER TABLE IF EXISTS public."User_Personal_Information" DROP COLUMN IF EXISTS salutation;


ALTER TABLE IF EXISTS public."User_Personal_Information"
    ADD COLUMN salutation_id bigint;
ALTER TABLE IF EXISTS public."User_Personal_Information"
    ADD CONSTRAINT fk_user_salutation_id FOREIGN KEY (salutation_id)
    REFERENCES public."User_Salutation" (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS public."General_Countries" DROP COLUMN IF EXISTS created_at;

ALTER TABLE IF EXISTS public."General_Countries" DROP COLUMN IF EXISTS updated_at;

ALTER TABLE IF EXISTS public."General_Cities" DROP COLUMN IF EXISTS created_at;

ALTER TABLE IF EXISTS public."General_Cities" DROP COLUMN IF EXISTS updated_at;

ALTER TABLE IF EXISTS public."General_States" DROP COLUMN IF EXISTS created_at;

ALTER TABLE IF EXISTS public."General_States" DROP COLUMN IF EXISTS updated_at;