"""Change wrist/hand/feet to just primary enchant

Revision ID: fd43d8c9241b
Revises: 92d85c353d3d
Create Date: 2021-03-23 23:01:18.588699

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fd43d8c9241b'
down_revision = '92d85c353d3d'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('characters', schema=None) as batch_op:
        batch_op.add_column(sa.Column('primary_enchant_description', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('primary_enchant_id', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('primary_enchant_name', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('primary_enchant_quality', sa.Integer(), nullable=True))
        batch_op.drop_column('wrist_enchant_id')
        batch_op.drop_column('hands_enchant_id')
        batch_op.drop_column('feet_enchant_id')
        batch_op.drop_column('wrist_enchant_name')
        batch_op.drop_column('hands_enchant_quality')
        batch_op.drop_column('feet_enchant_description')
        batch_op.drop_column('hands_enchant_description')
        batch_op.drop_column('wrist_enchant_description')
        batch_op.drop_column('feet_enchant_name')
        batch_op.drop_column('hands_enchant_name')
        batch_op.drop_column('wrist_enchant_quality')
        batch_op.drop_column('feet_enchant_quality')


def downgrade():
    with op.batch_alter_table('characters', schema=None) as batch_op:
        batch_op.add_column(sa.Column('feet_enchant_quality', sa.INTEGER(), nullable=True))
        batch_op.add_column(sa.Column('wrist_enchant_quality', sa.INTEGER(), nullable=True))
        batch_op.add_column(sa.Column('hands_enchant_name', sa.VARCHAR(), nullable=True))
        batch_op.add_column(sa.Column('feet_enchant_name', sa.VARCHAR(), nullable=True))
        batch_op.add_column(sa.Column('wrist_enchant_description', sa.VARCHAR(), nullable=True))
        batch_op.add_column(sa.Column('hands_enchant_description', sa.VARCHAR(), nullable=True))
        batch_op.add_column(sa.Column('feet_enchant_description', sa.VARCHAR(), nullable=True))
        batch_op.add_column(sa.Column('hands_enchant_quality', sa.INTEGER(), nullable=True))
        batch_op.add_column(sa.Column('wrist_enchant_name', sa.VARCHAR(), nullable=True))
        batch_op.add_column(sa.Column('feet_enchant_id', sa.INTEGER(), nullable=True))
        batch_op.add_column(sa.Column('hands_enchant_id', sa.INTEGER(), nullable=True))
        batch_op.add_column(sa.Column('wrist_enchant_id', sa.INTEGER(), nullable=True))
        batch_op.drop_column('primary_enchant_quality')
        batch_op.drop_column('primary_enchant_name')
        batch_op.drop_column('primary_enchant_id')
        batch_op.drop_column('primary_enchant_description')
