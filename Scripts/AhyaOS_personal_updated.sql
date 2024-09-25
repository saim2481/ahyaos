-- Enable uuid-ossp extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create tables
CREATE TABLE "Users" (
  "id" UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  "firstName" VARCHAR(50),
  "lastName" VARCHAR(50),
  "companyName" VARCHAR(50),
  "companyEmail" VARCHAR(50),
  "country_id" BIGINT,
  "state_id" BIGINT,
  "city_id" BIGINT,
  "password" VARCHAR(255) NOT NULL,
  "userTypeId" UUID NOT NULL,
  "isReset" BOOLEAN DEFAULT FALSE,
  "ipAddress" VARCHAR(50),
  "thirdPartySubscriptionId" VARCHAR(50),
  "status" INTEGER DEFAULT 4,
  "createdAt" TIMESTAMPTZ,
  "createdBy" UUID,
  "updatedAt" TIMESTAMPTZ,
  "updatedBy" UUID,
  "deletedAt" TIMESTAMPTZ,
  "deletedBy" UUID,
  "signupverifiedby" UUID,
  "profileverifiedby" UUID,
  "remarks" VARCHAR(500)
);

CREATE TABLE "User_History" (
  "id" UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  "Type" VARCHAR(50),
  "statusName" VARCHAR(50),
  "status" INTEGER DEFAULT 1,
  "remarks" VARCHAR(500),
  "createdAt" TIMESTAMPTZ,
  "createdBy" UUID,
  "updatedAt" TIMESTAMPTZ,
  "updatedBy" UUID,
  "deletedAt" TIMESTAMPTZ,
  "deletedBy" UUID
);

CREATE TABLE "User_Role" (
  "id" UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  "typeName" VARCHAR(50),
  "description" VARCHAR(255)
);

CREATE TABLE "User_Info" (
  "userId" UUID NOT NULL,
  "settingId" UUID NOT NULL,
  PRIMARY KEY("userId", "settingId")
);

CREATE TABLE "User_Codes" (
  "id" UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  "userId" UUID NOT NULL,
  "code" VARCHAR(50),
  "identityName" VARCHAR(50),
  "type" VARCHAR(50),
  "status" INTEGER DEFAULT 1,
  "createdAt" TIMESTAMPTZ,
  "createdBy" UUID,
  "updatedAt" TIMESTAMPTZ,
  "updatedBy" UUID,
  "deletedAt" TIMESTAMPTZ,
  "deletedBy" UUID
);

CREATE TABLE "User_Settings" (
  "id" UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  "headerName" VARCHAR(500),
  "sectionName" VARCHAR(500),
  "value" VARCHAR,
  "subValue" VARCHAR,
  "description" VARCHAR,
  "isOtherFields" BOOLEAN,
  "sortOrder" INTEGER,
  "status" INTEGER DEFAULT 1,
  "createdAt" TIMESTAMPTZ,
  "createdBy" UUID,
  "updatedAt" TIMESTAMPTZ,
  "updatedBy" UUID,
  "deletedAt" TIMESTAMPTZ,
  "deletedBy" UUID
);

CREATE TABLE "System_Sessions" (
  "id" UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  "userId" UUID NOT NULL,
  "token" VARCHAR(255) NOT NULL,
  "createdAt" TIMESTAMPTZ,
  "expiresAt" TIMESTAMPTZ
);

CREATE TABLE "User_Role_Permissions" (
  "id" UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  "permissionName" VARCHAR(50) NOT NULL,
  "description" VARCHAR(255),
  "createdAt" TIMESTAMPTZ,
  "createdBy" UUID,
  "updatedAt" TIMESTAMPTZ,
  "updatedBy" UUID,
  "deletedAt" TIMESTAMPTZ,
  "deletedBy" UUID
);

CREATE TABLE "User_Role_Permissions_Mapping" (
  "userTypeId" UUID NOT NULL,
  "permissionId" UUID NOT NULL,
  PRIMARY KEY("userTypeId", "permissionId")
);

