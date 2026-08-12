"""allow only one pending payment per order

Revision ID: cc075268000e
Revises: 0c1d027854b1
Create Date: 2026-08-12 09:09:06.937184

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cc075268000e'
down_revision: Union[str, Sequence[str], None] = '0c1d027854b1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_index(
        "ix_payments_one_pending_per_order",
        "payments",
        ["order_id"],
        unique=True,
        postgresql_where=sa.text("status = 'PENDING'"),
    )


def downgrade() -> None:
    op.drop_index(
        "ix_payments_one_pending_per_order",
        table_name="payments",
    )