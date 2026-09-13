"""Create initial content tables.

Revision ID: 0001_initial
Revises:
"""
from alembic import op
import sqlalchemy as sa

revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "events",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("date", sa.Date(), nullable=False),
        sa.Column("start_time", sa.String(length=5), nullable=False),
        sa.Column("end_time", sa.String(length=5)),
        sa.Column("venue", sa.String(length=255), nullable=False),
        sa.Column("city", sa.String(length=120), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("category", sa.String(length=50), nullable=False),
        sa.Column("is_free", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_events_date", "events", ["date"])
    op.create_table(
        "members",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("first_name", sa.String(length=120), nullable=False),
        sa.Column("last_name", sa.String(length=120), nullable=False),
        sa.Column("instrument", sa.String(length=120), nullable=False),
        sa.Column("section", sa.String(length=50), nullable=False),
        sa.Column("joined_year", sa.Integer(), nullable=False),
        sa.Column("role", sa.String(length=120)),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_members_section", "members", ["section"])
    op.create_table(
        "gallery_photos",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("src", sa.String(length=1000), nullable=False),
        sa.Column("alt", sa.String(length=500), nullable=False),
        sa.Column("caption", sa.Text(), nullable=False),
        sa.Column("year", sa.Integer(), nullable=False),
        sa.Column("place", sa.String(length=255), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_table(
        "contact_messages",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.Column("email", sa.String(length=320), nullable=False),
        sa.Column("message", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("is_read", sa.Boolean(), nullable=False, server_default=sa.false()),
    )


def downgrade() -> None:
    op.drop_table("contact_messages")
    op.drop_table("gallery_photos")
    op.drop_index("ix_members_section", table_name="members")
    op.drop_table("members")
    op.drop_index("ix_events_date", table_name="events")
    op.drop_table("events")
