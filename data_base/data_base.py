from peewee import (
    AutoField,
    CharField,
    ForeignKeyField,
    Model,
    SqliteDatabase, PrimaryKeyField, DateTimeField
)

db = SqliteDatabase("my_database.db")


class BaseModel(Model):
    class Meta:
        database = db


class Objects(BaseModel):
    id: PrimaryKeyField = PrimaryKeyField(unique=True)
    user_id: CharField = CharField()
    rating: CharField = CharField(null=True)
    genre: CharField = CharField(null=True)
    quan: CharField = CharField(null=True)
    sort_method: CharField = CharField(null=True)

    class Meta:
        table_name: str = "objects"


class Task(BaseModel):
    task_id: AutoField = AutoField()
    user: ForeignKeyField = ForeignKeyField(Objects, backref="tasks")
    title: CharField = CharField()
    due_date: DateTimeField = DateTimeField()
    genre: CharField = CharField(null=True)
    sort_method: CharField = CharField(null=True)
    quantity: CharField = CharField(null=True)

    class Meta:
        table_name: str = "tasks"


db.create_tables([Objects, Task])
