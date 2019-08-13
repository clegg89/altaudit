"""baseline

Revision ID: cc67fc067add
Revises:
Create Date: 2019-08-13 11:00:01.734713

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cc67fc067add'
down_revision = None
branch_labels = None
depends_on = None

# Initial database creation

def upgrade():
    op.create_table('azerite_traits',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('spell_id', sa.Integer(), nullable=True),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('icon', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_azerite_traits'))
    )
    op.create_table('classes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_classes'))
    )
    op.create_table('factions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_factions'))
    )
    op.create_table('gems',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('quality', sa.Integer(), nullable=True),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('icon', sa.String(), nullable=True),
    sa.Column('stat', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_gems'))
    )
    op.create_table('regions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_regions'))
    )
    op.create_table('races',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('faction_id', sa.Integer(), nullable=True),
    sa.Column('name', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['faction_id'], ['factions.id'], name=op.f('fk_races_faction_id_factions')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_races'))
    )
    op.create_table('realms',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('region_id', sa.Integer(), nullable=True),
    sa.Column('name', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['region_id'], ['regions.id'], name=op.f('fk_realms_region_id_regions')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_realms')),
    sa.UniqueConstraint('region_id', 'name', name=op.f('uq_realms_region_id_name'))
    )
    op.create_table('characters',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('realm_id', sa.Integer(), nullable=True),
    sa.Column('class_id', sa.Integer(), nullable=True),
    sa.Column('faction_id', sa.Integer(), nullable=True),
    sa.Column('race_id', sa.Integer(), nullable=True),
    sa.Column('head_tier0_selected_id', sa.Integer(), nullable=True),
    sa.Column('head_tier1_selected_id', sa.Integer(), nullable=True),
    sa.Column('head_tier2_selected_id', sa.Integer(), nullable=True),
    sa.Column('head_tier3_selected_id', sa.Integer(), nullable=True),
    sa.Column('head_tier4_selected_id', sa.Integer(), nullable=True),
    sa.Column('shoulder_tier0_selected_id', sa.Integer(), nullable=True),
    sa.Column('shoulder_tier1_selected_id', sa.Integer(), nullable=True),
    sa.Column('shoulder_tier2_selected_id', sa.Integer(), nullable=True),
    sa.Column('shoulder_tier3_selected_id', sa.Integer(), nullable=True),
    sa.Column('shoulder_tier4_selected_id', sa.Integer(), nullable=True),
    sa.Column('chest_tier0_selected_id', sa.Integer(), nullable=True),
    sa.Column('chest_tier1_selected_id', sa.Integer(), nullable=True),
    sa.Column('chest_tier2_selected_id', sa.Integer(), nullable=True),
    sa.Column('chest_tier3_selected_id', sa.Integer(), nullable=True),
    sa.Column('chest_tier4_selected_id', sa.Integer(), nullable=True),
    sa.Column('name_api', sa.String(), nullable=True),
    sa.Column('realm_name', sa.Integer(), nullable=True),
    sa.Column('lastmodified', sa.Integer(), nullable=True),
    sa.Column('level', sa.Integer(), nullable=True),
    sa.Column('mainspec', sa.String(), nullable=True),
    sa.Column('gender', sa.String(), nullable=True),
    sa.Column('avatar', sa.String(), nullable=True),
    sa.Column('bust', sa.String(), nullable=True),
    sa.Column('render', sa.String(), nullable=True),
    sa.Column('estimated_ilvl', sa.Float(), nullable=True),
    sa.Column('head_itemLevel', sa.Integer(), nullable=True),
    sa.Column('head_id', sa.Integer(), nullable=True),
    sa.Column('head_name', sa.String(), nullable=True),
    sa.Column('head_icon', sa.String(), nullable=True),
    sa.Column('head_quality', sa.Integer(), nullable=True),
    sa.Column('neck_itemLevel', sa.Integer(), nullable=True),
    sa.Column('neck_id', sa.Integer(), nullable=True),
    sa.Column('neck_name', sa.String(), nullable=True),
    sa.Column('neck_icon', sa.String(), nullable=True),
    sa.Column('neck_quality', sa.Integer(), nullable=True),
    sa.Column('shoulder_itemLevel', sa.Integer(), nullable=True),
    sa.Column('shoulder_id', sa.Integer(), nullable=True),
    sa.Column('shoulder_name', sa.String(), nullable=True),
    sa.Column('shoulder_icon', sa.String(), nullable=True),
    sa.Column('shoulder_quality', sa.Integer(), nullable=True),
    sa.Column('back_itemLevel', sa.Integer(), nullable=True),
    sa.Column('back_id', sa.Integer(), nullable=True),
    sa.Column('back_name', sa.String(), nullable=True),
    sa.Column('back_icon', sa.String(), nullable=True),
    sa.Column('back_quality', sa.Integer(), nullable=True),
    sa.Column('chest_itemLevel', sa.Integer(), nullable=True),
    sa.Column('chest_id', sa.Integer(), nullable=True),
    sa.Column('chest_name', sa.String(), nullable=True),
    sa.Column('chest_icon', sa.String(), nullable=True),
    sa.Column('chest_quality', sa.Integer(), nullable=True),
    sa.Column('wrist_itemLevel', sa.Integer(), nullable=True),
    sa.Column('wrist_id', sa.Integer(), nullable=True),
    sa.Column('wrist_name', sa.String(), nullable=True),
    sa.Column('wrist_icon', sa.String(), nullable=True),
    sa.Column('wrist_quality', sa.Integer(), nullable=True),
    sa.Column('hands_itemLevel', sa.Integer(), nullable=True),
    sa.Column('hands_id', sa.Integer(), nullable=True),
    sa.Column('hands_name', sa.String(), nullable=True),
    sa.Column('hands_icon', sa.String(), nullable=True),
    sa.Column('hands_quality', sa.Integer(), nullable=True),
    sa.Column('waist_itemLevel', sa.Integer(), nullable=True),
    sa.Column('waist_id', sa.Integer(), nullable=True),
    sa.Column('waist_name', sa.String(), nullable=True),
    sa.Column('waist_icon', sa.String(), nullable=True),
    sa.Column('waist_quality', sa.Integer(), nullable=True),
    sa.Column('legs_itemLevel', sa.Integer(), nullable=True),
    sa.Column('legs_id', sa.Integer(), nullable=True),
    sa.Column('legs_name', sa.String(), nullable=True),
    sa.Column('legs_icon', sa.String(), nullable=True),
    sa.Column('legs_quality', sa.Integer(), nullable=True),
    sa.Column('feet_itemLevel', sa.Integer(), nullable=True),
    sa.Column('feet_id', sa.Integer(), nullable=True),
    sa.Column('feet_name', sa.String(), nullable=True),
    sa.Column('feet_icon', sa.String(), nullable=True),
    sa.Column('feet_quality', sa.Integer(), nullable=True),
    sa.Column('finger1_itemLevel', sa.Integer(), nullable=True),
    sa.Column('finger1_id', sa.Integer(), nullable=True),
    sa.Column('finger1_name', sa.String(), nullable=True),
    sa.Column('finger1_icon', sa.String(), nullable=True),
    sa.Column('finger1_quality', sa.Integer(), nullable=True),
    sa.Column('finger2_itemLevel', sa.Integer(), nullable=True),
    sa.Column('finger2_id', sa.Integer(), nullable=True),
    sa.Column('finger2_name', sa.String(), nullable=True),
    sa.Column('finger2_icon', sa.String(), nullable=True),
    sa.Column('finger2_quality', sa.Integer(), nullable=True),
    sa.Column('trinket1_itemLevel', sa.Integer(), nullable=True),
    sa.Column('trinket1_id', sa.Integer(), nullable=True),
    sa.Column('trinket1_name', sa.String(), nullable=True),
    sa.Column('trinket1_icon', sa.String(), nullable=True),
    sa.Column('trinket1_quality', sa.Integer(), nullable=True),
    sa.Column('trinket2_itemLevel', sa.Integer(), nullable=True),
    sa.Column('trinket2_id', sa.Integer(), nullable=True),
    sa.Column('trinket2_name', sa.String(), nullable=True),
    sa.Column('trinket2_icon', sa.String(), nullable=True),
    sa.Column('trinket2_quality', sa.Integer(), nullable=True),
    sa.Column('mainHand_itemLevel', sa.Integer(), nullable=True),
    sa.Column('mainHand_id', sa.Integer(), nullable=True),
    sa.Column('mainHand_name', sa.String(), nullable=True),
    sa.Column('mainHand_icon', sa.String(), nullable=True),
    sa.Column('mainHand_quality', sa.Integer(), nullable=True),
    sa.Column('offHand_itemLevel', sa.Integer(), nullable=True),
    sa.Column('offHand_id', sa.Integer(), nullable=True),
    sa.Column('offHand_name', sa.String(), nullable=True),
    sa.Column('offHand_icon', sa.String(), nullable=True),
    sa.Column('offHand_quality', sa.Integer(), nullable=True),
    sa.Column('hoa_level', sa.Integer(), nullable=True),
    sa.Column('azerite_experience', sa.Integer(), nullable=True),
    sa.Column('azerite_experience_remaining', sa.Integer(), nullable=True),
    sa.Column('mainHand_enchant_id', sa.Integer(), nullable=True),
    sa.Column('mainHand_enchant_quality', sa.Integer(), nullable=True),
    sa.Column('mainHand_enchant_name', sa.String(), nullable=True),
    sa.Column('mainHand_enchant_description', sa.String(), nullable=True),
    sa.Column('offHand_enchant_id', sa.Integer(), nullable=True),
    sa.Column('offHand_enchant_quality', sa.Integer(), nullable=True),
    sa.Column('offHand_enchant_name', sa.String(), nullable=True),
    sa.Column('offHand_enchant_description', sa.String(), nullable=True),
    sa.Column('finger1_enchant_id', sa.Integer(), nullable=True),
    sa.Column('finger1_enchant_quality', sa.Integer(), nullable=True),
    sa.Column('finger1_enchant_name', sa.String(), nullable=True),
    sa.Column('finger1_enchant_description', sa.String(), nullable=True),
    sa.Column('finger2_enchant_id', sa.Integer(), nullable=True),
    sa.Column('finger2_enchant_quality', sa.Integer(), nullable=True),
    sa.Column('finger2_enchant_name', sa.String(), nullable=True),
    sa.Column('finger2_enchant_description', sa.String(), nullable=True),
    sa.Column('hands_enchant_id', sa.Integer(), nullable=True),
    sa.Column('hands_enchant_quality', sa.Integer(), nullable=True),
    sa.Column('hands_enchant_name', sa.String(), nullable=True),
    sa.Column('hands_enchant_description', sa.String(), nullable=True),
    sa.Column('wrist_enchant_id', sa.Integer(), nullable=True),
    sa.Column('wrist_enchant_quality', sa.Integer(), nullable=True),
    sa.Column('wrist_enchant_name', sa.String(), nullable=True),
    sa.Column('wrist_enchant_description', sa.String(), nullable=True),
    sa.Column('empty_sockets', sa.Integer(), nullable=True),
    sa.Column('primary1_name', sa.String(), nullable=True),
    sa.Column('primary1_icon', sa.String(), nullable=True),
    sa.Column('primary1_classic_level', sa.Integer(), nullable=True),
    sa.Column('primary1_classic_max', sa.Integer(), nullable=True),
    sa.Column('primary1_burning_crusade_level', sa.Integer(), nullable=True),
    sa.Column('primary1_burning_crusade_max', sa.Integer(), nullable=True),
    sa.Column('primary1_wrath_of_the_lich_king_level', sa.Integer(), nullable=True),
    sa.Column('primary1_wrath_of_the_lich_king_max', sa.Integer(), nullable=True),
    sa.Column('primary1_cataclysm_level', sa.Integer(), nullable=True),
    sa.Column('primary1_cataclysm_max', sa.Integer(), nullable=True),
    sa.Column('primary1_mists_of_pandaria_level', sa.Integer(), nullable=True),
    sa.Column('primary1_mists_of_pandaria_max', sa.Integer(), nullable=True),
    sa.Column('primary1_warlords_of_draenor_level', sa.Integer(), nullable=True),
    sa.Column('primary1_warlords_of_draenor_max', sa.Integer(), nullable=True),
    sa.Column('primary1_legion_level', sa.Integer(), nullable=True),
    sa.Column('primary1_legion_max', sa.Integer(), nullable=True),
    sa.Column('primary1_battle_for_azeroth_level', sa.Integer(), nullable=True),
    sa.Column('primary1_battle_for_azeroth_max', sa.Integer(), nullable=True),
    sa.Column('primary2_name', sa.String(), nullable=True),
    sa.Column('primary2_icon', sa.String(), nullable=True),
    sa.Column('primary2_classic_level', sa.Integer(), nullable=True),
    sa.Column('primary2_classic_max', sa.Integer(), nullable=True),
    sa.Column('primary2_burning_crusade_level', sa.Integer(), nullable=True),
    sa.Column('primary2_burning_crusade_max', sa.Integer(), nullable=True),
    sa.Column('primary2_wrath_of_the_lich_king_level', sa.Integer(), nullable=True),
    sa.Column('primary2_wrath_of_the_lich_king_max', sa.Integer(), nullable=True),
    sa.Column('primary2_cataclysm_level', sa.Integer(), nullable=True),
    sa.Column('primary2_cataclysm_max', sa.Integer(), nullable=True),
    sa.Column('primary2_mists_of_pandaria_level', sa.Integer(), nullable=True),
    sa.Column('primary2_mists_of_pandaria_max', sa.Integer(), nullable=True),
    sa.Column('primary2_warlords_of_draenor_level', sa.Integer(), nullable=True),
    sa.Column('primary2_warlords_of_draenor_max', sa.Integer(), nullable=True),
    sa.Column('primary2_legion_level', sa.Integer(), nullable=True),
    sa.Column('primary2_legion_max', sa.Integer(), nullable=True),
    sa.Column('primary2_battle_for_azeroth_level', sa.Integer(), nullable=True),
    sa.Column('primary2_battle_for_azeroth_max', sa.Integer(), nullable=True),
    sa.Column('cooking_name', sa.String(), nullable=True),
    sa.Column('cooking_icon', sa.String(), nullable=True),
    sa.Column('cooking_classic_level', sa.Integer(), nullable=True),
    sa.Column('cooking_classic_max', sa.Integer(), nullable=True),
    sa.Column('cooking_burning_crusade_level', sa.Integer(), nullable=True),
    sa.Column('cooking_burning_crusade_max', sa.Integer(), nullable=True),
    sa.Column('cooking_wrath_of_the_lich_king_level', sa.Integer(), nullable=True),
    sa.Column('cooking_wrath_of_the_lich_king_max', sa.Integer(), nullable=True),
    sa.Column('cooking_cataclysm_level', sa.Integer(), nullable=True),
    sa.Column('cooking_cataclysm_max', sa.Integer(), nullable=True),
    sa.Column('cooking_mists_of_pandaria_level', sa.Integer(), nullable=True),
    sa.Column('cooking_mists_of_pandaria_max', sa.Integer(), nullable=True),
    sa.Column('cooking_warlords_of_draenor_level', sa.Integer(), nullable=True),
    sa.Column('cooking_warlords_of_draenor_max', sa.Integer(), nullable=True),
    sa.Column('cooking_legion_level', sa.Integer(), nullable=True),
    sa.Column('cooking_legion_max', sa.Integer(), nullable=True),
    sa.Column('cooking_battle_for_azeroth_level', sa.Integer(), nullable=True),
    sa.Column('cooking_battle_for_azeroth_max', sa.Integer(), nullable=True),
    sa.Column('fishing_name', sa.String(), nullable=True),
    sa.Column('fishing_icon', sa.String(), nullable=True),
    sa.Column('fishing_classic_level', sa.Integer(), nullable=True),
    sa.Column('fishing_classic_max', sa.Integer(), nullable=True),
    sa.Column('fishing_burning_crusade_level', sa.Integer(), nullable=True),
    sa.Column('fishing_burning_crusade_max', sa.Integer(), nullable=True),
    sa.Column('fishing_wrath_of_the_lich_king_level', sa.Integer(), nullable=True),
    sa.Column('fishing_wrath_of_the_lich_king_max', sa.Integer(), nullable=True),
    sa.Column('fishing_cataclysm_level', sa.Integer(), nullable=True),
    sa.Column('fishing_cataclysm_max', sa.Integer(), nullable=True),
    sa.Column('fishing_mists_of_pandaria_level', sa.Integer(), nullable=True),
    sa.Column('fishing_mists_of_pandaria_max', sa.Integer(), nullable=True),
    sa.Column('fishing_warlords_of_draenor_level', sa.Integer(), nullable=True),
    sa.Column('fishing_warlords_of_draenor_max', sa.Integer(), nullable=True),
    sa.Column('fishing_legion_level', sa.Integer(), nullable=True),
    sa.Column('fishing_legion_max', sa.Integer(), nullable=True),
    sa.Column('fishing_battle_for_azeroth_level', sa.Integer(), nullable=True),
    sa.Column('fishing_battle_for_azeroth_max', sa.Integer(), nullable=True),
    sa.Column('archaeology_name', sa.String(), nullable=True),
    sa.Column('archaeology_icon', sa.String(), nullable=True),
    sa.Column('archaeology_level', sa.Integer(), nullable=True),
    sa.Column('archaeology_max', sa.Integer(), nullable=True),
    sa.Column('reputations', sa.String(), nullable=True),
    sa.Column('island_weekly_done', sa.String(), nullable=True),
    sa.Column('islands_total', sa.Integer(), nullable=True),
    sa.Column('world_quests_total', sa.Integer(), nullable=True),
    sa.Column('weekly_event_done', sa.String(), nullable=True),
    sa.Column('dungeons_total', sa.Integer(), nullable=True),
    sa.Column('dungeons_each_total', sa.String(), nullable=True),
    sa.Column('raiderio_score', sa.Float(), nullable=True),
    sa.Column('mplus_weekly_highest', sa.Integer(), nullable=True),
    sa.Column('mplus_season_highest', sa.Integer(), nullable=True),
    sa.Column('raids_raid_finder', sa.String(), nullable=True),
    sa.Column('raids_raid_finder_weekly', sa.String(), nullable=True),
    sa.Column('raids_normal', sa.String(), nullable=True),
    sa.Column('raids_normal_weekly', sa.String(), nullable=True),
    sa.Column('raids_heroic', sa.String(), nullable=True),
    sa.Column('raids_heroic_weekly', sa.String(), nullable=True),
    sa.Column('raids_mythic', sa.String(), nullable=True),
    sa.Column('raids_mythic_weekly', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['chest_tier0_selected_id'], ['azerite_traits.id'], name=op.f('fk_characters_chest_tier0_selected_id_azerite_traits')),
    sa.ForeignKeyConstraint(['chest_tier1_selected_id'], ['azerite_traits.id'], name=op.f('fk_characters_chest_tier1_selected_id_azerite_traits')),
    sa.ForeignKeyConstraint(['chest_tier2_selected_id'], ['azerite_traits.id'], name=op.f('fk_characters_chest_tier2_selected_id_azerite_traits')),
    sa.ForeignKeyConstraint(['chest_tier3_selected_id'], ['azerite_traits.id'], name=op.f('fk_characters_chest_tier3_selected_id_azerite_traits')),
    sa.ForeignKeyConstraint(['chest_tier4_selected_id'], ['azerite_traits.id'], name=op.f('fk_characters_chest_tier4_selected_id_azerite_traits')),
    sa.ForeignKeyConstraint(['class_id'], ['classes.id'], name=op.f('fk_characters_class_id_classes')),
    sa.ForeignKeyConstraint(['faction_id'], ['factions.id'], name=op.f('fk_characters_faction_id_factions')),
    sa.ForeignKeyConstraint(['head_tier0_selected_id'], ['azerite_traits.id'], name=op.f('fk_characters_head_tier0_selected_id_azerite_traits')),
    sa.ForeignKeyConstraint(['head_tier1_selected_id'], ['azerite_traits.id'], name=op.f('fk_characters_head_tier1_selected_id_azerite_traits')),
    sa.ForeignKeyConstraint(['head_tier2_selected_id'], ['azerite_traits.id'], name=op.f('fk_characters_head_tier2_selected_id_azerite_traits')),
    sa.ForeignKeyConstraint(['head_tier3_selected_id'], ['azerite_traits.id'], name=op.f('fk_characters_head_tier3_selected_id_azerite_traits')),
    sa.ForeignKeyConstraint(['head_tier4_selected_id'], ['azerite_traits.id'], name=op.f('fk_characters_head_tier4_selected_id_azerite_traits')),
    sa.ForeignKeyConstraint(['race_id'], ['races.id'], name=op.f('fk_characters_race_id_races')),
    sa.ForeignKeyConstraint(['realm_id'], ['realms.id'], name=op.f('fk_characters_realm_id_realms')),
    sa.ForeignKeyConstraint(['shoulder_tier0_selected_id'], ['azerite_traits.id'], name=op.f('fk_characters_shoulder_tier0_selected_id_azerite_traits')),
    sa.ForeignKeyConstraint(['shoulder_tier1_selected_id'], ['azerite_traits.id'], name=op.f('fk_characters_shoulder_tier1_selected_id_azerite_traits')),
    sa.ForeignKeyConstraint(['shoulder_tier2_selected_id'], ['azerite_traits.id'], name=op.f('fk_characters_shoulder_tier2_selected_id_azerite_traits')),
    sa.ForeignKeyConstraint(['shoulder_tier3_selected_id'], ['azerite_traits.id'], name=op.f('fk_characters_shoulder_tier3_selected_id_azerite_traits')),
    sa.ForeignKeyConstraint(['shoulder_tier4_selected_id'], ['azerite_traits.id'], name=op.f('fk_characters_shoulder_tier4_selected_id_azerite_traits')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_characters')),
    sa.UniqueConstraint('realm_id', 'name', name=op.f('uq_characters_realm_id_name'))
    )
    op.create_table('characters_gems',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('character_id', sa.Integer(), nullable=True),
    sa.Column('gem_id', sa.Integer(), nullable=True),
    sa.Column('slot', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['character_id'], ['characters.id'], name=op.f('fk_characters_gems_character_id_characters')),
    sa.ForeignKeyConstraint(['gem_id'], ['gems.id'], name=op.f('fk_characters_gems_gem_id_gems')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_characters_gems'))
    )
    op.create_table('characters_traits_chest_tier0',
    sa.Column('character_id', sa.Integer(), nullable=True),
    sa.Column('azerite_trait_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['azerite_trait_id'], ['azerite_traits.id'], name=op.f('fk_characters_traits_chest_tier0_azerite_trait_id_azerite_traits')),
    sa.ForeignKeyConstraint(['character_id'], ['characters.id'], name=op.f('fk_characters_traits_chest_tier0_character_id_characters'))
    )
    op.create_table('characters_traits_chest_tier1',
    sa.Column('character_id', sa.Integer(), nullable=True),
    sa.Column('azerite_trait_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['azerite_trait_id'], ['azerite_traits.id'], name=op.f('fk_characters_traits_chest_tier1_azerite_trait_id_azerite_traits')),
    sa.ForeignKeyConstraint(['character_id'], ['characters.id'], name=op.f('fk_characters_traits_chest_tier1_character_id_characters'))
    )
    op.create_table('characters_traits_chest_tier2',
    sa.Column('character_id', sa.Integer(), nullable=True),
    sa.Column('azerite_trait_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['azerite_trait_id'], ['azerite_traits.id'], name=op.f('fk_characters_traits_chest_tier2_azerite_trait_id_azerite_traits')),
    sa.ForeignKeyConstraint(['character_id'], ['characters.id'], name=op.f('fk_characters_traits_chest_tier2_character_id_characters'))
    )
    op.create_table('characters_traits_chest_tier3',
    sa.Column('character_id', sa.Integer(), nullable=True),
    sa.Column('azerite_trait_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['azerite_trait_id'], ['azerite_traits.id'], name=op.f('fk_characters_traits_chest_tier3_azerite_trait_id_azerite_traits')),
    sa.ForeignKeyConstraint(['character_id'], ['characters.id'], name=op.f('fk_characters_traits_chest_tier3_character_id_characters'))
    )
    op.create_table('characters_traits_chest_tier4',
    sa.Column('character_id', sa.Integer(), nullable=True),
    sa.Column('azerite_trait_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['azerite_trait_id'], ['azerite_traits.id'], name=op.f('fk_characters_traits_chest_tier4_azerite_trait_id_azerite_traits')),
    sa.ForeignKeyConstraint(['character_id'], ['characters.id'], name=op.f('fk_characters_traits_chest_tier4_character_id_characters'))
    )
    op.create_table('characters_traits_head_tier0',
    sa.Column('character_id', sa.Integer(), nullable=True),
    sa.Column('azerite_trait_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['azerite_trait_id'], ['azerite_traits.id'], name=op.f('fk_characters_traits_head_tier0_azerite_trait_id_azerite_traits')),
    sa.ForeignKeyConstraint(['character_id'], ['characters.id'], name=op.f('fk_characters_traits_head_tier0_character_id_characters'))
    )
    op.create_table('characters_traits_head_tier1',
    sa.Column('character_id', sa.Integer(), nullable=True),
    sa.Column('azerite_trait_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['azerite_trait_id'], ['azerite_traits.id'], name=op.f('fk_characters_traits_head_tier1_azerite_trait_id_azerite_traits')),
    sa.ForeignKeyConstraint(['character_id'], ['characters.id'], name=op.f('fk_characters_traits_head_tier1_character_id_characters'))
    )
    op.create_table('characters_traits_head_tier2',
    sa.Column('character_id', sa.Integer(), nullable=True),
    sa.Column('azerite_trait_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['azerite_trait_id'], ['azerite_traits.id'], name=op.f('fk_characters_traits_head_tier2_azerite_trait_id_azerite_traits')),
    sa.ForeignKeyConstraint(['character_id'], ['characters.id'], name=op.f('fk_characters_traits_head_tier2_character_id_characters'))
    )
    op.create_table('characters_traits_head_tier3',
    sa.Column('character_id', sa.Integer(), nullable=True),
    sa.Column('azerite_trait_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['azerite_trait_id'], ['azerite_traits.id'], name=op.f('fk_characters_traits_head_tier3_azerite_trait_id_azerite_traits')),
    sa.ForeignKeyConstraint(['character_id'], ['characters.id'], name=op.f('fk_characters_traits_head_tier3_character_id_characters'))
    )
    op.create_table('characters_traits_head_tier4',
    sa.Column('character_id', sa.Integer(), nullable=True),
    sa.Column('azerite_trait_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['azerite_trait_id'], ['azerite_traits.id'], name=op.f('fk_characters_traits_head_tier4_azerite_trait_id_azerite_traits')),
    sa.ForeignKeyConstraint(['character_id'], ['characters.id'], name=op.f('fk_characters_traits_head_tier4_character_id_characters'))
    )
    op.create_table('characters_traits_shoulder_tier0',
    sa.Column('character_id', sa.Integer(), nullable=True),
    sa.Column('azerite_trait_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['azerite_trait_id'], ['azerite_traits.id'], name=op.f('fk_characters_traits_shoulder_tier0_azerite_trait_id_azerite_traits')),
    sa.ForeignKeyConstraint(['character_id'], ['characters.id'], name=op.f('fk_characters_traits_shoulder_tier0_character_id_characters'))
    )
    op.create_table('characters_traits_shoulder_tier1',
    sa.Column('character_id', sa.Integer(), nullable=True),
    sa.Column('azerite_trait_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['azerite_trait_id'], ['azerite_traits.id'], name=op.f('fk_characters_traits_shoulder_tier1_azerite_trait_id_azerite_traits')),
    sa.ForeignKeyConstraint(['character_id'], ['characters.id'], name=op.f('fk_characters_traits_shoulder_tier1_character_id_characters'))
    )
    op.create_table('characters_traits_shoulder_tier2',
    sa.Column('character_id', sa.Integer(), nullable=True),
    sa.Column('azerite_trait_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['azerite_trait_id'], ['azerite_traits.id'], name=op.f('fk_characters_traits_shoulder_tier2_azerite_trait_id_azerite_traits')),
    sa.ForeignKeyConstraint(['character_id'], ['characters.id'], name=op.f('fk_characters_traits_shoulder_tier2_character_id_characters'))
    )
    op.create_table('characters_traits_shoulder_tier3',
    sa.Column('character_id', sa.Integer(), nullable=True),
    sa.Column('azerite_trait_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['azerite_trait_id'], ['azerite_traits.id'], name=op.f('fk_characters_traits_shoulder_tier3_azerite_trait_id_azerite_traits')),
    sa.ForeignKeyConstraint(['character_id'], ['characters.id'], name=op.f('fk_characters_traits_shoulder_tier3_character_id_characters'))
    )
    op.create_table('characters_traits_shoulder_tier4',
    sa.Column('character_id', sa.Integer(), nullable=True),
    sa.Column('azerite_trait_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['azerite_trait_id'], ['azerite_traits.id'], name=op.f('fk_characters_traits_shoulder_tier4_azerite_trait_id_azerite_traits')),
    sa.ForeignKeyConstraint(['character_id'], ['characters.id'], name=op.f('fk_characters_traits_shoulder_tier4_character_id_characters'))
    )
    op.create_table('years',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('character_id', sa.Integer(), nullable=False),
    sa.Column('year', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['character_id'], ['characters.id'], name=op.f('fk_years_character_id_characters')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_years')),
    sa.UniqueConstraint('character_id', 'year', name=op.f('uq_years_character_id_year'))
    )
    op.create_table('weeks',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('year_id', sa.Integer(), nullable=False),
    sa.Column('week', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['year_id'], ['years.id'], name=op.f('fk_weeks_year_id_years')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_weeks')),
    sa.UniqueConstraint('year_id', 'week', name=op.f('uq_weeks_year_id_week'))
    )
    op.create_table('snapshots',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('week_id', sa.Integer(), nullable=False),
    sa.Column('world_quests', sa.Integer(), nullable=True),
    sa.Column('dungeons', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['week_id'], ['weeks.id'], name=op.f('fk_snapshots_week_id_weeks')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_snapshots')),
    sa.UniqueConstraint('week_id', name=op.f('uq_snapshots_week_id'))
    )


def downgrade():
    op.drop_table('snapshots')
    op.drop_table('weeks')
    op.drop_table('years')
    op.drop_table('characters_traits_shoulder_tier4')
    op.drop_table('characters_traits_shoulder_tier3')
    op.drop_table('characters_traits_shoulder_tier2')
    op.drop_table('characters_traits_shoulder_tier1')
    op.drop_table('characters_traits_shoulder_tier0')
    op.drop_table('characters_traits_head_tier4')
    op.drop_table('characters_traits_head_tier3')
    op.drop_table('characters_traits_head_tier2')
    op.drop_table('characters_traits_head_tier1')
    op.drop_table('characters_traits_head_tier0')
    op.drop_table('characters_traits_chest_tier4')
    op.drop_table('characters_traits_chest_tier3')
    op.drop_table('characters_traits_chest_tier2')
    op.drop_table('characters_traits_chest_tier1')
    op.drop_table('characters_traits_chest_tier0')
    op.drop_table('characters_gems')
    op.drop_table('characters')
    op.drop_table('realms')
    op.drop_table('races')
    op.drop_table('regions')
    op.drop_table('gems')
    op.drop_table('factions')
    op.drop_table('classes')
    op.drop_table('azerite_traits')
