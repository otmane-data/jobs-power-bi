#!/usr/bin/env python3
"""
Export ALL data layers (Bronze, Silver, Gold) from DBT DuckDB to CSV
"""

import duckdb
import pandas as pd
from pathlib import Path

# Setup paths
DBT_PROJECT_PATH = Path(__file__).parent / "dbt_project"
DATA_PATH = Path(__file__).parent / "data"
DB_PATH = DBT_PROJECT_PATH / "duckdb.db"

# Schemas to export
LAYERS = {
    "bronze": ["stg_jobs_raw"],
    "silver": [
        "int_jobs_cleaned",
        "int_job_title_normalization",
        "int_skills_extraction"
    ],
    "gold": [
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
}

# Schema mapping
SCHEMA_MAP = {
    "bronze": "main_bronze",
    "silver": "main_silver",
    "gold": "main_gold"
}

def export_all_layers():
    """Export all data layers to CSV"""
    print(f"\n📊 Exporting ALL Data Layers (Bronze/Silver/Gold) to CSV\n")
    print(f"{'=' * 70}")
    
    try:
        # Connect to DuckDB
        if not DB_PATH.exists():
            print(f"✗ Database not found at: {DB_PATH}")
            return False
        
        print(f"✓ Using database: {DB_PATH}\n")
        conn = duckdb.connect(str(DB_PATH), read_only=True)
        
        total_exported = 0
        
        # Export each layer
        for layer, tables in LAYERS.items():
            layer_path = DATA_PATH / layer
            layer_path.mkdir(parents=True, exist_ok=True)
            
            schema = SCHEMA_MAP.get(layer, f"main_{layer}")
            print(f"\n🟤 {layer.upper()} Layer → {layer_path}")
            print(f"{'-' * 70}")
            
            for table in tables:
                try:
                    query = f"SELECT * FROM {schema}.{table}"
                    df = conn.execute(query).fetchdf()
                    
                    # Export to CSV
                    output_path = layer_path / f"{table}.csv"
                    df.to_csv(output_path, index=False)
                    
                    row_count = len(df)
                    size_mb = output_path.stat().st_size / (1024 * 1024)
                    
                    print(f"  ✓ {table:45} {row_count:>8} rows  {size_mb:>7.2f} MB")
                    total_exported += 1
                    
                except Exception as e:
                    print(f"  ✗ {table:45} Error: {str(e)[:40]}")
        
        print(f"\n{'=' * 70}")
        print(f"✓ Exported {total_exported}/{sum(len(v) for v in LAYERS.values())} tables")
        print(f"\n📁 Exported to:")
        for layer in LAYERS.keys():
            print(f"   - {DATA_PATH / layer}")
        print()
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"✗ Export failed: {e}")
        return False

if __name__ == "__main__":
    success = export_all_layers()
    exit(0 if success else 1)
