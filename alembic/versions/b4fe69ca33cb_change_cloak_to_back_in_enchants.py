"""Change cloak to back in enchants

Revision ID: b4fe69ca33cb
Revises: fd43d8c9241b
Create Date: 2021-03-24 18:05:11.893218

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b4fe69ca33cb'
down_revision = 'fd43d8c9241b'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('characters', schema=None) as batch_op:
        batch_op.add_column(sa.Column('back_enchant_description', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('back_enchant_id', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('back_enchant_name', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('back_enchant_quality', sa.Integer(), nullable=True))
        batch_op.drop_column('cloak_enchant_id')
        batch_op.drop_column('cloak_enchant_quality')
        batch_op.drop_column('cloak_enchant_description')
        batch_op.drop_column('cloak_enchant_name')


def downgrade():
    with op.batch_alter_table('characters', schema=None) as batch_op:
        batch_op.add_column(sa.Column('cloak_enchant_name', sa.VARCHAR(), nullable=True))
        batch_op.add_column(sa.Column('cloak_enchant_description', sa.VARCHAR(), nullable=True))
        batch_op.add_column(sa.Column('cloak_enchant_quality', sa.INTEGER(), nullable=True))
        batch_op.add_column(sa.Column('cloak_enchant_id', sa.INTEGER(), nullable=True))
        batch_op.drop_column('back_enchant_quality')
        batch_op.drop_column('back_enchant_name')
        batch_op.drop_column('back_enchant_id')
        batch_op.drop_column('back_enchant_description')
