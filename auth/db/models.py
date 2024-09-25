
from datetime import datetime,timezone
from sqlalchemy import (
    JSON, VARCHAR, Column, DateTime, PrimaryKeyConstraint, String, Integer, BigInteger, Boolean, TIMESTAMP, ForeignKey, Numeric, Text, SmallInteger, UniqueConstraint, text
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, DeclarativeBase, mapped_column, Mapped
import uuid
from sqlalchemy import Column, BigInteger, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
# from .database import Base # type: ignore
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from auth.dependencies import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, JSON, TIMESTAMP, func
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class IndustrySector(Base):
    __tablename__ = 'industry_sector'

    id = Column(Integer, primary_key=True, server_default=text("nextval('\"IndustrySector_id_seq\"'::regclass)"))
    name = Column(String(255), nullable=False)
    financed_entities: Mapped[list["CatalogsFinancedEntities"]] = relationship(
        "CatalogsFinancedEntities", foreign_keys="[CatalogsFinancedEntities.industry_sector_id]", back_populates="industrysector"
    )

class FactorUnit(Base):
    __tablename__ = 'factor_unit'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.utcnow)
    created_by: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('users.id'))
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP)
    updated_by: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('users.id'))
    deleted_at: Mapped[datetime] = mapped_column(TIMESTAMP)
    deleted_by: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('users.id'))


    createdby: Mapped["Users"] = relationship(
        "Users", foreign_keys=[created_by], back_populates="factor_units_created"
    )
    
    updatedby: Mapped["Users"] = relationship(
        "Users", foreign_keys=[updated_by], back_populates="factor_units_updated"
    )
    
    deletedby: Mapped["Users"] = relationship(
        "Users", foreign_keys=[deleted_by], back_populates="factor_units_deleted"
    )



class Industry(Base):
    __tablename__ = 'industry'

    id = Column(Integer, primary_key=True, server_default=text("nextval('\"Industry_id_seq\"'::regclass)"))
    name = Column(String(255), nullable=False)
    sector_id = Column(ForeignKey('industry_sector.id'), nullable=False)

    sector = relationship('IndustrySector')
    financed_entities: Mapped[list["CatalogsFinancedEntities"]] = relationship(
        "CatalogsFinancedEntities", foreign_keys="[CatalogsFinancedEntities.industry_id]", back_populates="industry"
    )

class SubIndustry(Base):
    __tablename__ = 'sub_industry'

    id = Column(Integer, primary_key=True, server_default=text("nextval('\"Industry_id_seq\"'::regclass)"))
    name = Column(String(255), nullable=False)
    industry_id = Column(ForeignKey('industry.id'), nullable=False)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.utcnow)
    created_by: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('users.id'))
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP)
    updated_by: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('users.id'))
    deleted_at: Mapped[datetime] = mapped_column(TIMESTAMP)
    deleted_by: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('users.id'))

    sector = relationship('Industry')
    financed_entities: Mapped[list["CatalogsFinancedEntities"]] = relationship(
        "CatalogsFinancedEntities", foreign_keys="[CatalogsFinancedEntities.sub_industry_id]", back_populates="subindustry")
    

class SystemSessions(Base):
    __tablename__ = "system_sessions"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    userId = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    token = Column(String(255), nullable=False)
    createdAt = Column(TIMESTAMP)
    expiresAt = Column(TIMESTAMP)

