"""Fixed incorrect column type

Revision ID: 62ddfe32b7db
Revises: cb4a92401965
Create Date: 2020-03-27 21:47:56.581124

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '62ddfe32b7db'
down_revision = 'cb4a92401965'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('characters', schema=None) as batch_op:
        batch_op.alter_column('realm_name',
               existing_type=sa.INTEGER(),
               type_=sa.String(),
               existing_nullable=True)


def downgrade():
    with op.batch_alter_table('characters', schema=None) as batch_op:
        batch_op.alter_column('realm_name',
               existing_type=sa.String(),
               type_=sa.INTEGER(),
               existing_nullable=True)
