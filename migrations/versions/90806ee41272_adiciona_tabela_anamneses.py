"""adiciona tabela anamneses

Revision ID: 90806ee41272
Revises: aa441ad50823
Create Date: 2026-07-24 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '90806ee41272'
down_revision = 'aa441ad50823'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('anamneses',
    sa.Column('cliente_id', sa.Integer(), nullable=False),
    sa.Column('respostas', sa.JSON(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('data_de_criacao', sa.DateTime(), nullable=False),
    sa.Column('data_de_atualizacao', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['cliente_id'], ['clientes.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('cliente_id')
    )


def downgrade():
    op.drop_table('anamneses')