class Users(Base):
    __tablename__ = "users"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    sso_id :  Mapped[str] = mapped_column(String(50))
    firstName: Mapped[str] = mapped_column(String(50))
    lastName: Mapped[str] = mapped_column(String(50))
    companyName: Mapped[str] = mapped_column(String(50))
    companyEmail: Mapped[str] = mapped_column(String(50))
    country_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('general_countries.id'))
    state_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('general_states.id'))
    city_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('general_cities.id'))
    password: Mapped[str] = mapped_column(String(50), nullable=True)
    userTypeId: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('user_role.id'), nullable=False)
    isReset: Mapped[bool] = mapped_column(Boolean, default=False)
    ipAddress: Mapped[str] = mapped_column(String(50))
    thirdPartySubscriptionId: Mapped[str] = mapped_column(String(50))
    status: Mapped[int] = mapped_column(Integer, default=4) # 1 = Active, 2 = Inactive, 3 = Deleted, 4 = Pending signup, 5 = Signup Reject, 6 = Pending Profile setup, 7 = pending profile approval, 8 = Rejected Profile
    createdAt: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.utcnow)
    createdBy: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('users.id'))
    updatedAt: Mapped[datetime] = mapped_column(TIMESTAMP, onupdate=datetime.utcnow)
    updatedBy: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('users.id'))
    deletedAt: Mapped[datetime] = mapped_column(TIMESTAMP)
    deletedBy: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('users.id'))
    signupverifiedby: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True))
    profileverifiedby: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True))
    remarks: Mapped[str] = mapped_column(String(500))
    image: Mapped[str] = mapped_column(String(250))
    reset_token: Mapped[str] = mapped_column(String, index=True)
    reset_token_expiration: Mapped[datetime] = mapped_column(DateTime)
    
    
    locations_created: Mapped[list["CatalogsLocation"]] = relationship(
        "CatalogsLocation", foreign_keys="[CatalogsLocation.created_by]", back_populates="createdby"
    )
    
    locations_updated: Mapped[list["CatalogsLocation"]] = relationship(
        "CatalogsLocation", foreign_keys="[CatalogsLocation.updated_by]", back_populates="updatedby"
    )
    
    locations_deleted: Mapped[list["CatalogsLocation"]] = relationship(
        "CatalogsLocation", foreign_keys="[CatalogsLocation.deleted_by]", back_populates="deletedby"
    )
    user_settings_assignments: Mapped[list["UserSettingsAssignment"]] = relationship("UserSettingsAssignment", back_populates="user", foreign_keys="[UserSettingsAssignment.user_id]")
    categories_created: Mapped[list["Category"]] = relationship(
        "Category", foreign_keys="[Category.created_by]", back_populates="createdby"
    )
    
    categories_updated: Mapped[list["Category"]] = relationship(
        "Category", foreign_keys="[Category.updated_by]", back_populates="updatedby"
    )
    
    categories_deleted: Mapped[list["Category"]] = relationship(
        "Category", foreign_keys="[Category.deleted_by]", back_populates="deletedby"
    )
    sub_categories_created: Mapped[list["SubCategory"]] = relationship(
        "SubCategory", foreign_keys="[SubCategory.created_by]", back_populates="createdby"
    )
    
    sub_categories_updated: Mapped[list["SubCategory"]] = relationship(
        "SubCategory", foreign_keys="[SubCategory.updated_by]", back_populates="updatedby"
    )
    
    sub_categories_deleted: Mapped[list["SubCategory"]] = relationship(
        "SubCategory", foreign_keys="[SubCategory.deleted_by]", back_populates="deletedby"
    )
    gross_area_created: Mapped[list["GrossArea"]] = relationship(
        "GrossArea", foreign_keys="[GrossArea.created_by]", back_populates="createdby"
    )
    
    gross_area_updated: Mapped[list["GrossArea"]] = relationship(
        "GrossArea", foreign_keys="[GrossArea.updated_by]", back_populates="updatedby"
    )
    
    gross_area_deleted: Mapped[list["GrossArea"]] = relationship(
        "GrossArea", foreign_keys="[GrossArea.deleted_by]", back_populates="deletedby"
    )
    gross_area_units_created: Mapped[list["GrossAreaUnit"]] = relationship(
        "GrossAreaUnit", foreign_keys="[GrossAreaUnit.created_by]", back_populates="createdby"
    )
    
    gross_area_units_updated: Mapped[list["GrossAreaUnit"]] = relationship(
        "GrossAreaUnit", foreign_keys="[GrossAreaUnit.updated_by]", back_populates="updatedby"
    )
    
    gross_area_units_deleted: Mapped[list["GrossAreaUnit"]] = relationship(
        "GrossAreaUnit", foreign_keys="[GrossAreaUnit.deleted_by]", back_populates="deletedby"
    )
    facilities_created: Mapped[list["CatalogsFacilities"]] = relationship(
        "CatalogsFacilities", foreign_keys="[CatalogsFacilities.created_by]", back_populates="createdby"
    )
    
    facilities_updated: Mapped[list["CatalogsFacilities"]] = relationship(
        "CatalogsFacilities", foreign_keys="[CatalogsFacilities.updated_by]", back_populates="updatedby"
    )
    
    facilities_deleted: Mapped[list["CatalogsFacilities"]] = relationship(
        "CatalogsFacilities", foreign_keys="[CatalogsFacilities.deleted_by]", back_populates="deletedby"
    )
    financed_entities_created: Mapped[list["CatalogsFinancedEntities"]] = relationship(
        "CatalogsFinancedEntities", foreign_keys="[CatalogsFinancedEntities.created_by]", back_populates="createdby"
    )
    financed_entities_updated: Mapped[list["CatalogsFinancedEntities"]] = relationship(
        "CatalogsFinancedEntities", foreign_keys="[CatalogsFinancedEntities.updated_by]", back_populates="updatedby"
    )

    financed_entities_deleted: Mapped[list["CatalogsFinancedEntities"]] = relationship(
        "CatalogsFinancedEntities", foreign_keys="[CatalogsFinancedEntities.deleted_by]", back_populates="deletedby"
    )
    equipment_types_created: Mapped[list["CatalogsEquipmentType"]] = relationship(
        "CatalogsEquipmentType", foreign_keys="[CatalogsEquipmentType.created_by]", back_populates="createdby"
    )
    equipment_types_updated: Mapped[list["CatalogsEquipmentType"]] = relationship(
        "CatalogsEquipmentType", foreign_keys="[CatalogsEquipmentType.updated_by]", back_populates="updatedby"
    )

    equipment_types_deleted: Mapped[list["CatalogsEquipmentType"]] = relationship(
        "CatalogsEquipmentType", foreign_keys="[CatalogsEquipmentType.deleted_by]", back_populates="deletedby"
    )

    factor_units_created: Mapped[list["FactorUnit"]] = relationship(
        "FactorUnit", foreign_keys="[FactorUnit.created_by]", back_populates="createdby"
    )
    factor_units_updated: Mapped[list["FactorUnit"]] = relationship(
        "FactorUnit", foreign_keys="[FactorUnit.updated_by]", back_populates="updatedby"
    )

    factor_units_deleted: Mapped[list["FactorUnit"]] = relationship(
        "FactorUnit", foreign_keys="[FactorUnit.deleted_by]", back_populates="deletedby"
    )
    
class UserHistory(Base):
    __tablename__ = "user_history"
    
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    Type: Mapped[str] = mapped_column(String(50))
    statusName: Mapped[str] = mapped_column(String(50))
    status: Mapped[int] = mapped_column(Integer, default=1)
    remarks: Mapped[str] = mapped_column(String(500))
    createdAt: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.utcnow)
    createdBy: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('users.id'))
    updatedAt: Mapped[datetime] = mapped_column(TIMESTAMP, onupdate=datetime.utcnow)
    updatedBy: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('users.id'))
    deletedAt: Mapped[datetime] = mapped_column(TIMESTAMP)
    deletedBy: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('users.id'))

