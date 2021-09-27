"""Added name column

Revision ID: ba02b8dbcee7
Create Date: 2021-09-22 13:57:28.544480

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ba02b8dbcee7'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(), nullable=True),
    sa.Column('create_date', sa.DateTime(), nullable=True),
    sa.Column('username', sa.String(), nullable=True),
    sa.Column('password', sa.String(), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('username')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)
    op.create_table('items',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=True),
    sa.Column('like', sa.Integer(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('owner_id', sa.Integer(), nullable=True),
    sa.Column('create_date', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['owner_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_items_description'), 'items', ['description'], unique=False)
    op.create_index(op.f('ix_items_id'), 'items', ['id'], unique=False)
    op.create_index(op.f('ix_items_like'), 'items', ['like'], unique=False)
    op.create_index(op.f('ix_items_title'), 'items', ['title'], unique=False)
    op.create_table('comments',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('owner_id', sa.Integer(), nullable=True),
    sa.Column('create_date', sa.DateTime(), nullable=True),
    sa.Column('item_id', sa.Integer(), nullable=True),
    sa.Column('text', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['item_id'], ['items.id'], ),
    sa.ForeignKeyConstraint(['owner_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_comments_id'), 'comments', ['id'], unique=False)
    op.create_index(op.f('ix_comments_text'), 'comments', ['text'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_comments_text'), table_name='comments')
    op.drop_index(op.f('ix_comments_id'), table_name='comments')
    op.drop_table('comments')
    op.drop_index(op.f('ix_items_title'), table_name='items')
    op.drop_index(op.f('ix_items_like'), table_name='items')
    op.drop_index(op.f('ix_items_id'), table_name='items')
    op.drop_index(op.f('ix_items_description'), table_name='items')
    op.drop_table('items')
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
    # ### end Alembic commands ###
