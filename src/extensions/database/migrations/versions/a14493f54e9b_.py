"""empty message

Revision ID: a14493f54e9b
Revises: 
Create Date: 2021-04-15 02:05:57.009557

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a14493f54e9b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('lavoura',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('latitude', sa.Float(precision=32), nullable=False),
    sa.Column('longitude', sa.Float(precision=32), nullable=False),
    sa.Column('tipo', sa.String(length=200), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('produtor_rural',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nome', sa.String(length=200), nullable=False),
    sa.Column('email', sa.String(length=200), nullable=False),
    sa.Column('cpf', sa.String(length=9), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('cpf')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=200), nullable=False),
    sa.Column('name', sa.String(length=200), nullable=True),
    sa.Column('password', sa.String(length=512), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('username')
    )
    op.create_table('perda',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('data', sa.Date(), nullable=False),
    sa.Column('evento', sa.Integer(), nullable=False),
    sa.Column('produtor_rural_id', sa.Integer(), nullable=False),
    sa.Column('lavoura_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['lavoura_id'], ['lavoura.id'], ),
    sa.ForeignKeyConstraint(['produtor_rural_id'], ['produtor_rural.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('perda')
    op.drop_table('user')
    op.drop_table('produtor_rural')
    op.drop_table('lavoura')
    # ### end Alembic commands ###
