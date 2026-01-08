#!/usr/bin/env python3
"""
Export Gold layer tables from DBT DuckDB to CSV
"""

import duckdb
import pandas as pd
from pathlib import Path

# Setup paths
DBT_PROJECT_PATH = Path(__file__).parent / "dbt_project"
GOLD_PATH = Path(__file__).parent / "data" / "gold"
DB_PATH = DBT_PROJECT_PATH / "duckdb.db"  # Changed from target/duckdb.db

# Ensure output directory exists
GOLD_PATH.mkdir(parents=True, exist_ok=True)

# Gold tables to export
GOLD_TABLES = [
    "dim_time",
    "dim_company",
    "dim_location",
    "dim_skills",
    "fact_job_offers",
    "fact_job_skills",
    "agg_job_offers_by_category_time",
    "agg_skills_demand",
    "agg_location_analysis"
]

def export_tables():
    """Export all gold tables to CSV"""
    print(f"\n📊 Exporting Gold Layer Tables to CSV\n")
    print(f"{"=" * 60}")
    
    try:
        # Connect to DuckDB
        if DB_PATH.exists():
            print(f"✓ Using database: {DB_PATH}")
            conn = duckdb.connect(str(DB_PATH), read_only=True)
        else:
            print(f"⚠ Database not found, creating in-memory connection")
            conn = duckdb.connect(":memory:")
            # Load models from schemas if in-memory
            return False
        
        # Export each table
        exported_count = 0
        for table in GOLD_TABLES:
            try:
                # Try different schema patterns
                for schema in ["main_gold", "gold", "main"]:
                    try:
                        query = f"SELECT * FROM {schema}.{table}"
                        
                        df = conn.execute(query).fetchdf()
                        
                        # Export to CSV
                        output_path = GOLD_PATH / f"{table}.csv"
                        df.to_csv(output_path, index=False)
                        
                        print(f"✓ Exported {table:40} ({len(df):>8} rows)")
                        exported_count += 1
                        break
                    except:
                        continue
                        
            except Exception as e:
                print(f"✗ Failed to export {table}: {e}")
        
        print(f"\n{'=' * 60}")
        print(f"✓ Exported {exported_count}/{len(GOLD_TABLES)} tables")
        print(f"✓ Files saved to: {GOLD_PATH}\n")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"✗ Export failed: {e}")
        return False

if __name__ == "__main__":
    success = export_tables()
    exit(0 if success else 1)