class UserRole(Base):
    __tablename__ = "user_role"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    typeName = Column(String(50))
    description = Column(String(255))

class UserInfo(Base):
    __tablename__ = "user_info"
    userId = Column(UUID(as_uuid=True), ForeignKey('users.id'), primary_key=True)
    settingId = Column(UUID(as_uuid=True), ForeignKey('user_settings.id'), primary_key=True)

class UserCodes(Base):
    __tablename__ = "user_codes"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    userId = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    code = Column(String(50))
    identityName = Column(String(50))
    type = Column(String(50))
    status = Column(Integer, default=1)
    createdAt = Column(TIMESTAMP)
    createdBy = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    updatedAt = Column(TIMESTAMP)
    updatedBy = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    deletedAt = Column(TIMESTAMP)
    deletedBy = Column(UUID(as_uuid=True), ForeignKey('users.id'))

class UserSettings(Base):
    __tablename__ = "user_settings"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    headerName = Column(String(500))
    sectionName = Column(String(500))
    value = Column(String)
    subValue = Column(String)
    description = Column(String)
    isOtherFields = Column(Boolean)
    sortOrder = Column(Integer)
    status = Column(Integer, default=1)
    createdAt = Column(TIMESTAMP)
    createdBy = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    updatedAt = Column(TIMESTAMP)
    updatedBy = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    deletedAt = Column(TIMESTAMP)
    deletedBy = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    user_settings_assignments = relationship("UserSettingsAssignment", back_populates="setting")

class UserRolePermissions(Base):
    __tablename__ = "user_role_permissions"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    permissionName = Column(String(50), nullable=False)
    description = Column(String(255))
    createdAt = Column(TIMESTAMP)
    createdBy = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    updatedAt = Column(TIMESTAMP)
    updatedBy = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    deletedAt = Column(TIMESTAMP)
    deletedBy = Column(UUID(as_uuid=True), ForeignKey('users.id'))

class UserRolePermissionsMapping(Base):
    __tablename__ = "user_role_permissions_mapping"
    userTypeId = Column(UUID(as_uuid=True), ForeignKey('user_role.id'), primary_key=True)
    permissionId = Column(UUID(as_uuid=True), ForeignKey('user_role_permissions.id'), primary_key=True)

# class UserBusinessDetails(Base):
#     __tablename__ = "User_Business_Details"
#     id = Column(String, primary_key=True, default=str(uuid.uuid4))
#     userId = Column(UUID(as_uuid=True), ForeignKey('Users.id'), nullable=False)
#     companyLegalName = Column(String(100))
#     industry = Column(String(100))
#     corporateWebsite = Column(String(255))
#     contactNumber = Column(String(50))
#     businessAddressLine1 = Column(String(255))
#     businessAddressLine2 = Column(String(255))
#     country_id = Column(BigInteger, ForeignKey('General_Countries.id'))
#     postalCode = Column(String(50))
#     state_id = Column(BigInteger, ForeignKey('General_States.id'))
#     city_id = Column(BigInteger, ForeignKey('General_Cities.id'))
#     createdAt = Column(TIMESTAMP)
#     createdBy = Column(UUID(as_uuid=True), ForeignKey('Users.id'))
#     updatedAt = Column(TIMESTAMP)
#     updatedBy = Column(UUID(as_uuid=True), ForeignKey('Users.id'))
#     deletedAt = Column(TIMESTAMP)
#     deletedBy = Column(UUID(as_uuid=True), ForeignKey('Users.id'))

# class UserBusinessDetails(Base):
#     __tablename__ = "User_Business_Details"
    
#     id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
#     userId = Column(UUID(as_uuid=True), ForeignKey('Users.id'), nullable=False)
#     companyLegalName = Column(String(100))
#     industry = Column(String(100))
#     corporateWebsite = Column(String(255))
#     contactNumber = Column(String(50))
#     businessAddressLine1 = Column(String(255))
#     businessAddressLine2 = Column(String(255))
#     country_id = Column(BigInteger, ForeignKey('General_Countries.id'))
#     postalCode = Column(String(50))
#     state_id = Column(BigInteger, ForeignKey('General_States.id'))
#     city_id = Column(BigInteger, ForeignKey('General_Cities.id'))
#     createdAt = Column(TIMESTAMP)
#     createdBy = Column(UUID(as_uuid=True), ForeignKey('Users.id'))
#     updatedAt = Column(TIMESTAMP)
#     updatedBy = Column(UUID(as_uuid=True), ForeignKey('Users.id'))
#     deletedAt = Column(TIMESTAMP)
#     deletedBy = Column(UUID(as_uuid=True), ForeignKey('Users.id'))

class UserBusinessDetails(Base):
    __tablename__ = 'user_business_details'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    userId = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    companyLegalName = Column(String(100), nullable=False)
    industry_id: Mapped[int] = mapped_column(Integer, ForeignKey('industry.id'))
    corporateWebsite = Column(String(255))
    contactNumber = Column(String(50))
    businessAddressLine1 = Column(String(255), nullable=False)
    businessAddressLine2 = Column(String(255))
    country_id = Column(Integer, ForeignKey('general_countries.id', ondelete='CASCADE'))
    postalCode = Column(String(50), nullable=False)
    state_id = Column(Integer, ForeignKey('general_states.id', ondelete='CASCADE'))
    city_id = Column(Integer, ForeignKey('general_cities.id', ondelete='CASCADE'))
    createdAt = Column(DateTime, default=datetime.utcnow, nullable=False)
    createdBy = Column(UUID(as_uuid=True))
    updatedAt = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    updatedBy = Column(UUID(as_uuid=True))
    deletedAt = Column(DateTime)
    deletedBy = Column(UUID(as_uuid=True))


