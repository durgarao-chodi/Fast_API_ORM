"""add_last_few_columns_to_posts_table

Revision ID: 8682abc21633
Revises: 6c33c106c35f
Create Date: 2022-03-12 21:35:11.114563

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8682abc21633'
down_revision = '6c33c106c35f'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts',sa.Column('published',sa.Boolean(),nullable=False,server_default='TRUE'))
    op.add_column('posts',sa.Column('created_at',sa.TIMESTAMP(timezone=True),nullable=False,server_default=sa.text('NOW()')))
    pass


def downgrade():
    op.drop_column('posts','published')
    op.drop_column('posts','created_at')
    pass
