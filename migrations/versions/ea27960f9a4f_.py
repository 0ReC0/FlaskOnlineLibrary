"""empty message

Revision ID: ea27960f9a4f
Revises: 1aa0bac23362
Create Date: 2021-04-12 22:04:02.294179

"""

# revision identifiers, used by Alembic.
revision = 'ea27960f9a4f'
down_revision = '1aa0bac23362'

from alembic import op
import sqlalchemy as sa


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('book',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=80), nullable=True),
    sa.Column('image_name', sa.String(length=300), nullable=True),
    sa.Column('image_data', sa.LargeBinary(), nullable=True),
    sa.Column('file_name', sa.String(length=300), nullable=True),
    sa.Column('file_data', sa.LargeBinary(), nullable=True),
    sa.Column('author', sa.String(length=80), nullable=True),
    sa.Column('is_private', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('roles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), server_default='', nullable=False),
    sa.Column('label', sa.Unicode(length=255), server_default='', nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.Unicode(length=255), server_default='', nullable=False),
    sa.Column('email_confirmed_at', sa.DateTime(), nullable=True),
    sa.Column('password', sa.String(length=255), server_default='', nullable=False),
    sa.Column('is_active', sa.Boolean(), server_default='0', nullable=False),
    sa.Column('first_name', sa.Unicode(length=50), server_default='', nullable=False),
    sa.Column('last_name', sa.Unicode(length=50), server_default='', nullable=False),
    sa.Column('api_key', sa.Unicode(length=20), server_default='', nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('users_roles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('role_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['role_id'], ['roles.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('user_roles')
    op.drop_table('role')
    op.drop_table('user')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('username', sa.VARCHAR(length=50), nullable=False),
    sa.Column('password', sa.VARCHAR(length=255), server_default=sa.text("('')"), nullable=False),
    sa.Column('reset_password_token', sa.VARCHAR(length=100), server_default=sa.text("('')"), nullable=False),
    sa.Column('email', sa.VARCHAR(length=255), nullable=False),
    sa.Column('confirmed_at', sa.DATETIME(), nullable=True),
    sa.Column('is_active', sa.BOOLEAN(), server_default=sa.text("'0'"), nullable=False),
    sa.Column('first_name', sa.VARCHAR(length=50), server_default=sa.text("('')"), nullable=False),
    sa.Column('last_name', sa.VARCHAR(length=50), server_default=sa.text("('')"), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('role',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('name', sa.VARCHAR(length=50), nullable=True),
    sa.Column('description', sa.VARCHAR(length=255), server_default=sa.text("('')"), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('user_roles',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('user_id', sa.INTEGER(), nullable=True),
    sa.Column('role_id', sa.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['role_id'], ['role.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('users_roles')
    op.drop_table('users')
    op.drop_table('roles')
    op.drop_table('book')
    # ### end Alembic commands ###
