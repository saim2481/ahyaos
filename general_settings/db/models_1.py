from typing import List, Optional

from sqlalchemy import BigInteger, Boolean, CHAR, Column, DateTime, ForeignKeyConstraint, Integer, Numeric, PrimaryKeyConstraint, SmallInteger, String, Table, Text, UniqueConstraint, Uuid, text
from sqlalchemy.orm import Mapped, declarative_base, mapped_column, relationship
from sqlalchemy.orm.base import Mapped

Base = declarative_base()
metadata = Base.metadata


class GeneralCountries(Base):
    __tablename__ = 'General_Countries'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='General_Countries_pkey'),
    )

    id = mapped_column(Integer)
    name = mapped_column(String(100), nullable=False)
    updated_at = mapped_column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    flag = mapped_column(SmallInteger, nullable=False, server_default=text('1'))
    iso3 = mapped_column(CHAR(3))
    numeric_code = mapped_column(CHAR(3))
    iso2 = mapped_column(CHAR(2))
    phonecode = mapped_column(String(255))
    capital = mapped_column(String(255))
    currency = mapped_column(String(255))
    currency_name = mapped_column(String(255))
    currency_symbol = mapped_column(String(255))
    tld = mapped_column(String(255))
    native = mapped_column(String(255))
    region = mapped_column(String(255))
    region_id = mapped_column(BigInteger)
    subregion = mapped_column(String(255))
    subregion_id = mapped_column(BigInteger)
    nationality = mapped_column(String(255))
    timezones = mapped_column(Text)
    translations = mapped_column(Text)
    latitude = mapped_column(Numeric(10, 8))
    longitude = mapped_column(Numeric(11, 8))
    emoji = mapped_column(String(191))
    emojiU = mapped_column(String(191))
    created_at = mapped_column(DateTime)
    wikiDataId = mapped_column(String(255))
    createdAt = mapped_column(DateTime(True))
    createdBy = mapped_column(Uuid)
    updatedAt = mapped_column(DateTime(True))
    updatedBy = mapped_column(Uuid)
    deletedAt = mapped_column(DateTime(True))
    deletedBy = mapped_column(Uuid)

    General_States: Mapped[List['GeneralStates']] = relationship('GeneralStates', uselist=True, back_populates='country')
    General_Cities: Mapped[List['GeneralCities']] = relationship('GeneralCities', uselist=True, back_populates='country')
    Users: Mapped[List['Users']] = relationship('Users', uselist=True, back_populates='country')
    User_Business_Details: Mapped[List['UserBusinessDetails']] = relationship('UserBusinessDetails', uselist=True, back_populates='country')
    User_Company_Registration_Tax: Mapped[List['UserCompanyRegistrationTax']] = relationship('UserCompanyRegistrationTax', uselist=True, back_populates='country')
    User_Bank_Account_Information: Mapped[List['UserBankAccountInformation']] = relationship('UserBankAccountInformation', uselist=True, back_populates='country')
    User_Personal_Information: Mapped[List['UserPersonalInformation']] = relationship('UserPersonalInformation', uselist=True, back_populates='country')


class IndustrySector(Base):
    __tablename__ = 'IndustrySector'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='IndustrySector_pkey'),
    )

    id = mapped_column(Integer)
    name = mapped_column(String(255), nullable=False)

    Industry: Mapped[List['Industry']] = relationship('Industry', uselist=True, back_populates='sector')


class SettingsSMTP(Base):
    __tablename__ = 'Settings_SMTP'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='Settings_SMTP_pkey'),
    )

    id = mapped_column(Integer)
    server = mapped_column(String)
    server_username = mapped_column(String)
    server_password = mapped_column(String)


class SettingsSSO(Base):
    __tablename__ = 'Settings_SSO'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='Settings_SSO_pkey'),
    )

    id = mapped_column(Integer)
    api_key = mapped_column(String)
    login_url = mapped_column(String)
    signup_url = mapped_column(String)
    forgot_pwd_url = mapped_column(String)
    reset_pwd_url = mapped_column(String)
    change_pwd_url = mapped_column(String)


class SettingsSession(Base):
    __tablename__ = 'Settings_Session'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='Settings_Session_pkey'),
    )

    id = mapped_column(Integer)
    secret_key = mapped_column(String)
    algorithm = mapped_column(String)
    acs_tkn_expire = mapped_column(Integer)
    rst_tkn_expire = mapped_column(Integer)
    otp_expire = mapped_column(Integer)


