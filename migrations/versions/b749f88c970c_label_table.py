"""label table

Revision ID: b749f88c970c
Revises: a0fbd3f7aed6
Create Date: 2022-07-29 00:11:01.600275

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "b749f88c970c"
down_revision = "a0fbd3f7aed6"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "label",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("project_label_id", sa.Integer(), nullable=True),
        sa.Column("image_id", sa.Integer(), nullable=True),
        sa.Column("creator_id", sa.Integer(), nullable=True),
        sa.Column(
            "data", postgresql.JSONB(astext_type=sa.Text()), nullable=False
        ),
        sa.ForeignKeyConstraint(
            ["creator_id"], ["user.id"], ondelete="CASCADE"
        ),
        sa.ForeignKeyConstraint(
            ["image_id"], ["image.id"], ondelete="CASCADE"
        ),
        sa.ForeignKeyConstraint(
            ["project_label_id"], ["projectlabel.id"], ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("label")
    # ### end Alembic commands ###
