"""Fix hand enchant typo and change gemslot key

Revision ID: e4b97f335683
Revises: 628e222ef99d
Create Date: 2019-08-13 07:44:13.549411

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e4b97f335683'
down_revision = '628e222ef99d'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('characters', schema=None) as batch_op:
        batch_op.alter_column('hand_enchant_name',
                existing_type=sa.String(),
                new_column_name='hands_enchant_name')
        batch_op.alter_column('hand_enchant_description',
                existing_type=sa.String(),
                new_column_name='hands_enchant_description')
        batch_op.alter_column('hand_enchant_quality',
                existing_type=sa.Integer(),
                new_column_name='hands_enchant_quality')
        batch_op.alter_column('hand_enchant_id',
                existing_type=sa.Integer(),
                new_column_name='hands_enchant_id')

    with op.batch_alter_table('characters_gems', schema=None) as batch_op:
        batch_op.add_column(sa.Column('id', sa.Integer(), nullable=False))
        batch_op.alter_column('character_id',
               existing_type=sa.INTEGER(),
               nullable=True)
        batch_op.alter_column('gem_id',
               existing_type=sa.INTEGER(),
               nullable=True)


def downgrade():
    with op.batch_alter_table('characters_gems', schema=None) as batch_op:
        batch_op.alter_column('gem_id',
               existing_type=sa.INTEGER(),
               nullable=False)
        batch_op.alter_column('character_id',
               existing_type=sa.INTEGER(),
               nullable=False)
        batch_op.drop_column('id')

    with op.batch_alter_table('characters', schema=None) as batch_op:
        batch_op.alter_column('hands_enchant_name',
                existing_type=sa.String(),
                new_column_name='hand_enchant_name')
        batch_op.alter_column('hands_enchant_description',
                existing_type=sa.String(),
                new_column_name='hand_enchant_description')
        batch_op.alter_column('hands_enchant_quality',
                existing_type=sa.Integer(),
                new_column_name='hand_enchant_quality')
        batch_op.alter_column('hands_enchant_id',
                existing_type=sa.Integer(),
                new_column_name='hand_enchant_id')
