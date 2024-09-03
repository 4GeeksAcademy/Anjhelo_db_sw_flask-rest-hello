"""empty message

Revision ID: c59e8b89d123
Revises: 591a637bcb0e
Create Date: 2024-09-02 16:18:11.072007

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c59e8b89d123'
down_revision = '591a637bcb0e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('people', schema=None) as batch_op:
        batch_op.create_unique_constraint(None, ['birth_year'])
        batch_op.create_unique_constraint(None, ['gender'])

    with op.batch_alter_table('planets', schema=None) as batch_op:
        batch_op.create_unique_constraint(None, ['gravity'])

    with op.batch_alter_table('vehicles', schema=None) as batch_op:
        batch_op.create_unique_constraint(None, ['manufacturer'])
        batch_op.create_unique_constraint(None, ['cost_in_credits'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('vehicles', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')
        batch_op.drop_constraint(None, type_='unique')

    with op.batch_alter_table('planets', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')

    with op.batch_alter_table('people', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')
        batch_op.drop_constraint(None, type_='unique')

    # ### end Alembic commands ###
