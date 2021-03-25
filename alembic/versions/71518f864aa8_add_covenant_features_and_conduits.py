"""Add covenant features and conduits

Revision ID: 71518f864aa8
Revises: b4fe69ca33cb
Create Date: 2021-03-24 23:27:55.402520

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '71518f864aa8'
down_revision = 'b4fe69ca33cb'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('characters', schema=None) as batch_op:
        batch_op.add_column(sa.Column('conduit_1_id', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('conduit_1_ilvl', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('conduit_1_name', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('conduit_2_id', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('conduit_2_ilvl', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('conduit_2_name', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('conduit_3_id', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('conduit_3_ilvl', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('conduit_3_name', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('covenant', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('current_soulbind', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('renown', sa.Integer(), nullable=True))


def downgrade():
    with op.batch_alter_table('characters', schema=None) as batch_op:
        batch_op.drop_column('renown')
        batch_op.drop_column('current_soulbind')
        batch_op.drop_column('covenant')
        batch_op.drop_column('conduit_3_name')
        batch_op.drop_column('conduit_3_ilvl')
        batch_op.drop_column('conduit_3_id')
        batch_op.drop_column('conduit_2_name')
        batch_op.drop_column('conduit_2_ilvl')
        batch_op.drop_column('conduit_2_id')
        batch_op.drop_column('conduit_1_name')
        batch_op.drop_column('conduit_1_ilvl')
        batch_op.drop_column('conduit_1_id')
