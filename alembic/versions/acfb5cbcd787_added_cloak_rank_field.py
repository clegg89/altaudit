"""Added cloak rank field

Revision ID: acfb5cbcd787
Revises: 46359a97caea
Create Date: 2020-03-22 19:59:43.534274

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'acfb5cbcd787'
down_revision = '46359a97caea'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('characters', schema=None) as batch_op:
        batch_op.add_column(sa.Column('cloak_rank', sa.Integer(), nullable=True))



def downgrade():
    with op.batch_alter_table('characters', schema=None) as batch_op:
        batch_op.drop_column('cloak_rank')