CREATE TABLE "User_Business_Details" (
  "id" UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  "userId" UUID NOT NULL,
  "companyLegalName" VARCHAR(100),
  "industry" VARCHAR(100),
  "corporateWebsite" VARCHAR(255),
  "contactNumber" VARCHAR(50),
  "businessAddressLine1" VARCHAR(255),
  "businessAddressLine2" VARCHAR(255),
  "country_id" BIGINT,
  "postalCode" VARCHAR(50),
  "state_id" BIGINT,
  "city_id" BIGINT,
  "createdAt" TIMESTAMPTZ,
  "createdBy" UUID,
  "updatedAt" TIMESTAMPTZ,
  "updatedBy" UUID,
  "deletedAt" TIMESTAMPTZ,
  "deletedBy" UUID
);
CREATE TABLE "User_Personal_Information" (
  "id" UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  "userId" UUID NOT NULL,
  "firstName" VARCHAR(100),
  "lastName" VARCHAR(100),
  "middleName" VARCHAR(100),
  "dateOfBirth" TIMESTAMPTZ,
  "contactNumber" VARCHAR(50),
  "email" VARCHAR(255),
  "gender" VARCHAR(50),
  "maritalStatus" VARCHAR(50),
  "residentialAddressLine1" VARCHAR(255),
  "residentialAddressLine2" VARCHAR(255),
  "country_id" BIGINT,
  "postalCode" VARCHAR(50),
  "state_id" BIGINT,
  "city_id" BIGINT,
  "createdAt" TIMESTAMPTZ,
  "createdBy" UUID,
  "updatedAt" TIMESTAMPTZ,
  "updatedBy" UUID,
  "deletedAt" TIMESTAMPTZ,
  "deletedBy" UUID
);


CREATE TABLE "User_Company_Registration_Tax" (
  "id" UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  "userId" UUID NOT NULL,
  "companyName" VARCHAR(255),
  "companyRegistrationNo" VARCHAR(255),
  "vatNo" VARCHAR(255),
  "taxNo" VARCHAR(255),
  "taxOffice" VARCHAR(255),
  "country_id" BIGINT,
  "createdAt" TIMESTAMPTZ,
  "createdBy" UUID,
  "updatedAt" TIMESTAMPTZ,
  "updatedBy" UUID,
  "deletedAt" TIMESTAMPTZ,
  "deletedBy" UUID
);

CREATE TABLE "User_Bank_Account_Information" (
  "id" UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  "userId" UUID NOT NULL,
  "bankName" VARCHAR(255),
  "bankBranch" VARCHAR(255),
  "accountName" VARCHAR(255),
  "accountNumber" VARCHAR(255),
  "swiftCode" VARCHAR(255),
  "iban" VARCHAR(255),
  "currency" VARCHAR(50),
  "country_id" BIGINT,
  "createdAt" TIMESTAMPTZ,
  "createdBy" UUID,
  "updatedAt" TIMESTAMPTZ,
  "updatedBy" UUID,
  "deletedAt" TIMESTAMPTZ,
  "deletedBy" UUID
);

CREATE TABLE "User_Goals_Targets" (
  "id" UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  "userId" UUID NOT NULL,
  "goalName" VARCHAR(255),
  "targetValue" DECIMAL(18,2),
  "achievedValue" DECIMAL(18,2),
  "status" INTEGER DEFAULT 1,
  "createdAt" TIMESTAMPTZ,
  "createdBy" UUID,
  "updatedAt" TIMESTAMPTZ,
  "updatedBy" UUID,
  "deletedAt" TIMESTAMPTZ,
  "deletedBy" UUID
);

CREATE TABLE "User_Package_Subscription" (
  "id" UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  "userId" UUID NOT NULL,
  "packageName" VARCHAR(255),
  "subscriptionDate" TIMESTAMPTZ,
  "expiryDate" TIMESTAMPTZ,
  "status" INTEGER DEFAULT 1,
  "createdAt" TIMESTAMPTZ,
  "createdBy" UUID,
  "updatedAt" TIMESTAMPTZ,
  "updatedBy" UUID,
  "deletedAt" TIMESTAMPTZ,
  "deletedBy" UUID
);

-- Create the new states table
CREATE TABLE public."General_States" (
    id serial PRIMARY KEY,
    name character varying(255) NOT NULL,
    country_id bigint NOT NULL,
    country_code character(2) NOT NULL,
    fips_code varchar(255),
    iso2 varchar(255),
    type varchar(191),
    latitude numeric(10,8),
    longitude numeric(11,8),
    created_at timestamp without time zone,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    flag smallint DEFAULT 1 NOT NULL,
    "wikiDataId" varchar(255),
    "createdAt" TIMESTAMPTZ,
    "createdBy" UUID,
    "updatedAt" TIMESTAMPTZ,
    "updatedBy" UUID,
    "deletedAt" TIMESTAMPTZ,
    "deletedBy" UUID
);

