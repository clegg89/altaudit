"""Remove corruption resistance column

Revision ID: e81e4cdf7924
Revises: a85f1df955ea
Create Date: 2020-09-22 10:42:48.115826

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e81e4cdf7924'
down_revision = 'a85f1df955ea'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('characters', schema=None) as batch_op:
        batch_op.drop_column('cloak_resistance')


def downgrade():
    with op.batch_alter_table('characters', schema=None) as batch_op:
        batch_op.add_column(sa.Column('cloak_resistance', sa.INTEGER(), nullable=True))
