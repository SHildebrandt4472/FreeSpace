"""add skills

Revision ID: 54e644f9716e
Revises: 8abf345ca73f
Create Date: 2025-07-04 00:38:00.973727

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '54e644f9716e'
down_revision = '8abf345ca73f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('skill',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('description', sa.String(length=20), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('description')
    )
    op.create_table('user_skill',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('skill_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['skill_id'], ['skill.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('user_id', 'skill_id')
    )
    op.create_table('workspace_skill',
    sa.Column('workspace_id', sa.Integer(), nullable=False),
    sa.Column('skill_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['skill_id'], ['skill.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['workspace_id'], ['work_space.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('workspace_id', 'skill_id')
    )
    with op.batch_alter_table('work_space', schema=None) as batch_op:
        batch_op.alter_column('name',
               existing_type=sa.VARCHAR(length=32),
               type_=sa.String(length=15),
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('work_space', schema=None) as batch_op:
        batch_op.alter_column('name',
               existing_type=sa.String(length=15),
               type_=sa.VARCHAR(length=32),
               existing_nullable=True)

    op.drop_table('workspace_skill')
    op.drop_table('user_skill')
    op.drop_table('skill')
    # ### end Alembic commands ###