class UserRole(Base):
    __tablename__ = 'User_Role'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='User_Role_pkey'),
    )

    id = mapped_column(Uuid, server_default=text('uuid_generate_v4()'))
    typeName = mapped_column(String(50))
    description = mapped_column(String(255))

    User_Role_Permissions: Mapped['UserRolePermissions'] = relationship('UserRolePermissions', secondary='User_Role_Permissions_Mapping', back_populates='User_Role')
    Users: Mapped[List['Users']] = relationship('Users', uselist=True, back_populates='User_Role')


class UserRolePermissions(Base):
    __tablename__ = 'User_Role_Permissions'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='User_Role_Permissions_pkey'),
    )

    id = mapped_column(Uuid, server_default=text('uuid_generate_v4()'))
    permissionName = mapped_column(String(50), nullable=False)
    description = mapped_column(String(255))
    createdAt = mapped_column(DateTime(True))
    createdBy = mapped_column(Uuid)
    updatedAt = mapped_column(DateTime(True))
    updatedBy = mapped_column(Uuid)
    deletedAt = mapped_column(DateTime(True))
    deletedBy = mapped_column(Uuid)

    User_Role: Mapped['UserRole'] = relationship('UserRole', secondary='User_Role_Permissions_Mapping', back_populates='User_Role_Permissions')


class UserSettings(Base):
    __tablename__ = 'User_Settings'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='User_Settings_pkey'),
    )

    id = mapped_column(Uuid, server_default=text('uuid_generate_v4()'))
    headerName = mapped_column(String(500))
    sectionName = mapped_column(String(500))
    value = mapped_column(String)
    subValue = mapped_column(String)
    description = mapped_column(String)
    isOtherFields = mapped_column(Boolean)
    sortOrder = mapped_column(Integer)
    status = mapped_column(Integer, server_default=text('1'))
    createdAt = mapped_column(DateTime(True))
    createdBy = mapped_column(Uuid)
    updatedAt = mapped_column(DateTime(True))
    updatedBy = mapped_column(Uuid)
    deletedAt = mapped_column(DateTime(True))
    deletedBy = mapped_column(Uuid)

    Users: Mapped['Users'] = relationship('Users', secondary='User_Info', back_populates='User_Settings')
    User_Settings_Assignment: Mapped[List['UserSettingsAssignment']] = relationship('UserSettingsAssignment', uselist=True, back_populates='setting')


class GeneralStates(Base):
    __tablename__ = 'General_States'
    __table_args__ = (
        ForeignKeyConstraint(['country_id'], ['General_Countries.id'], name='General_States_country_id_fkey'),
        PrimaryKeyConstraint('id', name='General_States_pkey')
    )

    id = mapped_column(Integer)
    name = mapped_column(String(255), nullable=False)
    country_id = mapped_column(BigInteger, nullable=False)
    country_code = mapped_column(CHAR(2), nullable=False)
    updated_at = mapped_column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    flag = mapped_column(SmallInteger, nullable=False, server_default=text('1'))
    fips_code = mapped_column(String(255))
    iso2 = mapped_column(String(255))
    type = mapped_column(String(191))
    latitude = mapped_column(Numeric(10, 8))
    longitude = mapped_column(Numeric(11, 8))
    created_at = mapped_column(DateTime)
    wikiDataId = mapped_column(String(255))
    createdAt = mapped_column(DateTime(True))
    createdBy = mapped_column(Uuid)
    updatedAt = mapped_column(DateTime(True))
    updatedBy = mapped_column(Uuid)
    deletedAt = mapped_column(DateTime(True))
    deletedBy = mapped_column(Uuid)

    country: Mapped['GeneralCountries'] = relationship('GeneralCountries', back_populates='General_States')
    General_Cities: Mapped[List['GeneralCities']] = relationship('GeneralCities', uselist=True, back_populates='state')
    Users: Mapped[List['Users']] = relationship('Users', uselist=True, back_populates='state')
    User_Business_Details: Mapped[List['UserBusinessDetails']] = relationship('UserBusinessDetails', uselist=True, back_populates='state')
    User_Personal_Information: Mapped[List['UserPersonalInformation']] = relationship('UserPersonalInformation', uselist=True, back_populates='state')


