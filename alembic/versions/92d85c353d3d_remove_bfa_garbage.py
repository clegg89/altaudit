"""Remove BfA garbage

Revision ID: 92d85c353d3d
Revises: e81e4cdf7924
Create Date: 2020-09-22 11:24:40.038632

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '92d85c353d3d'
down_revision = 'e81e4cdf7924'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('characters', schema=None) as batch_op:
        batch_op.add_column(sa.Column('chest_enchant_description', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('chest_enchant_id', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('chest_enchant_name', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('chest_enchant_quality', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('cloak_enchant_description', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('cloak_enchant_id', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('cloak_enchant_name', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('cloak_enchant_quality', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('feet_enchant_description', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('feet_enchant_id', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('feet_enchant_name', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('feet_enchant_quality', sa.Integer(), nullable=True))
        batch_op.drop_constraint('fk_characters_head_tier4_selected_id_azerite_traits', type_='foreignkey')
        batch_op.drop_constraint('fk_characters_shoulder_tier0_selected_id_azerite_traits', type_='foreignkey')
        batch_op.drop_constraint('fk_characters_shoulder_tier2_selected_id_azerite_traits', type_='foreignkey')
        batch_op.drop_constraint('fk_characters_shoulder_tier1_selected_id_azerite_traits', type_='foreignkey')
        batch_op.drop_constraint('fk_characters_chest_tier1_selected_id_azerite_traits', type_='foreignkey')
        batch_op.drop_constraint('fk_characters_chest_tier0_selected_id_azerite_traits', type_='foreignkey')
        batch_op.drop_constraint('fk_characters_shoulder_tier3_selected_id_azerite_traits', type_='foreignkey')
        batch_op.drop_constraint('fk_characters_head_tier0_selected_id_azerite_traits', type_='foreignkey')
        batch_op.drop_constraint('fk_characters_head_tier3_selected_id_azerite_traits', type_='foreignkey')
        batch_op.drop_constraint('fk_characters_chest_tier3_selected_id_azerite_traits', type_='foreignkey')
        batch_op.drop_constraint('fk_characters_head_tier1_selected_id_azerite_traits', type_='foreignkey')
        batch_op.drop_constraint('fk_characters_chest_tier2_selected_id_azerite_traits', type_='foreignkey')
        batch_op.drop_constraint('fk_characters_head_tier2_selected_id_azerite_traits', type_='foreignkey')
        batch_op.drop_constraint('fk_characters_shoulder_tier4_selected_id_azerite_traits', type_='foreignkey')
        batch_op.drop_constraint('fk_characters_chest_tier4_selected_id_azerite_traits', type_='foreignkey')
        batch_op.drop_column('islands_total')
        batch_op.drop_column('chest_tier3_selected_id')
        batch_op.drop_column('cloak_rank')
        batch_op.drop_column('azerite_percentage')
        batch_op.drop_column('shoulder_tier1_selected_id')
        batch_op.drop_column('head_tier4_selected_id')
        batch_op.drop_column('shoulder_tier0_selected_id')
        batch_op.drop_column('shoulder_tier2_selected_id')
        batch_op.drop_column('head_tier2_selected_id')
        batch_op.drop_column('shoulder_tier3_selected_id')
        batch_op.drop_column('island_weekly_done')
        batch_op.drop_column('chest_tier1_selected_id')
        batch_op.drop_column('chest_tier2_selected_id')
        batch_op.drop_column('chest_tier4_selected_id')
        batch_op.drop_column('chest_tier0_selected_id')
        batch_op.drop_column('head_tier0_selected_id')
        batch_op.drop_column('head_tier1_selected_id')
        batch_op.drop_column('shoulder_tier4_selected_id')
        batch_op.drop_column('head_tier3_selected_id')
        batch_op.drop_column('hoa_level')

    op.drop_table('characters_traits_chest_tier0')
    op.drop_table('characters_traits_shoulder_tier1')
    op.drop_table('characters_traits_head_tier0')
    op.drop_table('azerite_traits')
    op.drop_table('characters_traits_chest_tier3')
    op.drop_table('characters_traits_shoulder_tier0')
    op.drop_table('characters_traits_shoulder_tier4')
    op.drop_table('characters_traits_head_tier1')
    op.drop_table('characters_traits_chest_tier4')
    op.drop_table('characters_traits_head_tier3')
    op.drop_table('characters_traits_head_tier2')
    op.drop_table('characters_traits_chest_tier1')
    op.drop_table('characters_traits_chest_tier2')
    op.drop_table('characters_traits_head_tier4')
    op.drop_table('characters_traits_shoulder_tier3')
    op.drop_table('characters_traits_shoulder_tier2')


def downgrade():
    op.create_table('characters_traits_shoulder_tier2',
    sa.Column('character_id', sa.INTEGER(), nullable=True),
    sa.Column('azerite_trait_id', sa.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['azerite_trait_id'], ['azerite_traits.id'], name='fk_characters_traits_shoulder_tier2_azerite_trait_id_azerite_traits'),
    sa.ForeignKeyConstraint(['character_id'], ['characters.id'], name='fk_characters_traits_shoulder_tier2_character_id_characters')
    )
    op.create_table('characters_traits_shoulder_tier3',
    sa.Column('character_id', sa.INTEGER(), nullable=True),
    sa.Column('azerite_trait_id', sa.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['azerite_trait_id'], ['azerite_traits.id'], name='fk_characters_traits_shoulder_tier3_azerite_trait_id_azerite_traits'),
    sa.ForeignKeyConstraint(['character_id'], ['characters.id'], name='fk_characters_traits_shoulder_tier3_character_id_characters')
    )
    op.create_table('characters_traits_head_tier4',
    sa.Column('character_id', sa.INTEGER(), nullable=True),
    sa.Column('azerite_trait_id', sa.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['azerite_trait_id'], ['azerite_traits.id'], name='fk_characters_traits_head_tier4_azerite_trait_id_azerite_traits'),
    sa.ForeignKeyConstraint(['character_id'], ['characters.id'], name='fk_characters_traits_head_tier4_character_id_characters')
    )
    op.create_table('characters_traits_chest_tier2',
    sa.Column('character_id', sa.INTEGER(), nullable=True),
    sa.Column('azerite_trait_id', sa.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['azerite_trait_id'], ['azerite_traits.id'], name='fk_characters_traits_chest_tier2_azerite_trait_id_azerite_traits'),
    sa.ForeignKeyConstraint(['character_id'], ['characters.id'], name='fk_characters_traits_chest_tier2_character_id_characters')
    )
    op.create_table('characters_traits_chest_tier1',
    sa.Column('character_id', sa.INTEGER(), nullable=True),
    sa.Column('azerite_trait_id', sa.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['azerite_trait_id'], ['azerite_traits.id'], name='fk_characters_traits_chest_tier1_azerite_trait_id_azerite_traits'),
    sa.ForeignKeyConstraint(['character_id'], ['characters.id'], name='fk_characters_traits_chest_tier1_character_id_characters')
    )
    op.create_table('characters_traits_head_tier2',
    sa.Column('character_id', sa.INTEGER(), nullable=True),
    sa.Column('azerite_trait_id', sa.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['azerite_trait_id'], ['azerite_traits.id'], name='fk_characters_traits_head_tier2_azerite_trait_id_azerite_traits'),
    sa.ForeignKeyConstraint(['character_id'], ['characters.id'], name='fk_characters_traits_head_tier2_character_id_characters')
    )
    op.create_table('characters_traits_head_tier3',
    sa.Column('character_id', sa.INTEGER(), nullable=True),
    sa.Column('azerite_trait_id', sa.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['azerite_trait_id'], ['azerite_traits.id'], name='fk_characters_traits_head_tier3_azerite_trait_id_azerite_traits'),
    sa.ForeignKeyConstraint(['character_id'], ['characters.id'], name='fk_characters_traits_head_tier3_character_id_characters')
    )
    op.create_table('characters_traits_chest_tier4',
    sa.Column('character_id', sa.INTEGER(), nullable=True),
    sa.Column('azerite_trait_id', sa.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['azerite_trait_id'], ['azerite_traits.id'], name='fk_characters_traits_chest_tier4_azerite_trait_id_azerite_traits'),
    sa.ForeignKeyConstraint(['character_id'], ['characters.id'], name='fk_characters_traits_chest_tier4_character_id_characters')
    )
    op.create_table('characters_traits_head_tier1',
    sa.Column('character_id', sa.INTEGER(), nullable=True),
    sa.Column('azerite_trait_id', sa.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['azerite_trait_id'], ['azerite_traits.id'], name='fk_characters_traits_head_tier1_azerite_trait_id_azerite_traits'),
    sa.ForeignKeyConstraint(['character_id'], ['characters.id'], name='fk_characters_traits_head_tier1_character_id_characters')
    )
    op.create_table('characters_traits_shoulder_tier4',
    sa.Column('character_id', sa.INTEGER(), nullable=True),
    sa.Column('azerite_trait_id', sa.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['azerite_trait_id'], ['azerite_traits.id'], name='fk_characters_traits_shoulder_tier4_azerite_trait_id_azerite_traits'),
    sa.ForeignKeyConstraint(['character_id'], ['characters.id'], name='fk_characters_traits_shoulder_tier4_character_id_characters')
    )
    op.create_table('characters_traits_shoulder_tier0',
    sa.Column('character_id', sa.INTEGER(), nullable=True),
    sa.Column('azerite_trait_id', sa.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['azerite_trait_id'], ['azerite_traits.id'], name='fk_characters_traits_shoulder_tier0_azerite_trait_id_azerite_traits'),
    sa.ForeignKeyConstraint(['character_id'], ['characters.id'], name='fk_characters_traits_shoulder_tier0_character_id_characters')
    )
    op.create_table('characters_traits_chest_tier3',
    sa.Column('character_id', sa.INTEGER(), nullable=True),
    sa.Column('azerite_trait_id', sa.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['azerite_trait_id'], ['azerite_traits.id'], name='fk_characters_traits_chest_tier3_azerite_trait_id_azerite_traits'),
    sa.ForeignKeyConstraint(['character_id'], ['characters.id'], name='fk_characters_traits_chest_tier3_character_id_characters')
    )
    op.create_table('azerite_traits',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('spell_id', sa.INTEGER(), nullable=True),
    sa.Column('name', sa.VARCHAR(), nullable=True),
    sa.Column('icon', sa.VARCHAR(), nullable=True),
    sa.PrimaryKeyConstraint('id', name='pk_azerite_traits')
    )
    op.create_table('characters_traits_head_tier0',
    sa.Column('character_id', sa.INTEGER(), nullable=True),
    sa.Column('azerite_trait_id', sa.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['azerite_trait_id'], ['azerite_traits.id'], name='fk_characters_traits_head_tier0_azerite_trait_id_azerite_traits'),
    sa.ForeignKeyConstraint(['character_id'], ['characters.id'], name='fk_characters_traits_head_tier0_character_id_characters')
    )
    op.create_table('characters_traits_shoulder_tier1',
    sa.Column('character_id', sa.INTEGER(), nullable=True),
    sa.Column('azerite_trait_id', sa.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['azerite_trait_id'], ['azerite_traits.id'], name='fk_characters_traits_shoulder_tier1_azerite_trait_id_azerite_traits'),
    sa.ForeignKeyConstraint(['character_id'], ['characters.id'], name='fk_characters_traits_shoulder_tier1_character_id_characters')
    )
    op.create_table('characters_traits_chest_tier0',
    sa.Column('character_id', sa.INTEGER(), nullable=True),
    sa.Column('azerite_trait_id', sa.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['azerite_trait_id'], ['azerite_traits.id'], name='fk_characters_traits_chest_tier0_azerite_trait_id_azerite_traits'),
    sa.ForeignKeyConstraint(['character_id'], ['characters.id'], name='fk_characters_traits_chest_tier0_character_id_characters')
    )

    with op.batch_alter_table('characters', schema=None) as batch_op:
        batch_op.add_column(sa.Column('hoa_level', sa.INTEGER(), nullable=True))
        batch_op.add_column(sa.Column('head_tier3_selected_id', sa.INTEGER(), nullable=True))
        batch_op.add_column(sa.Column('shoulder_tier4_selected_id', sa.INTEGER(), nullable=True))
        batch_op.add_column(sa.Column('head_tier1_selected_id', sa.INTEGER(), nullable=True))
        batch_op.add_column(sa.Column('head_tier0_selected_id', sa.INTEGER(), nullable=True))
        batch_op.add_column(sa.Column('chest_tier0_selected_id', sa.INTEGER(), nullable=True))
        batch_op.add_column(sa.Column('chest_tier4_selected_id', sa.INTEGER(), nullable=True))
        batch_op.add_column(sa.Column('chest_tier2_selected_id', sa.INTEGER(), nullable=True))
        batch_op.add_column(sa.Column('chest_tier1_selected_id', sa.INTEGER(), nullable=True))
        batch_op.add_column(sa.Column('island_weekly_done', sa.VARCHAR(), nullable=True))
        batch_op.add_column(sa.Column('shoulder_tier3_selected_id', sa.INTEGER(), nullable=True))
        batch_op.add_column(sa.Column('head_tier2_selected_id', sa.INTEGER(), nullable=True))
        batch_op.add_column(sa.Column('shoulder_tier2_selected_id', sa.INTEGER(), nullable=True))
        batch_op.add_column(sa.Column('shoulder_tier0_selected_id', sa.INTEGER(), nullable=True))
        batch_op.add_column(sa.Column('head_tier4_selected_id', sa.INTEGER(), nullable=True))
        batch_op.add_column(sa.Column('shoulder_tier1_selected_id', sa.INTEGER(), nullable=True))
        batch_op.add_column(sa.Column('azerite_percentage', sa.FLOAT(), nullable=True))
        batch_op.add_column(sa.Column('cloak_rank', sa.INTEGER(), nullable=True))
        batch_op.add_column(sa.Column('chest_tier3_selected_id', sa.INTEGER(), nullable=True))
        batch_op.add_column(sa.Column('islands_total', sa.INTEGER(), nullable=True))
        batch_op.create_foreign_key('fk_characters_chest_tier4_selected_id_azerite_traits', 'azerite_traits', ['chest_tier4_selected_id'], ['id'])
        batch_op.create_foreign_key('fk_characters_shoulder_tier4_selected_id_azerite_traits', 'azerite_traits', ['shoulder_tier4_selected_id'], ['id'])
        batch_op.create_foreign_key('fk_characters_head_tier2_selected_id_azerite_traits', 'azerite_traits', ['head_tier2_selected_id'], ['id'])
        batch_op.create_foreign_key('fk_characters_chest_tier2_selected_id_azerite_traits', 'azerite_traits', ['chest_tier2_selected_id'], ['id'])
        batch_op.create_foreign_key('fk_characters_head_tier1_selected_id_azerite_traits', 'azerite_traits', ['head_tier1_selected_id'], ['id'])
        batch_op.create_foreign_key('fk_characters_chest_tier3_selected_id_azerite_traits', 'azerite_traits', ['chest_tier3_selected_id'], ['id'])
        batch_op.create_foreign_key('fk_characters_head_tier3_selected_id_azerite_traits', 'azerite_traits', ['head_tier3_selected_id'], ['id'])
        batch_op.create_foreign_key('fk_characters_head_tier0_selected_id_azerite_traits', 'azerite_traits', ['head_tier0_selected_id'], ['id'])
        batch_op.create_foreign_key('fk_characters_shoulder_tier3_selected_id_azerite_traits', 'azerite_traits', ['shoulder_tier3_selected_id'], ['id'])
        batch_op.create_foreign_key('fk_characters_chest_tier0_selected_id_azerite_traits', 'azerite_traits', ['chest_tier0_selected_id'], ['id'])
        batch_op.create_foreign_key('fk_characters_chest_tier1_selected_id_azerite_traits', 'azerite_traits', ['chest_tier1_selected_id'], ['id'])
        batch_op.create_foreign_key('fk_characters_shoulder_tier1_selected_id_azerite_traits', 'azerite_traits', ['shoulder_tier1_selected_id'], ['id'])
        batch_op.create_foreign_key('fk_characters_shoulder_tier2_selected_id_azerite_traits', 'azerite_traits', ['shoulder_tier2_selected_id'], ['id'])
        batch_op.create_foreign_key('fk_characters_shoulder_tier0_selected_id_azerite_traits', 'azerite_traits', ['shoulder_tier0_selected_id'], ['id'])
        batch_op.create_foreign_key('fk_characters_head_tier4_selected_id_azerite_traits', 'azerite_traits', ['head_tier4_selected_id'], ['id'])
        batch_op.drop_column('feet_enchant_quality')
        batch_op.drop_column('feet_enchant_name')
        batch_op.drop_column('feet_enchant_id')
        batch_op.drop_column('feet_enchant_description')
        batch_op.drop_column('cloak_enchant_quality')
        batch_op.drop_column('cloak_enchant_name')
        batch_op.drop_column('cloak_enchant_id')
        batch_op.drop_column('cloak_enchant_description')
        batch_op.drop_column('chest_enchant_quality')
        batch_op.drop_column('chest_enchant_name')
        batch_op.drop_column('chest_enchant_id')
        batch_op.drop_column('chest_enchant_description')
