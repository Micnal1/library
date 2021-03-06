"""empty message

Revision ID: 5d09fc3fa6ef
Revises: 
Create Date: 2021-04-19 20:19:33.680823

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5d09fc3fa6ef'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('author',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('author_name', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_author_author_name'), 'author', ['author_name'], unique=True)
    op.create_table('book',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.Text(), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('created', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('title')
    )
    op.create_index(op.f('ix_book_created'), 'book', ['created'], unique=False)
    op.create_table('books',
    sa.Column('book_id', sa.Integer(), nullable=False),
    sa.Column('author_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['author_id'], ['author.id'], ),
    sa.ForeignKeyConstraint(['book_id'], ['book.id'], ),
    sa.PrimaryKeyConstraint('book_id', 'author_id')
    )
    op.create_table('hire',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('borrower', sa.Text(), nullable=True),
    sa.Column('date_hire', sa.DateTime(), nullable=True),
    sa.Column('where', sa.Text(), nullable=True),
    sa.Column('book_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['book_id'], ['book.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_hire_date_hire'), 'hire', ['date_hire'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_hire_date_hire'), table_name='hire')
    op.drop_table('hire')
    op.drop_table('books')
    op.drop_index(op.f('ix_book_created'), table_name='book')
    op.drop_table('book')
    op.drop_index(op.f('ix_author_author_name'), table_name='author')
    op.drop_table('author')
    # ### end Alembic commands ###