class Industry(Base):
    __tablename__ = 'Industry'
    __table_args__ = (
        ForeignKeyConstraint(['sector_id'], ['IndustrySector.id'], name='Industry_sector_id_fkey'),
        PrimaryKeyConstraint('id', name='Industry_pkey')
    )

    id = mapped_column(Integer)
    company_name = mapped_column(String(255), nullable=False)
    sector_id = mapped_column(Integer, nullable=False)

    sector: Mapped['IndustrySector'] = relationship('IndustrySector', back_populates='Industry')


t_User_Role_Permissions_Mapping = Table(
    'User_Role_Permissions_Mapping', metadata,
    Column('userTypeId', Uuid, nullable=False),
    Column('permissionId', Uuid, nullable=False),
    ForeignKeyConstraint(['permissionId'], ['User_Role_Permissions.id'], name='User_Role_Permissions_Mapping_permissionId_fkey'),
    ForeignKeyConstraint(['userTypeId'], ['User_Role.id'], name='User_Role_Permissions_Mapping_userTypeId_fkey'),
    PrimaryKeyConstraint('userTypeId', 'permissionId', name='User_Role_Permissions_Mapping_pkey')
)


class GeneralCities(Base):
    __tablename__ = 'General_Cities'
    __table_args__ = (
        ForeignKeyConstraint(['country_id'], ['General_Countries.id'], name='General_Cities_country_id_fkey'),
        ForeignKeyConstraint(['state_id'], ['General_States.id'], name='General_Cities_state_id_fkey'),
        PrimaryKeyConstraint('id', name='General_Cities_pkey')
    )

    id = mapped_column(Integer)
    name = mapped_column(String(255), nullable=False)
    state_id = mapped_column(BigInteger, nullable=False)
    state_code = mapped_column(String(255), nullable=False)
    country_id = mapped_column(BigInteger, nullable=False)
    country_code = mapped_column(CHAR(2), nullable=False)
    latitude = mapped_column(Numeric(10, 8), nullable=False)
    longitude = mapped_column(Numeric(11, 8), nullable=False)
    created_at = mapped_column(DateTime, nullable=False, server_default=text("'2014-01-01 06:31:01'::timestamp without time zone"))
    updated_at = mapped_column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    flag = mapped_column(SmallInteger, nullable=False, server_default=text('1'))
    wikiDataId = mapped_column(String(255))
    createdAt = mapped_column(DateTime(True))
    createdBy = mapped_column(Uuid)
    updatedAt = mapped_column(DateTime(True))
    updatedBy = mapped_column(Uuid)
    deletedAt = mapped_column(DateTime(True))
    deletedBy = mapped_column(Uuid)

    country: Mapped['GeneralCountries'] = relationship('GeneralCountries', back_populates='General_Cities')
    state: Mapped['GeneralStates'] = relationship('GeneralStates', back_populates='General_Cities')
    Users: Mapped[List['Users']] = relationship('Users', uselist=True, back_populates='city')
    User_Business_Details: Mapped[List['UserBusinessDetails']] = relationship('UserBusinessDetails', uselist=True, back_populates='city')
    User_Bank_Account_Information: Mapped[List['UserBankAccountInformation']] = relationship('UserBankAccountInformation', uselist=True, back_populates='city')
    User_Personal_Information: Mapped[List['UserPersonalInformation']] = relationship('UserPersonalInformation', uselist=True, back_populates='city')