class UserPersonalInformation(Base):
    __tablename__ = "user_personal_information"
    
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    userId: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    company_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('user_company_registration_tax.id'), nullable=False)
    country_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('general_countries.id'))
    state_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('general_states.id'))
    city_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('general_cities.id'))
    # salutation: Mapped[str] = mapped_column(String(20))
    firstName: Mapped[str] = mapped_column(String(100))
    lastName: Mapped[str] = mapped_column(String(100))
    middleName: Mapped[str] = mapped_column(String(100))
    dateOfBirth: Mapped[datetime] = mapped_column(TIMESTAMP)
    contactNumber: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(255))
    job_title: Mapped[str] = mapped_column(String(100))
    gender: Mapped[str] = mapped_column(String(50))
    maritalStatus: Mapped[str] = mapped_column(String(50))
    residentialAddressLine1: Mapped[str] = mapped_column(String(255))
    residentialAddressLine2: Mapped[str] = mapped_column(String(255))
    postalCode: Mapped[str] = mapped_column(String(50))
    createdAt: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.utcnow)
    createdBy: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('users.id'))
    updatedAt: Mapped[datetime] = mapped_column(TIMESTAMP, onupdate=datetime.utcnow)
    updatedBy: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('users.id'))
    deletedAt: Mapped[datetime] = mapped_column(TIMESTAMP)
    deletedBy: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('users.id'))
    salutation_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('user_salutation.id'))



class UserPersonalFiles(Base):
    __tablename__ = 'user_personal_files'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    screen_name: Mapped[str] = mapped_column(String(50))
    screen_uuid : Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True))
    user_id : Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('users.id'))
    file_name: Mapped[str] = mapped_column(String, nullable=False)
    file_path: Mapped[str] = mapped_column(String, nullable=False)

class UserCompanyRegistrationTax(Base):
    __tablename__ = "user_company_registration_tax"
    
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    userId: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    companyName: Mapped[str] = mapped_column(String(255))
    companyRegistrationNo: Mapped[str] = mapped_column(String(255))
    vatNo: Mapped[str] = mapped_column(String(255))
    taxNo: Mapped[str] = mapped_column(String(255))
    taxOffice: Mapped[str] = mapped_column(String(255))
    company_id: Mapped[str] = mapped_column(String(100))
    country_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('general_countries.id'))
    createdAt: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.utcnow)
    createdBy: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('users.id'))
    updatedAt: Mapped[datetime] = mapped_column(TIMESTAMP, onupdate=datetime.utcnow)
    updatedBy: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('users.id'))
    deletedAt: Mapped[datetime] = mapped_column(TIMESTAMP)
    deletedBy: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('users.id'))

class UserBankAccountInformation(Base):
    __tablename__ = "user_bank_account_information"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    userId = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    bankName = Column(String(255))
    # bankCode = Column(String(50))
    bankBranch = Column(String(255))
    accountName = Column(String(255))
    accountNumber = Column(String(255))
    iban = Column(String(255))
    swiftCode = Column(String(255))
    country_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('general_countries.id'))
    city_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('general_cities.id'))
    company_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('user_company_registration_tax.id'))
    createdAt = Column(TIMESTAMP)
    createdBy = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    updatedAt = Column(TIMESTAMP)
    updatedBy = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    deletedAt = Column(TIMESTAMP)
    deletedBy = Column(UUID(as_uuid=True), ForeignKey('users.id'))

class UserGoalsTargets(Base):
    __tablename__ = "user_goals_targets"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    userId = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    goal = Column(String(255))
    target = Column(String(255))
    description = Column(Text)
    startDate = Column(TIMESTAMP)
    endDate = Column(TIMESTAMP)
    createdAt = Column(TIMESTAMP)
    createdBy = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    updatedAt = Column(TIMESTAMP)
    updatedBy = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    deletedAt = Column(TIMESTAMP)
    deletedBy = Column(UUID(as_uuid=True), ForeignKey('users.id'))

class UserPackageSubscription(Base):
    __tablename__ = "user_package_subscription"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    userId = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    packageType = Column(String(50))
    packageName = Column(String(50))
    description = Column(Text)
    cost = Column(Numeric)
    duration = Column(Integer)
    unit = Column(String(50))
    subscriptionStartDate = Column(TIMESTAMP)
    subscriptionEndDate = Column(TIMESTAMP)
    status = Column(Integer, default=1)
    createdAt = Column(TIMESTAMP)
    createdBy = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    updatedAt = Column(TIMESTAMP)
    updatedBy = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    deletedAt = Column(TIMESTAMP)
    deletedBy = Column(UUID(as_uuid=True), ForeignKey('users.id'))
