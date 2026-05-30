import pandas as pd
from sqlalchemy import create_engine

DATABASE_URL = (
    "postgresql://postgres:6/.2vWpN84+dyvr@db.ciqhcsgfgqlfpxfhifjw.supabase.co:5432/postgres"
)

engine = create_engine(DATABASE_URL)

try:

    df = pd.read_sql(
        """
        SELECT table_name
        FROM information_schema.tables
        LIMIT 20
        """,
        engine
    )

    print(df)

    print("✅ CONEXIÓN EXITOSA")

except Exception as e:

    print("❌ ERROR:")
    print(e)