class Users(Base):
    __tablename__ = 'Users'
    __table_args__ = (
        ForeignKeyConstraint(['city_id'], ['General_Cities.id'], name='Users_city_id_fkey'),
        ForeignKeyConstraint(['country_id'], ['General_Countries.id'], name='Users_country_id_fkey'),
        ForeignKeyConstraint(['createdBy'], ['Users.id'], name='fk_users_createdby'),
        ForeignKeyConstraint(['deletedBy'], ['Users.id'], name='fk_users_deletedby'),
        ForeignKeyConstraint(['state_id'], ['General_States.id'], name='Users_state_id_fkey'),
        ForeignKeyConstraint(['updatedBy'], ['Users.id'], name='fk_users_updatedby'),
        ForeignKeyConstraint(['userTypeId'], ['User_Role.id'], name='Users_userTypeId_fkey'),
        PrimaryKeyConstraint('id', name='Users_pkey')
    )

    id = mapped_column(Uuid, server_default=text('uuid_generate_v4()'))
    userTypeId = mapped_column(Uuid, nullable=False)
    firstName = mapped_column(String(50))
    lastName = mapped_column(String(50))
    companyName = mapped_column(String(50))
    companyEmail = mapped_column(String(50))
    country_id = mapped_column(BigInteger)
    state_id = mapped_column(BigInteger)
    city_id = mapped_column(BigInteger)
    password = mapped_column(String(255))
    isReset = mapped_column(Boolean, server_default=text('false'))
    ipAddress = mapped_column(String(50))
    thirdPartySubscriptionId = mapped_column(String(50))
    status = mapped_column(Integer, server_default=text('4'))
    createdAt = mapped_column(DateTime(True))
    createdBy = mapped_column(Uuid)
    updatedAt = mapped_column(DateTime(True))
    updatedBy = mapped_column(Uuid)
    deletedAt = mapped_column(DateTime(True))
    deletedBy = mapped_column(Uuid)
    signupverifiedby = mapped_column(Uuid)
    profileverifiedby = mapped_column(Uuid)
    remarks = mapped_column(String(500))
    reset_token = mapped_column(String)
    reset_token_expiration = mapped_column(DateTime)
    sso_id = mapped_column(String(50))

    User_Settings: Mapped['UserSettings'] = relationship('UserSettings', secondary='User_Info', back_populates='Users')
    city: Mapped[Optional['GeneralCities']] = relationship('GeneralCities', back_populates='Users')
    country: Mapped[Optional['GeneralCountries']] = relationship('GeneralCountries', back_populates='Users')
    Users: Mapped[Optional['Users']] = relationship('Users', remote_side=[id], foreign_keys=[createdBy], back_populates='Users_reverse')
    Users_reverse: Mapped[List['Users']] = relationship('Users', uselist=True, remote_side=[createdBy], foreign_keys=[createdBy], back_populates='Users')
    Users_: Mapped[Optional['Users']] = relationship('Users', remote_side=[id], foreign_keys=[deletedBy], back_populates='Users__reverse')
    Users__reverse: Mapped[List['Users']] = relationship('Users', uselist=True, remote_side=[deletedBy], foreign_keys=[deletedBy], back_populates='Users_')
    state: Mapped[Optional['GeneralStates']] = relationship('GeneralStates', back_populates='Users')
    Users1: Mapped[Optional['Users']] = relationship('Users', remote_side=[id], foreign_keys=[updatedBy], back_populates='Users1_reverse')
    Users1_reverse: Mapped[List['Users']] = relationship('Users', uselist=True, remote_side=[updatedBy], foreign_keys=[updatedBy], back_populates='Users1')
    User_Role: Mapped['UserRole'] = relationship('UserRole', back_populates='Users')
    System_Sessions: Mapped[List['SystemSessions']] = relationship('SystemSessions', uselist=True, back_populates='Users_')
    User_Business_Details: Mapped[List['UserBusinessDetails']] = relationship('UserBusinessDetails', uselist=True, back_populates='Users_')
    User_Codes: Mapped[List['UserCodes']] = relationship('UserCodes', uselist=True, back_populates='Users_')
    User_Company_Registration_Tax: Mapped[List['UserCompanyRegistrationTax']] = relationship('UserCompanyRegistrationTax', uselist=True, back_populates='Users_')
    User_Goals_Targets: Mapped[List['UserGoalsTargets']] = relationship('UserGoalsTargets', uselist=True, back_populates='Users_')
    User_History: Mapped[List['UserHistory']] = relationship('UserHistory', uselist=True, foreign_keys='[UserHistory.createdBy]', back_populates='Users_')
    User_History_: Mapped[List['UserHistory']] = relationship('UserHistory', uselist=True, foreign_keys='[UserHistory.deletedBy]', back_populates='Users1')
    User_History1: Mapped[List['UserHistory']] = relationship('UserHistory', uselist=True, foreign_keys='[UserHistory.updatedBy]', back_populates='Users2')
    User_Package_Subscription: Mapped[List['UserPackageSubscription']] = relationship('UserPackageSubscription', uselist=True, back_populates='Users_')
    User_Personal_Files: Mapped[List['UserPersonalFiles']] = relationship('UserPersonalFiles', uselist=True, back_populates='user')
    User_Settings_Assignment: Mapped[List['UserSettingsAssignment']] = relationship('UserSettingsAssignment', uselist=True, back_populates='user')
    userfiles: Mapped[List['Userfiles']] = relationship('Userfiles', uselist=True, back_populates='user')
    User_Bank_Account_Information: Mapped[List['UserBankAccountInformation']] = relationship('UserBankAccountInformation', uselist=True, back_populates='Users_')
    User_Personal_Information: Mapped[List['UserPersonalInformation']] = relationship('UserPersonalInformation', uselist=True, back_populates='Users_')