CREATE TABLE public."General_Countries" (
    id serial PRIMARY KEY,
    name varchar(100) NOT NULL,
    iso3 char(3),
    numeric_code char(3),
    iso2 char(2),
    phonecode varchar(255),
    capital varchar(255),
    currency varchar(255),
    currency_name varchar(255),
    currency_symbol varchar(255),
    tld varchar(255),
    native varchar(255),
    region varchar(255),
    region_id bigint,
    subregion varchar(255),
    subregion_id bigint,
    nationality varchar(255),
    timezones text,
    translations text,
    latitude numeric(10,8),
    longitude numeric(11,8),
    emoji varchar(191),
    "emojiU" varchar(191),
    created_at timestamp without time zone,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    flag smallint DEFAULT 1 NOT NULL,
    "wikiDataId" varchar(255),
    "createdAt" TIMESTAMPTZ,
    "createdBy" UUID,
    "updatedAt" TIMESTAMPTZ,
    "updatedBy" UUID,
    "deletedAt" TIMESTAMPTZ,
    "deletedBy" UUID
);

CREATE TABLE "General_Cities" (
    id serial PRIMARY KEY,
    name varchar(255) NOT NULL,
    state_id bigint NOT NULL,
    state_code varchar(255) NOT NULL,
    country_id bigint NOT NULL,
    country_code char(2) NOT NULL,
    latitude numeric(10,8) NOT NULL,
    longitude numeric(11,8) NOT NULL,
    created_at timestamp DEFAULT '2014-01-01 06:31:01' NOT NULL,
    updated_at timestamp DEFAULT CURRENT_TIMESTAMP NOT NULL,
    flag smallint DEFAULT 1 NOT NULL,
    "wikiDataId" varchar(255),
	"createdAt" TIMESTAMPTZ,
  	"createdBy" UUID,
  	"updatedAt" TIMESTAMPTZ,
  	"updatedBy" UUID,
  	"deletedAt" TIMESTAMPTZ,
  	"deletedBy" UUID
);
-- Table: public.User_Settings_Assignment

-- DROP TABLE IF EXISTS public."User_Settings_Assignment";

