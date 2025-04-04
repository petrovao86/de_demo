from json import loads

from infi.clickhouse_orm.fields import Field, LowCardinalityField, NullableField, BaseIntField


class MapField(Field):
    class_default = None

    def __init__(
            self,
            key_type: Field,
            value_type: Field,
            default=None,
            alias=None,
            materialized=None,
            readonly=None,
            codec=None
    ):
        key_field = key_type
        if isinstance(key_field, LowCardinalityField):
            key_field = key_field.inner_field

        if isinstance(key_field, NullableField) or isinstance(key_field, BaseIntField):
            raise ValueError("MapField don't support Nullable and Int keys!")

        self.key_type = key_type
        self.value_type = value_type
        super(MapField, self).__init__(default=default, alias=alias,
                                       materialized=materialized, readonly=readonly,
                                       codec=codec)

    def to_python(self, value, timezone_in_use):
        if value is None:
            return {}
        if isinstance(value, str):
            return {
                self.key_type.to_python(k, timezone_in_use): self.value_type.to_python(v, timezone_in_use)
                for k, v in loads(value.replace("'", "\"")).items()
            }
        elif isinstance(value, dict):
            return {
                self.key_type.to_python(k, timezone_in_use): self.value_type.to_python(v, timezone_in_use)
                for k, v in value.items()
            }
        raise ValueError(f"Invalid value for MapField '{value}'")

    def validate(self, value):
        if isinstance(value, dict):
            for key, val in value.items():
                self.key_type.validate(key)
                self.value_type.validate(val)
        else:
            raise ValueError(f"Invalid value for MapField '{value}'s")

    def to_db_string(self, value, quote=True):
        items = []
        for k, v in value.items():
            items.append(f"{self.key_type.to_db_string(k)}: {self.value_type.to_db_string(v)}")

        return f"{{{', '.join(items)}}}"

    def get_sql(self, with_default_expression=True, db=None):
        sql = (f"Map("
               f"{self.key_type.get_sql(with_default_expression=False, db=db)}, "
               f"{self.value_type.get_sql(with_default_expression=False, db=db)})")
        if with_default_expression:
            sql = f"{sql} DEFAULT {self.class_default or 'map()'}"

        return sql
