"""Added corruption resistance column

Revision ID: a85f1df955ea
Revises: 62ddfe32b7db
Create Date: 2020-06-17 15:59:09.833867

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a85f1df955ea'
down_revision = '62ddfe32b7db'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('characters', schema=None) as batch_op:
        batch_op.add_column(sa.Column('cloak_resistance', sa.Integer(), nullable=True))


def downgrade():
    with op.batch_alter_table('characters', schema=None) as batch_op:
        batch_op.drop_column('cloak_resistance')