CREATE TABLE IF NOT EXISTS public."User_Settings_Assignment"
(
    id uuid NOT NULL DEFAULT uuid_generate_v4(),
    user_id uuid NOT NULL,
    setting_id uuid NOT NULL,
    "createdAt" timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    "createdBy" uuid,
    "updatedAt" timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    "updatedBy" uuid,
    "deletedAt" timestamp with time zone,
    "deletedBy" uuid,
    CONSTRAINT "User_Settings_Assignment_pkey" PRIMARY KEY (id),
    CONSTRAINT unique_user_setting_assignment UNIQUE (user_id, setting_id),
    CONSTRAINT fk_user_settings_assignment_setting FOREIGN KEY (setting_id)
        REFERENCES public."User_Settings" (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE CASCADE,
    CONSTRAINT fk_user_settings_assignment_user FOREIGN KEY (user_id)
        REFERENCES public."Users" (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE CASCADE
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public."User_Settings_Assignment"
    OWNER to postgres;
	
	
	
-- Add foreign keys
ALTER TABLE "Users" ADD FOREIGN KEY ("country_id") REFERENCES "General_Countries" ("id");
ALTER TABLE "Users" ADD FOREIGN KEY ("state_id") REFERENCES "General_States" ("id");
ALTER TABLE "Users" ADD FOREIGN KEY ("city_id") REFERENCES "General_Cities" ("id");
ALTER TABLE "Users" ADD FOREIGN KEY ("userTypeId") REFERENCES "User_Role" ("id");

ALTER TABLE "User_Info" ADD FOREIGN KEY ("userId") REFERENCES "Users" ("id");
ALTER TABLE "User_Info" ADD FOREIGN KEY ("settingId") REFERENCES "User_Settings" ("id");

ALTER TABLE "User_Codes" ADD FOREIGN KEY ("userId") REFERENCES "Users" ("id");

ALTER TABLE "System_Sessions" ADD FOREIGN KEY ("userId") REFERENCES "Users" ("id");

ALTER TABLE "User_Role_Permissions_Mapping" ADD FOREIGN KEY ("userTypeId") REFERENCES "User_Role" ("id");
ALTER TABLE "User_Role_Permissions_Mapping" ADD FOREIGN KEY ("permissionId") REFERENCES "User_Role_Permissions" ("id");

ALTER TABLE "User_Business_Details" ADD FOREIGN KEY ("userId") REFERENCES "Users" ("id");
ALTER TABLE "User_Business_Details" ADD FOREIGN KEY ("country_id") REFERENCES "General_Countries" ("id");
ALTER TABLE "User_Business_Details" ADD FOREIGN KEY ("state_id") REFERENCES "General_States" ("id");
ALTER TABLE "User_Business_Details" ADD FOREIGN KEY ("city_id") REFERENCES "General_Cities" ("id");

ALTER TABLE "User_Personal_Information" ADD FOREIGN KEY ("userId") REFERENCES "Users" ("id");
ALTER TABLE "User_Personal_Information" ADD FOREIGN KEY ("country_id") REFERENCES "General_Countries" ("id");
ALTER TABLE "User_Personal_Information" ADD FOREIGN KEY ("state_id") REFERENCES "General_States" ("id");
ALTER TABLE "User_Personal_Information" ADD FOREIGN KEY ("city_id") REFERENCES "General_Cities" ("id");

ALTER TABLE "User_Company_Registration_Tax" ADD FOREIGN KEY ("userId") REFERENCES "Users" ("id");
ALTER TABLE "User_Company_Registration_Tax" ADD FOREIGN KEY ("country_id") REFERENCES "General_Countries" ("id");

ALTER TABLE "User_Bank_Account_Information" ADD FOREIGN KEY ("userId") REFERENCES "Users" ("id");
ALTER TABLE "User_Bank_Account_Information" ADD FOREIGN KEY ("country_id") REFERENCES "General_Countries" ("id");

ALTER TABLE "User_Goals_Targets" ADD FOREIGN KEY ("userId") REFERENCES "Users" ("id");

ALTER TABLE "User_Package_Subscription" ADD FOREIGN KEY ("userId") REFERENCES "Users" ("id");

ALTER TABLE "General_States" ADD FOREIGN KEY ("country_id") REFERENCES "General_Countries" ("id");

ALTER TABLE "General_Cities" ADD FOREIGN KEY ("state_id") REFERENCES "General_States" ("id");
ALTER TABLE "General_Cities" ADD FOREIGN KEY ("country_id") REFERENCES "General_Countries" ("id");

------------------------------------------------------------------------------------------------------------------------------
-- Add createdBy column to Users table if not exists
ALTER TABLE "Users"
ADD COLUMN IF NOT EXISTS "createdBy" UUID;

-- Add foreign key constraint for createdBy in Users table if not exists
DO $$BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'fk_users_createdby') THEN
        ALTER TABLE "Users"
        ADD CONSTRAINT "fk_users_createdby"
        FOREIGN KEY ("createdBy")
        REFERENCES "Users" ("id");
    END IF;
END$$;

-- Add updatedBy column to Users table if not exists
ALTER TABLE "Users"
ADD COLUMN IF NOT EXISTS "updatedBy" UUID;

-- Add foreign key constraint for updatedBy in Users table if not exists
DO $$BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'fk_users_updatedby') THEN
        ALTER TABLE "Users"
        ADD CONSTRAINT "fk_users_updatedby"
        FOREIGN KEY ("updatedBy")
        REFERENCES "Users" ("id");
    END IF;
END$$;

-- Add deletedBy column to Users table if not exists
ALTER TABLE "Users"
ADD COLUMN IF NOT EXISTS "deletedBy" UUID;

-- Add foreign key constraint for deletedBy in Users table if not exists
DO $$BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'fk_users_deletedby') THEN
        ALTER TABLE "Users"
        ADD CONSTRAINT "fk_users_deletedby"
        FOREIGN KEY ("deletedBy")
        REFERENCES "Users" ("id");
    END IF;
END$$;

-- Add createdBy column to User_History table if not exists
ALTER TABLE "User_History"
ADD COLUMN IF NOT EXISTS "createdBy" UUID;

-- Add foreign key constraint for createdBy in User_History table if not exists
DO $$BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'fk_user_history_createdby') THEN
        ALTER TABLE "User_History"
        ADD CONSTRAINT "fk_user_history_createdby"
        FOREIGN KEY ("createdBy")
        REFERENCES "Users" ("id");
    END IF;
END$$;

-- Add updatedBy column to User_History table if not exists
ALTER TABLE "User_History"
ADD COLUMN IF NOT EXISTS "updatedBy" UUID;

-- Add foreign key constraint for updatedBy in User_History table if not exists
DO $$BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'fk_user_history_updatedby') THEN
        ALTER TABLE "User_History"
        ADD CONSTRAINT "fk_user_history_updatedby"
        FOREIGN KEY ("updatedBy")
        REFERENCES "Users" ("id");
    END IF;
END$$;

-- Add deletedBy column to User_History table if not exists
ALTER TABLE "User_History"
ADD COLUMN IF NOT EXISTS "deletedBy" UUID;

-- Add foreign key constraint for deletedBy in User_History table if not exists
DO $$BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'fk_user_history_deletedby') THEN
        ALTER TABLE "User_History"
        ADD CONSTRAINT "fk_user_history_deletedby"
        FOREIGN KEY ("deletedBy")
        REFERENCES "Users" ("id");
    END IF;
END$$;
