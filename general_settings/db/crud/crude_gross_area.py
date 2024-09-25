from general_settings.db.models import GrossArea,GeneralUnit,UserSettings
from general_settings.db.crud.crude_base import CRUDBase
from general_settings.schemas import schemas

crud_gross_area = CRUDBase[GrossArea, schemas.GrossAreaBase, schemas.GrossAreaBase](GrossArea)
crud_unit = CRUDBase[GeneralUnit, schemas.UnitBase, schemas.UnitBase](GeneralUnit)
crud_user_settings = CRUDBase[UserSettings,schemas.UserSettingsCreate,schemas.UserSettingsCreate](UserSettings)

