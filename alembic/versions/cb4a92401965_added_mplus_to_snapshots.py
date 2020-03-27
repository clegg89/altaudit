"""Added mplus to snapshots

Revision ID: cb4a92401965
Revises: acfb5cbcd787
Create Date: 2020-03-27 09:57:16.433327

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cb4a92401965'
down_revision = 'acfb5cbcd787'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('snapshots', schema=None) as batch_op:
        batch_op.add_column(sa.Column('highest_mplus', sa.Integer(), nullable=True))


def downgrade():
    with op.batch_alter_table('snapshots', schema=None) as batch_op:
        batch_op.drop_column('highest_mplus')