class GeneralCountries(Base):
    __tablename__ = "general_countries"
    
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    iso3: Mapped[str] = mapped_column(String(3))
    numeric_code: Mapped[str] = mapped_column(String(3))
    iso2: Mapped[str] = mapped_column(String(2))
    phonecode: Mapped[str] = mapped_column(String(255))
    capital: Mapped[str] = mapped_column(String(255))
    currency: Mapped[str] = mapped_column(String(255))
    currency_name: Mapped[str] = mapped_column(String(255))
    currency_symbol: Mapped[str] = mapped_column(String(255))
    tld: Mapped[str] = mapped_column(String(255))
    native: Mapped[str] = mapped_column(String(255))
    region: Mapped[str] = mapped_column(String(255))
    subregion: Mapped[str] = mapped_column(String(255))
    timezones: Mapped[str] = mapped_column(Text)
    translations: Mapped[str] = mapped_column(Text)
    latitude: Mapped[float] = mapped_column(Numeric)
    longitude: Mapped[float] = mapped_column(Numeric)
    flag:  Mapped[int] = mapped_column(SmallInteger, nullable=False, server_default='1')
    wikiDataId: Mapped[str] = mapped_column((String(255)))
    nationality: Mapped[str] = mapped_column(String(255))
    emoji: Mapped[str] = mapped_column(String(191))
    emojiU: Mapped[str] = mapped_column(String(191))
    createdAt: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.utcnow)
    createdBy: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('users.id'))
    updatedAt: Mapped[datetime] = mapped_column(TIMESTAMP, onupdate=datetime.utcnow)
    updatedBy: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('users.id'))
    deletedAt: Mapped[datetime] = mapped_column(TIMESTAMP)
    deletedBy: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('users.id'))
    
    states: Mapped[list["GeneralStates"]] = relationship("GeneralStates", back_populates="country", lazy="selectin")
    cities: Mapped[list["GeneralCities"]] = relationship("GeneralCities", back_populates="country", lazy="selectin")
    locations: Mapped[list["CatalogsLocation"]] = relationship("CatalogsLocation", back_populates="country")
    financed_entities: Mapped[list["CatalogsFinancedEntities"]] = relationship("CatalogsFinancedEntities", back_populates="country")



class GeneralStates(Base):
    __tablename__ = "general_states"
    
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    country_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('general_countries.id'), nullable=False)
    country_code: Mapped[str] = mapped_column(String(2))
    fips_code: Mapped[str] = mapped_column(String(255))
    iso2: Mapped[str] = mapped_column(String(255))
    type: Mapped[str] = mapped_column(String(191))
    latitude: Mapped[float] = mapped_column(Numeric)
    longitude: Mapped[float] = mapped_column(Numeric)
    flag:  Mapped[int] = mapped_column(SmallInteger, nullable=False, server_default='1')
    wikiDataId: Mapped[str] = mapped_column(String(255),nullable=False)
    createdAt: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.utcnow)
    createdBy: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('users.id'))
    updatedAt: Mapped[datetime] = mapped_column(TIMESTAMP, onupdate=datetime.utcnow)
    updatedBy: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('users.id'))
    deletedAt: Mapped[datetime] = mapped_column(TIMESTAMP)
    deletedBy: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('users.id'))
    
    country: Mapped["GeneralCountries"] = relationship("GeneralCountries", back_populates="states", lazy="selectin")
    cities: Mapped[list["GeneralCities"]] = relationship("GeneralCities", back_populates="state", lazy="selectin")
    locations: Mapped[list["CatalogsLocation"]] = relationship("CatalogsLocation", back_populates="state")
    financed_entities: Mapped[list["CatalogsFinancedEntities"]] = relationship("CatalogsFinancedEntities", back_populates="state")



class GeneralCities(Base):
    __tablename__ = "general_cities"
    
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    state_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('general_states.id'), nullable=False)
    state_code: Mapped[str] = mapped_column(String(255))
    country_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('general_countries.id'), nullable=False)
    country_code: Mapped[str] = mapped_column(String(255))
    latitude: Mapped[float] = mapped_column(Numeric)
    longitude: Mapped[float] = mapped_column(Numeric)
    wikiDataId: Mapped[str] = mapped_column(String(255),nullable=False)
    flag:  Mapped[int] = mapped_column(SmallInteger, nullable=False, server_default='1')
    createdAt: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.utcnow)
    createdBy: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('users.id'))
    updatedAt: Mapped[datetime] = mapped_column(TIMESTAMP, onupdate=datetime.utcnow)
    updatedBy: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('users.id'))
    deletedAt: Mapped[datetime] = mapped_column(TIMESTAMP)
    deletedBy: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('users.id'))
    
    country: Mapped["GeneralCountries"] = relationship("GeneralCountries", back_populates="cities", lazy="selectin")
    state: Mapped["GeneralStates"] = relationship("GeneralStates", back_populates="cities", lazy="selectin")
    locations: Mapped[list["CatalogsLocation"]] = relationship("CatalogsLocation", back_populates="city")
    financed_entities: Mapped[list["CatalogsFinancedEntities"]] = relationship("CatalogsFinancedEntities", back_populates="city")


class UserSettingsAssignment(Base):
    __tablename__ = "user_settings_assignment"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    # setting_id = Column(BigInteger, ForeignKey('User_Settings.id'), nullable=False)
    setting_id = Column(UUID(as_uuid=True), ForeignKey('user_settings.id'))
    createdAt = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
    createdBy = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    updatedAt = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    updatedBy = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    deletedAt = Column(TIMESTAMP(timezone=True))
    deletedBy = Column(UUID(as_uuid=True), ForeignKey('users.id'))

    user = relationship("Users", back_populates="user_settings_assignments", foreign_keys=[user_id])
    setting = relationship("UserSettings", back_populates="user_settings_assignments",foreign_keys=[setting_id])

class Userfile(Base):
    __tablename__ = 'userfiles'

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=func.uuid_generate_v4(), unique=True)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('users.id'))
    file_name = Column(String(255), nullable=False)
    file_path = Column(String(255), nullable=False)


