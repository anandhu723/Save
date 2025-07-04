"""
Alembic Environment Configuration
Version: 1.0.0
Created: 2025-06-08 23:48:20
Author: anandhu723
"""

from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

from saveai.core.config import Settings

# Load config from alembic.ini
config = context.config

# Set up logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Get database URL from settings
settings = Settings()
config.set_main_option("sqlalchemy.url", str(settings.DATABASE_URL))

def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=None,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=None
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