class SystemSessions(Base):
    __tablename__ = 'System_Sessions'
    __table_args__ = (
        ForeignKeyConstraint(['userId'], ['Users.id'], name='System_Sessions_userId_fkey'),
        PrimaryKeyConstraint('id', name='System_Sessions_pkey')
    )

    id = mapped_column(Uuid, server_default=text('uuid_generate_v4()'))
    userId = mapped_column(Uuid, nullable=False)
    token = mapped_column(String(255), nullable=False)
    createdAt = mapped_column(DateTime(True))
    expiresAt = mapped_column(DateTime(True))

    Users_: Mapped['Users'] = relationship('Users', back_populates='System_Sessions')


class UserBusinessDetails(Base):
    __tablename__ = 'User_Business_Details'
    __table_args__ = (
        ForeignKeyConstraint(['city_id'], ['General_Cities.id'], name='User_Business_Details_city_id_fkey'),
        ForeignKeyConstraint(['country_id'], ['General_Countries.id'], name='User_Business_Details_country_id_fkey'),
        ForeignKeyConstraint(['state_id'], ['General_States.id'], name='User_Business_Details_state_id_fkey'),
        ForeignKeyConstraint(['userId'], ['Users.id'], name='User_Business_Details_userId_fkey'),
        PrimaryKeyConstraint('id', name='User_Business_Details_pkey')
    )

    id = mapped_column(Uuid, server_default=text('uuid_generate_v4()'))
    userId = mapped_column(Uuid, nullable=False)
    companyLegalName = mapped_column(String(100))
    industry = mapped_column(String(100))
    corporateWebsite = mapped_column(String(255))
    contactNumber = mapped_column(String(50))
    businessAddressLine1 = mapped_column(String(255))
    businessAddressLine2 = mapped_column(String(255))
    country_id = mapped_column(BigInteger)
    postalCode = mapped_column(String(50))
    state_id = mapped_column(BigInteger)
    city_id = mapped_column(BigInteger)
    createdAt = mapped_column(DateTime(True))
    createdBy = mapped_column(Uuid)
    updatedAt = mapped_column(DateTime(True))
    updatedBy = mapped_column(Uuid)
    deletedAt = mapped_column(DateTime(True))
    deletedBy = mapped_column(Uuid)

    city: Mapped[Optional['GeneralCities']] = relationship('GeneralCities', back_populates='User_Business_Details')
    country: Mapped[Optional['GeneralCountries']] = relationship('GeneralCountries', back_populates='User_Business_Details')
    state: Mapped[Optional['GeneralStates']] = relationship('GeneralStates', back_populates='User_Business_Details')
    Users_: Mapped['Users'] = relationship('Users', back_populates='User_Business_Details')


class UserCodes(Base):
    __tablename__ = 'User_Codes'
    __table_args__ = (
        ForeignKeyConstraint(['userId'], ['Users.id'], name='User_Codes_userId_fkey'),
        PrimaryKeyConstraint('id', name='User_Codes_pkey')
    )

    id = mapped_column(Uuid, server_default=text('uuid_generate_v4()'))
    userId = mapped_column(Uuid, nullable=False)
    code = mapped_column(String(50))
    identityName = mapped_column(String(50))
    type = mapped_column(String(50))
    status = mapped_column(Integer, server_default=text('1'))
    createdAt = mapped_column(DateTime(True))
    createdBy = mapped_column(Uuid)
    updatedAt = mapped_column(DateTime(True))
    updatedBy = mapped_column(Uuid)
    deletedAt = mapped_column(DateTime(True))
    deletedBy = mapped_column(Uuid)

    Users_: Mapped['Users'] = relationship('Users', back_populates='User_Codes')