class CatalogsLocation(Base):
    __tablename__ = "catalogs_locations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(255),nullable=False)
    address: Mapped[str] = mapped_column(String(255),nullable=False)
    aptsuite: Mapped[str] = mapped_column(String(255),nullable=False)
    country_id: Mapped[int] = mapped_column(BigInteger,ForeignKey('general_countries.id'),nullable=False)
    state_id: Mapped[int] = mapped_column(BigInteger,ForeignKey('general_states.id'),nullable=False)
    city_id: Mapped[int] = mapped_column(BigInteger,ForeignKey('general_cities.id'),nullable=False)
    zip_code: Mapped[str] = mapped_column(String(50),nullable=False)
    description: Mapped[str] = mapped_column(String(255),nullable=False)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.utcnow)
    created_by: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('users.id'))
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP)
    updated_by: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('users.id'))
    deleted_at: Mapped[datetime] = mapped_column(TIMESTAMP)
    deleted_by: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('users.id'))

    
    country:Mapped["GeneralCountries"] = relationship("GeneralCountries",back_populates="locations")
    state:Mapped["GeneralStates"] = relationship("GeneralStates",back_populates="locations")
    city:Mapped["GeneralCities"] = relationship("GeneralCities",back_populates="locations")
    createdby: Mapped["Users"] = relationship(
        "Users", foreign_keys=[created_by], back_populates="locations_created"
    )
    
    updatedby: Mapped["Users"] = relationship(
        "Users", foreign_keys=[updated_by], back_populates="locations_updated"
    )
    
    deletedby: Mapped["Users"] = relationship(
        "Users", foreign_keys=[deleted_by], back_populates="locations_deleted"
    )
    facilities: Mapped[list["CatalogsFacilities"]] = relationship(
        "CatalogsFacilities", foreign_keys="[CatalogsFacilities.location_id]", back_populates="location"
    )

class GrossArea(Base):

    __tablename__ = "gross_area"

    id = Column(Integer, primary_key=True, autoincrement=True)
    area = Column(Integer, nullable=False)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.utcnow)
    created_by: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('users.id'))
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP)
    updated_by: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('users.id'))
    deleted_at: Mapped[datetime] = mapped_column(TIMESTAMP)
    deleted_by: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('users.id'))
    
    createdby: Mapped["Users"] = relationship(
        "Users", foreign_keys=[created_by], back_populates="gross_area_created"
    )
    
    updatedby: Mapped["Users"] = relationship(
        "Users", foreign_keys=[updated_by], back_populates="gross_area_updated"
    )
    
    deletedby: Mapped["Users"] = relationship(
        "Users", foreign_keys=[deleted_by], back_populates="gross_area_deleted")
    facilities: Mapped[list["CatalogsFacilities"]] = relationship(
        "CatalogsFacilities", foreign_keys="[CatalogsFacilities.gross_area_id]", back_populates="gross_area"
    )

class GrossAreaUnit(Base):

    __tablename__ = "gross_area_unit"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.utcnow)
    created_by: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('users.id'))
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP)
    updated_by: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('users.id'))
    deleted_at: Mapped[datetime] = mapped_column(TIMESTAMP)
    deleted_by: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('users.id'))
    
    createdby: Mapped["Users"] = relationship(
        "Users", foreign_keys=[created_by], back_populates="gross_area_units_created"
    )
    
    updatedby: Mapped["Users"] = relationship(
        "Users", foreign_keys=[updated_by], back_populates="gross_area_units_updated"
    )
    
    deletedby: Mapped["Users"] = relationship(
        "Users", foreign_keys=[deleted_by], back_populates="gross_area_units_deleted")
    facilities: Mapped[list["CatalogsFacilities"]] = relationship(
        "CatalogsFacilities", foreign_keys="[CatalogsFacilities.gross_area_unit_id]", back_populates="gross_area_unit"
    )

class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.utcnow)
    created_by: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('users.id'))
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP)
    updated_by: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('users.id'))
    deleted_at: Mapped[datetime] = mapped_column(TIMESTAMP)
    deleted_by: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('users.id'))
    


    subcategories:Mapped[list["SubCategory"]] = relationship("SubCategory",back_populates="category")
    equipment_types:Mapped[list["CatalogsEquipmentType"]] = relationship("CatalogsEquipmentType",back_populates="category")
    createdby: Mapped["Users"] = relationship(
        "Users", foreign_keys=[created_by], back_populates="categories_created"
    )
    updatedby: Mapped["Users"] = relationship(
        "Users", foreign_keys=[updated_by], back_populates="categories_updated"
    )
    deletedby: Mapped["Users"] = relationship(
        "Users", foreign_keys=[deleted_by], back_populates="categories_deleted")
    facilities: Mapped[list["CatalogsFacilities"]] = relationship(
        "CatalogsFacilities", foreign_keys="[CatalogsFacilities.category_id]", back_populates="category"
    )
    

class SubCategory(Base):
    __tablename__ = 'sub_categories'

    id = Column(Integer, primary_key=True,autoincrement=True)
    name = Column(String(255), nullable=False)
    category_id = Column(ForeignKey('category.id'), nullable=False)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.utcnow)
    created_by: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('users.id'))
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP)
    updated_by: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('users.id'))
    deleted_at: Mapped[datetime] = mapped_column(TIMESTAMP)
    deleted_by: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('users.id'))
    

    category:Mapped["Category"] = relationship("Category",back_populates="subcategories")
    createdby: Mapped["Users"] = relationship(
        "Users", foreign_keys=[created_by], back_populates="sub_categories_created"
    )
    
    updatedby: Mapped["Users"] = relationship(
        "Users", foreign_keys=[updated_by], back_populates="sub_categories_updated"
    )
    
    deletedby: Mapped["Users"] = relationship(
        "Users", foreign_keys=[deleted_by], back_populates="sub_categories_deleted")
    facilities: Mapped[list["CatalogsFacilities"]] = relationship(
        "CatalogsFacilities", foreign_keys="[CatalogsFacilities.sub_category_id]", back_populates="sub_category"
    )

