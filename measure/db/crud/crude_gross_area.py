from measure.db.models import CatalogsUserCompanyAssignment,CatalogsCustomer,CatalogsSupplier,CatalogsEquipmentType, GrossArea,CatalogsFacilities,CatalogsProduct,CatalogsFinancedEntities
from measure.db.crud.crude_base import CRUDBase
from measure.schemas import schemas

# crud_gross_area = CRUDBase[GrossArea, schemas.GrossAreaBase, schemas.GrossAreaBase](GrossArea)

crud_facilities = CRUDBase[CatalogsFacilities, schemas.FacilitiesCreate, schemas.FacilitiesCreate](CatalogsFacilities)

crud_financed_entities = CRUDBase[CatalogsFinancedEntities, schemas.FinancedEntitiesCreate, schemas.FinancedEntitiesCreate](CatalogsFinancedEntities)
crud_equipment_type = CRUDBase[CatalogsEquipmentType, schemas.EquipmentTypeCreate, schemas.EquipmentTypeCreate](CatalogsEquipmentType)
crud_product = CRUDBase[CatalogsProduct, schemas.ProductCreate, schemas.ProductCreate](CatalogsProduct)
crud_supplier = CRUDBase[CatalogsSupplier,schemas.SupplierCreate,schemas.SupplierCreate](CatalogsSupplier)
crud_customer = CRUDBase[CatalogsCustomer,schemas.CustomerCreate,schemas.CustomerCreate](CatalogsCustomer)
crud_user_company_assignment = CRUDBase[CatalogsUserCompanyAssignment,schemas.UserCompanyAssignmentCreate,schemas.UserCompanyAssignmentCreate](CatalogsUserCompanyAssignment)