class UserCompanyRegistrationTax(Base):
    __tablename__ = 'User_Company_Registration_Tax'
    __table_args__ = (
        ForeignKeyConstraint(['country_id'], ['General_Countries.id'], name='User_Company_Registration_Tax_country_id_fkey'),
        ForeignKeyConstraint(['userId'], ['Users.id'], name='User_Company_Registration_Tax_userId_fkey'),
        PrimaryKeyConstraint('id', name='User_Company_Registration_Tax_pkey')
    )

    id = mapped_column(Uuid, server_default=text('uuid_generate_v4()'))
    userId = mapped_column(Uuid, nullable=False)
    companyName = mapped_column(String(255))
    companyRegistrationNo = mapped_column(String(255))
    vatNo = mapped_column(String(255))
    taxNo = mapped_column(String(255))
    taxOffice = mapped_column(String(255))
    country_id = mapped_column(BigInteger)
    createdAt = mapped_column(DateTime(True))
    createdBy = mapped_column(Uuid)
    updatedAt = mapped_column(DateTime(True))
    updatedBy = mapped_column(Uuid)
    deletedAt = mapped_column(DateTime(True))
    deletedBy = mapped_column(Uuid)
    company_id = mapped_column(String(100))

    country: Mapped[Optional['GeneralCountries']] = relationship('GeneralCountries', back_populates='User_Company_Registration_Tax')
    Users_: Mapped['Users'] = relationship('Users', back_populates='User_Company_Registration_Tax')
    User_Bank_Account_Information: Mapped[List['UserBankAccountInformation']] = relationship('UserBankAccountInformation', uselist=True, back_populates='company')
    User_Personal_Information: Mapped[List['UserPersonalInformation']] = relationship('UserPersonalInformation', uselist=True, back_populates='company')


class UserGoalsTargets(Base):
    __tablename__ = 'User_Goals_Targets'
    __table_args__ = (
        ForeignKeyConstraint(['userId'], ['Users.id'], name='User_Goals_Targets_userId_fkey'),
        PrimaryKeyConstraint('id', name='User_Goals_Targets_pkey')
    )

    id = mapped_column(Uuid, server_default=text('uuid_generate_v4()'))
    userId = mapped_column(Uuid, nullable=False)
    goalName = mapped_column(String(255))
    targetValue = mapped_column(Numeric(18, 2))
    achievedValue = mapped_column(Numeric(18, 2))
    status = mapped_column(Integer, server_default=text('1'))
    createdAt = mapped_column(DateTime(True))
    createdBy = mapped_column(Uuid)
    updatedAt = mapped_column(DateTime(True))
    updatedBy = mapped_column(Uuid)
    deletedAt = mapped_column(DateTime(True))
    deletedBy = mapped_column(Uuid)

    Users_: Mapped['Users'] = relationship('Users', back_populates='User_Goals_Targets')


class UserHistory(Base):
    __tablename__ = 'User_History'
    __table_args__ = (
        ForeignKeyConstraint(['createdBy'], ['Users.id'], name='fk_user_history_createdby'),
        ForeignKeyConstraint(['deletedBy'], ['Users.id'], name='fk_user_history_deletedby'),
        ForeignKeyConstraint(['updatedBy'], ['Users.id'], name='fk_user_history_updatedby'),
        PrimaryKeyConstraint('id', name='User_History_pkey')
    )

    id = mapped_column(Uuid, server_default=text('uuid_generate_v4()'))
    Type = mapped_column(String(50))
    statusName = mapped_column(String(50))
    status = mapped_column(Integer, server_default=text('1'))
    remarks = mapped_column(String(500))
    createdAt = mapped_column(DateTime(True))
    createdBy = mapped_column(Uuid)
    updatedAt = mapped_column(DateTime(True))
    updatedBy = mapped_column(Uuid)
    deletedAt = mapped_column(DateTime(True))
    deletedBy = mapped_column(Uuid)

    Users_: Mapped[Optional['Users']] = relationship('Users', foreign_keys=[createdBy], back_populates='User_History')
    Users1: Mapped[Optional['Users']] = relationship('Users', foreign_keys=[deletedBy], back_populates='User_History_')
    Users2: Mapped[Optional['Users']] = relationship('Users', foreign_keys=[updatedBy], back_populates='User_History1')


t_User_Info = Table(
    'User_Info', metadata,
    Column('userId', Uuid, nullable=False),
    Column('settingId', Uuid, nullable=False),
    ForeignKeyConstraint(['settingId'], ['User_Settings.id'], name='User_Info_settingId_fkey'),
    ForeignKeyConstraint(['userId'], ['Users.id'], name='User_Info_userId_fkey'),
    PrimaryKeyConstraint('userId', 'settingId', name='User_Info_pkey')
)