class CatalogsFacilities(Base):
    __tablename__ = "catalogs_facilities"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True),primary_key=True,default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    category_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('category.id'),nullable=False)
    sub_category_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('sub_categories.id'),nullable=False)
    location_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('catalogs_locations.id'))
    internal_id: Mapped[str] = mapped_column(String(255),nullable=False)
    description: Mapped[str] = mapped_column(String(500))
    refrigrant_remaining_at_disposal: Mapped[float] = mapped_column(Numeric(5,2),nullable=False)
    gross_area_id: Mapped[int] = mapped_column(BigInteger,ForeignKey('gross_area.id'),nullable=False)
    gross_area_unit_id: Mapped[int] = mapped_column(BigInteger,ForeignKey('gross_area_unit.id'),nullable=False)
    occupancy: Mapped[float] = mapped_column(Numeric(5,2),nullable=False)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.utcnow)
    created_by: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('users.id'))
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP)
    updated_by: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('users.id'))
    deleted_at: Mapped[datetime] = mapped_column(TIMESTAMP)
    deleted_by: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('users.id'))



    category : Mapped["Category"] = relationship(
        "Category", foreign_keys=[category_id], back_populates="facilities")
    sub_category: Mapped["SubCategory"] = relationship(
        "SubCategory", foreign_keys=[sub_category_id],back_populates="facilities")
    location: Mapped["CatalogsLocation"] = relationship(
        "CatalogsLocation", foreign_keys=[location_id],back_populates="facilities")
    gross_area: Mapped["GrossArea"] = relationship(
        "GrossArea", foreign_keys=[gross_area_id],back_populates="facilities")
    gross_area_unit: Mapped["GrossAreaUnit"] = relationship(
        "GrossAreaUnit", foreign_keys=[gross_area_unit_id],back_populates="facilities")
    createdby: Mapped["Users"] = relationship(
        "Users", foreign_keys=[created_by], back_populates="facilities_created")
    updatedby: Mapped["Users"] = relationship(
        "Users", foreign_keys=[updated_by], back_populates="facilities_updated")
    deletedby: Mapped["Users"] = relationship(
        "Users", foreign_keys=[deleted_by], back_populates="facilities_deleted")

class CatalogsFinancedEntities(Base):
    
    __tablename__ = 'catalogs_financed_entity'

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True),primary_key=True,default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    listed: Mapped[bool] = mapped_column(Boolean,nullable=False)
    ticker: Mapped[str] = mapped_column(VARCHAR(25),nullable=True)
    description: Mapped[str] = mapped_column(String(500))
    contact_name: Mapped[str] = mapped_column(String(255))
    contact_email: Mapped[str] = mapped_column(String(255))
    internal_id: Mapped[str] = mapped_column(String(255),nullable=False)
    country_id: Mapped[int] = mapped_column(BigInteger,ForeignKey('general_countries.id'),nullable=False)
    state_id: Mapped[int] = mapped_column(BigInteger,ForeignKey('general_states.id'),nullable=False)
    city_id: Mapped[int] = mapped_column(BigInteger,ForeignKey('general_cities.id'),nullable=False)
    industry_sector_id: Mapped[int] = mapped_column(BigInteger,ForeignKey('industry_sector.id'),nullable=False)
    industry_id: Mapped[int] = mapped_column(BigInteger,ForeignKey('industry.id'),nullable=False)
    sub_industry_id: Mapped[int] = mapped_column(BigInteger,ForeignKey('sub_industry.id'),nullable=False)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.utcnow)
    created_by: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('users.id'))
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP)
    updated_by: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('users.id'))
    deleted_at: Mapped[datetime] = mapped_column(TIMESTAMP)
    deleted_by: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('users.id'))


    country:Mapped["GeneralCountries"] = relationship("GeneralCountries",back_populates="financed_entities")
    state:Mapped["GeneralStates"] = relationship("GeneralStates",back_populates="financed_entities")
    city:Mapped["GeneralCities"] = relationship("GeneralCities",back_populates="financed_entities")
    industrysector:Mapped["IndustrySector"] = relationship("IndustrySector",back_populates="financed_entities")
    industry:Mapped["Industry"] = relationship("Industry",back_populates="financed_entities")
    subindustry:Mapped["SubIndustry"] = relationship("SubIndustry",back_populates="financed_entities")
    createdby: Mapped["Users"] = relationship(
        "Users", foreign_keys=[created_by], back_populates="financed_entities_created"
    )
    
    updatedby: Mapped["Users"] = relationship(
        "Users", foreign_keys=[updated_by], back_populates="financed_entities_updated"
    )
    
    deletedby: Mapped["Users"] = relationship(
        "Users", foreign_keys=[deleted_by], back_populates="financed_entities_deleted"
    )

class CatalogsEquipmentType(Base):
    
    __tablename__ = 'catalogs_equipment_type'

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True),primary_key=True,default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    installation_emission: Mapped[int] = mapped_column(BigInteger, nullable=False)
    operation_emission_per_year: Mapped[int] = mapped_column(BigInteger, nullable=False)
    refrigrant_remaining_at_disposal: Mapped[int] = mapped_column(BigInteger, nullable=False)
    refrigrant_remaining_at_disposal_percentage:Mapped[int] = mapped_column(Numeric(5,2), nullable=False)
    category_id: Mapped[int] = mapped_column(BigInteger,ForeignKey('category.id') ,nullable=False)
    created_at: Mapped[datetime.timestamp] = mapped_column(TIMESTAMP(timezone=True), default=datetime.now(timezone.utc),nullable=False)
    created_by: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('users.id'),nullable=True)
    updated_at: Mapped[datetime.timestamp] = mapped_column(TIMESTAMP(timezone=True),nullable=True)
    updated_by: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('users.id'),nullable=True)
    deleted_at: Mapped[datetime.timestamp] = mapped_column(TIMESTAMP(timezone=True),nullable=True)
    deleted_by: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('users.id'),nullable=True)


    category : Mapped["Category"] = relationship(
        "Category", foreign_keys=[category_id], back_populates="equipment_types")
    createdby: Mapped["Users"] = relationship(
        "Users", foreign_keys=[created_by], back_populates="equipment_types_created"
    )
    
    updatedby: Mapped["Users"] = relationship(
        "Users", foreign_keys=[updated_by], back_populates="equipment_types_updated"
    )
    
    deletedby: Mapped["Users"] = relationship(
        "Users", foreign_keys=[deleted_by], back_populates="equipment_types_deleted"
    )
