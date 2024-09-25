-- Date: 12-Aug-2024
ALTER TABLE IF EXISTS public."User_Bank_Account_Information"
    ADD COLUMN company_id bigint;
ALTER TABLE IF EXISTS public."User_Bank_Account_Information"
    ADD CONSTRAINT "User_Bank_Account_Information_companyid_fkey" FOREIGN KEY (company_id)
    REFERENCES public."User_Company_Registration_Tax" (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;



ALTER TABLE IF EXISTS public.userfiles DROP COLUMN IF EXISTS user_personal_info_id;

ALTER TABLE IF EXISTS public.userfiles
    ADD COLUMN user_id uuid;
ALTER TABLE IF EXISTS public.userfiles DROP CONSTRAINT IF EXISTS files_user_id;

ALTER TABLE IF EXISTS public.userfiles
    ADD CONSTRAINT files_userid_fkey FOREIGN KEY (user_id)
    REFERENCES public."Users" (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;



CREATE TABLE public."Settings_SSO"
(
    id integer NOT NULL,
    api_key character varying,
    login_url character varying,
    signup_url character varying,
    forgot_pwd_url character varying,
    reset_pwd_url character varying,
    change_pwd_url character varying,
    PRIMARY KEY (id)
);

CREATE TABLE public."Settings_SMTP"
(
    id integer NOT NULL,
    server character varying,
    server_username character varying,
    server_password bit varying,
    PRIMARY KEY (id)
);

CREATE TABLE public."Settings_Session"
(
    id integer NOT NULL,
    secret_key character varying,
    algorithm character varying,
    acs_tkn_expire integer,
    rst_kn_expire integer,
    otp_expire integer,
    PRIMARY KEY (id)
);