class UserPackageSubscription(Base):
    __tablename__ = 'User_Package_Subscription'
    __table_args__ = (
        ForeignKeyConstraint(['userId'], ['Users.id'], name='User_Package_Subscription_userId_fkey'),
        PrimaryKeyConstraint('id', name='User_Package_Subscription_pkey')
    )

    id = mapped_column(Uuid, server_default=text('uuid_generate_v4()'))
    userId = mapped_column(Uuid, nullable=False)
    packageName = mapped_column(String(255))
    subscriptionDate = mapped_column(DateTime(True))
    expiryDate = mapped_column(DateTime(True))
    status = mapped_column(Integer, server_default=text('1'))
    createdAt = mapped_column(DateTime(True))
    createdBy = mapped_column(Uuid)
    updatedAt = mapped_column(DateTime(True))
    updatedBy = mapped_column(Uuid)
    deletedAt = mapped_column(DateTime(True))
    deletedBy = mapped_column(Uuid)

    Users_: Mapped['Users'] = relationship('Users', back_populates='User_Package_Subscription')


class UserPersonalFiles(Base):
    __tablename__ = 'User_Personal_Files'
    __table_args__ = (
        ForeignKeyConstraint(['user_id'], ['Users.id'], name='user_id_fk'),
        PrimaryKeyConstraint('id', name='User_Personal_Files_pkey')
    )

    id = mapped_column(Integer)
    file_name = mapped_column(String(255), nullable=False)
    file_path = mapped_column(String(255), nullable=False)
    user_id = mapped_column(Uuid)
    screen_name = mapped_column(String)
    screen_uuid = mapped_column(Uuid)

    user: Mapped[Optional['Users']] = relationship('Users', back_populates='User_Personal_Files')


class UserSettingsAssignment(Base):
    __tablename__ = 'User_Settings_Assignment'
    __table_args__ = (
        ForeignKeyConstraint(['setting_id'], ['User_Settings.id'], ondelete='CASCADE', name='fk_user_settings_assignment_setting'),
        ForeignKeyConstraint(['user_id'], ['Users.id'], ondelete='CASCADE', name='fk_user_settings_assignment_user'),
        PrimaryKeyConstraint('id', name='User_Settings_Assignment_pkey'),
        UniqueConstraint('user_id', 'setting_id', name='unique_user_setting_assignment')
    )

    id = mapped_column(Uuid, server_default=text('uuid_generate_v4()'))
    user_id = mapped_column(Uuid, nullable=False)
    setting_id = mapped_column(Uuid, nullable=False)
    createdAt = mapped_column(DateTime(True), server_default=text('CURRENT_TIMESTAMP'))
    createdBy = mapped_column(Uuid)
    updatedAt = mapped_column(DateTime(True), server_default=text('CURRENT_TIMESTAMP'))
    updatedBy = mapped_column(Uuid)
    deletedAt = mapped_column(DateTime(True))
    deletedBy = mapped_column(Uuid)

    setting: Mapped['UserSettings'] = relationship('UserSettings', back_populates='User_Settings_Assignment')
    user: Mapped['Users'] = relationship('Users', back_populates='User_Settings_Assignment')


class Userfiles(Base):
    __tablename__ = 'userfiles'
    __table_args__ = (
        ForeignKeyConstraint(['user_id'], ['Users.id'], name='files_userid_fkey'),
        PrimaryKeyConstraint('id', name='userfiles_pkey')
    )

    id = mapped_column(Integer)
    file_name = mapped_column(String(255), nullable=False)
    file_path = mapped_column(String(255), nullable=False)
    user_id = mapped_column(Uuid)

    user: Mapped[Optional['Users']] = relationship('Users', back_populates='userfiles')


