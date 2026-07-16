
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '73b21af81ff1'
down_revision: Union[str, Sequence[str], None] = '91f0a0413ac7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    bind = op.get_bind()
    columns = [c["name"] for c in sa.inspect(bind).get_columns("session")]

    # Reflex's dev db-sync can add nullable columns ahead of this script running,
    # so only add it here if it isn't already present.
    if "expires_at" not in columns:
        with op.batch_alter_table('session', schema=None) as batch_op:
            batch_op.add_column(sa.Column('expires_at', sa.DateTime(), nullable=True))

    # Backfill existing sessions so they expire 7 days after they were created,
    # matching Session.SESSION_LIFETIME, instead of leaving them NULL.
    op.execute(
        "UPDATE session SET expires_at = datetime(created_at, '+7 days') WHERE expires_at IS NULL"
    )

    with op.batch_alter_table('session', schema=None) as batch_op:
        batch_op.alter_column('expires_at', nullable=False)


def downgrade() -> None:
    with op.batch_alter_table('session', schema=None) as batch_op:
        batch_op.drop_column('expires_at')
