"""Peewee migrations -- 001_auto.py.

Some examples (model - class or model name)::

    > Model = migrator.orm['model_name']            # Return model in current state by name

    > migrator.sql(sql)                             # Run custom SQL
    > migrator.python(func, *args, **kwargs)        # Run python code
    > migrator.create_model(Model)                  # Create a model (could be used as decorator)
    > migrator.remove_model(model, cascade=True)    # Remove a model
    > migrator.add_fields(model, **fields)          # Add fields to a model
    > migrator.change_fields(model, **fields)       # Change fields
    > migrator.remove_fields(model, *field_names, cascade=True)
    > migrator.rename_field(model, old_field_name, new_field_name)
    > migrator.rename_table(model, new_table_name)
    > migrator.add_index(model, *col_names, unique=False)
    > migrator.drop_index(model, *col_names)
    > migrator.add_not_null(model, *field_names)
    > migrator.drop_not_null(model, *field_names)
    > migrator.add_default(model, field_name, default)

"""

import datetime as dt
import peewee as pw
from decimal import ROUND_HALF_EVEN

try:
    import playhouse.postgres_ext as pw_pext
except ImportError:
    pass

SQL = pw.SQL


def migrate(migrator, database, fake=False, **kwargs):
    """Write your migrations here."""

    @migrator.create_model
    class UnionLottoModel(pw.Model):
        issue = pw.IntegerField(primary_key=True)
        red1 = pw.IntegerField()
        red2 = pw.IntegerField()
        red3 = pw.IntegerField()
        red4 = pw.IntegerField()
        red5 = pw.IntegerField()
        red6 = pw.IntegerField()
        blue = pw.IntegerField()

        class Meta:
            table_name = "unionlottomodel"
            indexes = ['issue', 'red1', 'red2', 'red3', 'red4', 'red5', 'red6', 'blue']

    @migrator.create_model
    class UnionLottoExtendModel(pw.Model):
        issue = pw.ForeignKeyField(backref='infos', column_name='issue_id', field='issue', model=migrator.orm['unionlottomodel'], on_delete='CASCADE', primary_key=True)
        sale = pw.IntegerField(null=True)
        residue = pw.IntegerField(null=True)
        url = pw.CharField(max_length=200, null=True)
        lottery_dates = pw.DateField(null=True)
        limite_dates = pw.DateField(null=True)
        prize_1_count = pw.IntegerField(constraints=[SQL("DEFAULT 0")])
        prize_2_count = pw.IntegerField(constraints=[SQL("DEFAULT 0")])
        prize_3_count = pw.IntegerField(constraints=[SQL("DEFAULT 0")])
        prize_4_count = pw.IntegerField(constraints=[SQL("DEFAULT 0")])
        prize_5_count = pw.IntegerField(constraints=[SQL("DEFAULT 0")])
        prize_6_count = pw.IntegerField(constraints=[SQL("DEFAULT 0")])
        prize_1_money = pw.IntegerField(constraints=[SQL("DEFAULT 0")])
        prize_2_money = pw.IntegerField(constraints=[SQL("DEFAULT 0")])
        prize_3_money = pw.IntegerField(constraints=[SQL("DEFAULT 3000")])
        prize_4_money = pw.IntegerField(constraints=[SQL("DEFAULT 200")])
        prize_5_money = pw.IntegerField(constraints=[SQL("DEFAULT 10")])
        prize_6_money = pw.IntegerField(constraints=[SQL("DEFAULT 5")])

        class Meta:
            table_name = "unionlottoextendmodel"



def rollback(migrator, database, fake=False, **kwargs):
    """Write your rollback migrations here."""

    migrator.remove_model('unionlottoextendmodel')

    migrator.remove_model('unionlottomodel')
