import os
class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")
    if not SECRET_KEY:
        import secrets
        SECRET_KEY = secrets.token_hex(32)
        print(
            "⚠️  WARNING: SECRET_KEY environment variable is not set. "
            "Using a random key generated at startup (sessions will invalidate on restart). "
            "Set the SECRET_KEY env var before deploying to production."
        )
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    UPLOAD_FOLDER = os.path.join(BASE_DIR, "static", "uploads" )
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL","sqlite:///database.db")
    if SQLALCHEMY_DATABASE_URI.startswith("sqlite") and os.getenv("VERCEL"):
        print(
            "⚠️  WARNING: Running on Vercel with SQLite. Vercel's filesystem is "
            "ephemeral/read-only, so data written to database.db will NOT persist "
            "between deploys or cold starts. Set DATABASE_URL to a hosted Postgres "
            "database (e.g. Supabase/Neon) before deploying."
        )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER ="smtp.gmail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD= os.getenv("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER= MAIL_USERNAME