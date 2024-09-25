ALTER TABLE IF EXISTS public."System_Sessions"
    ADD COLUMN last_resend_count bigint;

ALTER TABLE IF EXISTS public."System_Sessions"
    ADD COLUMN last_resend_at time with time zone;