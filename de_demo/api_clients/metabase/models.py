from pydantic import BaseModel, ConfigDict, Field, PositiveInt


class SessionPropertiesResponse(BaseModel):
    setup_token: str = Field(alias="setup-token")
    has_user_setup: bool = Field(alias="has-user-setup")

    model_config = ConfigDict(extra='ignore')


class UserInfo(BaseModel):
    email: str
    first_name: str
    last_name: str


class SitePreferences(BaseModel):
    site_locale: str = "en"
    site_name: str


class User(UserInfo):
    password: str


class SetupRequest(BaseModel):
    invite: UserInfo
    prefs: SitePreferences
    token: str
    user: User


class DatabaseSettings(BaseModel):
    host: str
    port: int
    user: str
    password: str
    dbname: str
    scan_all_databases: bool = Field(False, alias="scan-all-databases")
    ssl: bool = False
    tunnel_enabled: bool = Field(False, alias="tunnel-enabled")
    advanced_options: bool = Field(False, alias="advanced-options")


class AddDatabaseRequest(BaseModel):
    name: str = Field(min_length=1)
    engine: str = Field(min_length=1)
    is_on_demand: bool = False
    cache_ttl: PositiveInt | None = None
    is_full_sync: bool = True
    is_sample: bool = False
    auto_run_queries: bool = True
    details: DatabaseSettings
    schedules: dict = {}