class UserBankAccountInformation(Base):
    __tablename__ = 'User_Bank_Account_Information'
    __table_args__ = (
        ForeignKeyConstraint(['city_id'], ['General_Cities.id'], name='User_Bank_Account_Information_cityId_fkey'),
        ForeignKeyConstraint(['company_id'], ['User_Company_Registration_Tax.id'], name='User_Bank_Account_Information_companyid_fkey'),
        ForeignKeyConstraint(['country_id'], ['General_Countries.id'], name='User_Bank_Account_Information_country_id_fkey'),
        ForeignKeyConstraint(['userId'], ['Users.id'], name='User_Bank_Account_Information_userId_fkey'),
        PrimaryKeyConstraint('id', name='User_Bank_Account_Information_pkey')
    )

    id = mapped_column(Uuid, server_default=text('uuid_generate_v4()'))
    userId = mapped_column(Uuid, nullable=False)
    bankName = mapped_column(String(255))
    bankBranch = mapped_column(String(255))
    accountName = mapped_column(String(255))
    accountNumber = mapped_column(String(255))
    swiftCode = mapped_column(String(255))
    iban = mapped_column(String(255))
    currency = mapped_column(String(50))
    country_id = mapped_column(BigInteger)
    createdAt = mapped_column(DateTime(True))
    createdBy = mapped_column(Uuid)
    updatedAt = mapped_column(DateTime(True))
    updatedBy = mapped_column(Uuid)
    deletedAt = mapped_column(DateTime(True))
    deletedBy = mapped_column(Uuid)
    city_id = mapped_column(BigInteger)
    company_id = mapped_column(Uuid)

    city: Mapped[Optional['GeneralCities']] = relationship('GeneralCities', back_populates='User_Bank_Account_Information')
    company: Mapped[Optional['UserCompanyRegistrationTax']] = relationship('UserCompanyRegistrationTax', back_populates='User_Bank_Account_Information')
    country: Mapped[Optional['GeneralCountries']] = relationship('GeneralCountries', back_populates='User_Bank_Account_Information')
    Users_: Mapped['Users'] = relationship('Users', back_populates='User_Bank_Account_Information')


class UserPersonalInformation(Base):
    __tablename__ = 'User_Personal_Information'
    __table_args__ = (
        ForeignKeyConstraint(['city_id'], ['General_Cities.id'], name='User_Personal_Information_city_id_fkey'),
        ForeignKeyConstraint(['company_id'], ['User_Company_Registration_Tax.id'], name='fk_user_company_id'),
        ForeignKeyConstraint(['country_id'], ['General_Countries.id'], name='User_Personal_Information_country_id_fkey'),
        ForeignKeyConstraint(['state_id'], ['General_States.id'], name='User_Personal_Information_state_id_fkey'),
        ForeignKeyConstraint(['userId'], ['Users.id'], name='User_Personal_Information_userId_fkey'),
        PrimaryKeyConstraint('id', name='User_Personal_Information_pkey')
    )

    id = mapped_column(Uuid, server_default=text('uuid_generate_v4()'))
    userId = mapped_column(Uuid, nullable=False)
    firstName = mapped_column(String(100))
    lastName = mapped_column(String(100))
    middleName = mapped_column(String(100))
    dateOfBirth = mapped_column(DateTime(True))
    contactNumber = mapped_column(String(50))
    email = mapped_column(String(255))
    gender = mapped_column(String(50))
    maritalStatus = mapped_column(String(50))
    residentialAddressLine1 = mapped_column(String(255))
    residentialAddressLine2 = mapped_column(String(255))
    country_id = mapped_column(BigInteger)
    postalCode = mapped_column(String(50))
    state_id = mapped_column(BigInteger)
    city_id = mapped_column(BigInteger)
    createdAt = mapped_column(DateTime(True))
    createdBy = mapped_column(Uuid)
    updatedAt = mapped_column(DateTime(True))
    updatedBy = mapped_column(Uuid)
    deletedAt = mapped_column(DateTime(True))
    deletedBy = mapped_column(Uuid)
    salutation = mapped_column(String(20))
    job_title = mapped_column(String(100))
    company_id = mapped_column(Uuid)

    city: Mapped[Optional['GeneralCities']] = relationship('GeneralCities', back_populates='User_Personal_Information')
    company: Mapped[Optional['UserCompanyRegistrationTax']] = relationship('UserCompanyRegistrationTax', back_populates='User_Personal_Information')
    country: Mapped[Optional['GeneralCountries']] = relationship('GeneralCountries', back_populates='User_Personal_Information')
    state: Mapped[Optional['GeneralStates']] = relationship('GeneralStates', back_populates='User_Personal_Information')
    Users_: Mapped['Users'] = relationship('Users', back_populates='User_Personal_Information')
