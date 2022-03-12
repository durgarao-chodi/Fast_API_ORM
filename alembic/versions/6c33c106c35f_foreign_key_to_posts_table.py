"""Foreign Key To Posts Table

Revision ID: 6c33c106c35f
Revises: 0c9229c2887c
Create Date: 2022-03-12 21:27:14.499483

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6c33c106c35f'
down_revision = '0c9229c2887c'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts',sa.Column('owner_id',sa.Integer(),nullable=False))
    op.create_foreign_key('posts_users_fk',source_table='posts',referent_table='users',local_cols=['owner_id'],
    remote_cols=['id'],ondelete='CASCADE')
    pass


def downgrade():
    op.drop_constraint('posts_users_fk',table_name='posts')
    op.drop_column('posts','Owner_id')
    pass
