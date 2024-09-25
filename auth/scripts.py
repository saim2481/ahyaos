# CREATE TABLE UserFiles (
#     id SERIAL PRIMARY KEY,
#     user_personal_info_id INT NOT NULL,
#     file_name VARCHAR(255) NOT NULL,
#     file_path VARCHAR(255) NOT NULL,
#     FOREIGN KEY (user_personal_info_id) REFERENCES UserPersonalInformation(id)
# );


# ALTER TABLE public."User_Company_Registration_Tax" ADD COLUMN company_id VARCHAR(100);

# ALTER TABLE public."User_Personal_Information" ADD COLUMN "salutation" VARCHAR(20);

# ALTER TABLE public."User_Personal_Information" ADD COLUMN "job_title" VARCHAR(100);

# ALTER TABLE public."User_Personal_Information"
# ADD COLUMN "company_id" UUID;

# ALTER TABLE public."User_Personal_Information"
# ADD CONSTRAINT fk_user_company_id
# FOREIGN KEY (company_id)
# REFERENCES public."User_Company_Registration_Tax"(id);
