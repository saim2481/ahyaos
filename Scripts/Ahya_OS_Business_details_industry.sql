ALTER TABLE IF EXISTS public.user_business_details DROP COLUMN IF EXISTS industry;

ALTER TABLE IF EXISTS public.user_business_details
    ADD COLUMN industry_id bigint;