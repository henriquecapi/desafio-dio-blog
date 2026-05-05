import sqlalchemy as sa

from database import metadata

posts = sa.Table(
    "posts",
    metadata,
    sa.Column("id", sa.Integer, primary_key=True),
    sa.Column("title", sa.String(150), nullable=False, unique=True),
    sa.Column("content", sa.String, nullable=False),
    sa.Column("published_at", sa.DateTime, nullable=True),
    sa.Column("published", sa.Boolean, default=False),
)

users = sa.Table(
    "users",
    metadata,
    sa.Column("id", sa.Integer, primary_key=True),
    sa.Column("email", sa.String(150), nullable=False, unique=True),
    sa.Column("senha", sa.String, nullable=True),
    sa.Column("created_at", sa.DateTime, nullable=True),
    sa.Column("token", sa.String(256), nullable=False),
    sa.Column("updated_at", sa.DateTime, nullable=False),
)