class UserSalutation(Base):
    __tablename__ = 'user_salutation'
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    salutation: Mapped[str] = mapped_column(String(255))



class SettingsSMTP(Base):
    __tablename__ = 'settings_SMTP'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='settings_SMTP_pkey'),
    )

    id = mapped_column(Integer)
    server = mapped_column(String)
    server_username = mapped_column(String)
    server_password = mapped_column(String)

class SettingsStripe(Base):
    __tablename__ = 'settings_stripe'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='settings_stripe_pkey'),
    )

    id = mapped_column(Integer)
    api_key = mapped_column(String)
    version = mapped_column(String)
    test_api_key = mapped_column(String)
    live_api_key = mapped_column(String)
    success_url = mapped_column(String)
    cancel_url = mapped_column(String)

class SettingsSSO(Base):
    __tablename__ = 'settings_SSO'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='settings_SSO_pkey'),
    )

    id = mapped_column(Integer)
    api_key = mapped_column(String)
    login_url = mapped_column(String)
    signup_url = mapped_column(String)
    forgot_pwd_url = mapped_column(String)
    reset_pwd_url = mapped_column(String)
    change_pwd_url = mapped_column(String)

class SystemOTPSessions(Base):
    __tablename__ = "system_OTP_sessions"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    userId = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    token = Column(String(255), nullable=False)
    last_resend_count = Column(Integer)
    last_resend_at = Column(TIMESTAMP)
    createdAt = Column(TIMESTAMP)
    expiresAt = Column(TIMESTAMP)

class SettingsSession(Base):
    __tablename__ = 'settings_session'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='settings_Session_pkey'),
    )

    id = mapped_column(Integer)
    secret_key = mapped_column(String)
    algorithm = mapped_column(String)
    acs_tkn_expire = mapped_column(Integer)
    rst_tkn_expire = mapped_column(Integer)
    otp_expire = mapped_column(Integer)
    otp_max_count = mapped_column(Integer)
    otp_resend_time = mapped_column(Integer)
    otp_resend_count_reset_time = mapped_column(Integer)



class StripePackage(Base):
    __tablename__ = 'stripe_packages'
    
    id = Column(Integer, primary_key=True)
    subscription_type = Column(VARCHAR(255), nullable=False)
    package_name = Column(VARCHAR(255))
    team = Column(VARCHAR(255))
    state = Column(Boolean)
    recommended = Column(Boolean)
    price_monthly = Column(Integer, nullable=False)
    discount_monthly = Column(Integer)
    discounted_price_yearly = Column(Integer, nullable=False)
    discounted_price_monthly = Column(Integer, nullable=False)
    price_yearly = Column(Integer, nullable=False)
    discount_yearly = Column(Integer)
    digital = Column(Boolean)
    manual = Column(Boolean)
    features = Column(JSON)  # Store features as JSON
    stripe_product_id = Column(VARCHAR(255))  # Store Stripe product ID
    stripe_price_monthly_id = Column(VARCHAR(255))  # Store monthly price ID
    stripe_price_yearly_id = Column(VARCHAR(255))  # Store yearly price ID
    coupon_monthly_id = Column(VARCHAR(255), nullable=True)  # Store monthly coupon ID
    coupon_yearly_id = Column(VARCHAR(255), nullable=True)  # Store yearly coupon ID
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), server_default=func.now(),nullable=False)
    created_by: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('users.id'),nullable=True)
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True),nullable=True)
    updated_by: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('users.id'),nullable=True)
    deleted_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True),nullable=True)
    deleted_by: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('users.id'),nullable=True)
    display= Column(Boolean)
    stripe_features = relationship('StripeFeature', back_populates='stripe_packages', cascade="all, delete-orphan")

# class StripeFeature(Base):
#     __tablename__ = 'stripe_features'
    
#     id = Column(Integer, primary_key=True)
#     package_id = Column(Integer, ForeignKey('stripe_packages.id', ondelete='CASCADE'))
#     title = Column(String(255), nullable=False)
#     caption = Column(String(255), nullable=False)
    
#     stripe_packages = relationship('StripePackage', back_populates='stripe_features')


class StripeFeature(Base):
    __tablename__ = 'stripe_features'
    
    id = Column(Integer, primary_key=True)
    package_id = Column(Integer, ForeignKey('stripe_packages.id', ondelete='CASCADE'))
    title = Column(String(255), nullable=False)
    caption = Column(String(255), nullable=False)
    stripe_feature_id = Column(String(255))  # Store Stripe feature ID
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), server_default=func.now(),nullable=False)
    created_by: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('users.id'),nullable=True)
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True),nullable=True)
    updated_by: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('users.id'),nullable=True)
    deleted_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True),nullable=True)
    deleted_by: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('users.id'),nullable=True)

    # Relationship with StripePackage
    stripe_packages = relationship('StripePackage', back_populates='stripe_features')
