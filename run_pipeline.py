#!/usr/bin/env python3
"""
JOB INTELLIGENT - Data Pipeline Orchestration Script
Purpose: Orchestrate DBT runs and export data to CSV/Parquet
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path
from datetime import datetime

# Configuration
PROJECT_ROOT = Path(__file__).parent
DBT_PROJECT_PATH = PROJECT_ROOT / "dbt_project"
DATA_PATH = PROJECT_ROOT / "data"
GOLD_PATH = DATA_PATH / "gold"
BRONZE_PATH = DATA_PATH / "bronze"
SILVER_PATH = DATA_PATH / "silver"

# Colors for console output
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_section(title):
    """Print a section header"""
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}{Colors.ENDC}\n")

def print_success(message):
    """Print success message"""
    print(f"{Colors.OKGREEN}✓ {message}{Colors.ENDC}")

def print_warning(message):
    """Print warning message"""
    print(f"{Colors.WARNING}⚠ {message}{Colors.ENDC}")

def print_error(message):
    """Print error message"""
    print(f"{Colors.FAIL}✗ {message}{Colors.ENDC}")

def print_info(message):
    """Print info message"""
    print(f"{Colors.OKCYAN}ℹ {message}{Colors.ENDC}")

def run_command(command, cwd=None):
    """Run a shell command"""
    try:
        result = subprocess.run(
            command,
            shell=True,
            cwd=cwd,
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            return True, result.stdout
        else:
            return False, result.stderr
    except Exception as e:
        return False, str(e)

def check_dependencies():
    """Check if required packages are installed"""
    print_section("Checking Dependencies")
    
    dependencies = {
        'dbt': 'dbt-core',
        'duckdb': 'duckdb',
        'pandas': 'pandas'
    }
    
    missing = []
    for name, package in dependencies.items():
        try:
            __import__(name)
            print_success(f"{package} is installed")
        except ImportError:
            print_warning(f"{package} is NOT installed")
            missing.append(package)
    
    if missing:
        print_error(f"\nMissing dependencies: {', '.join(missing)}")
        print_info(f"Install with: pip install {' '.join(missing)}")
        return False
    
    return True

def initialize_dbt():
    """Initialize DBT project"""
    print_section("Initializing DBT")
    
    # Check dbt_project.yml exists
    if not (DBT_PROJECT_PATH / "dbt_project.yml").exists():
        print_error("dbt_project.yml not found!")
        return False
    
    print_info(f"DBT Project Path: {DBT_PROJECT_PATH}")
    
    # Run dbt debug
    success, output = run_command("dbt debug", cwd=DBT_PROJECT_PATH)
    if success:
        print_success("DBT debug passed")
        return True
    else:
        print_error(f"DBT debug failed: {output}")
        return False

def copy_source_data():
    """Copy source data to bronze layer"""
    print_section("Copying Source Data to Bronze Layer")
    
    source_file = PROJECT_ROOT / "final_data.csv"
    bronze_file = BRONZE_PATH / "final_data.csv"
    
    if not source_file.exists():
        print_error(f"Source file not found: {source_file}")
        return False
    
    try:
        shutil.copy2(source_file, bronze_file)
        print_success(f"Copied {source_file.name} to {BRONZE_PATH}")
        
        # Get file size
        size_mb = source_file.stat().st_size / (1024 * 1024)
        print_info(f"File size: {size_mb:.2f} MB")
        
        return True
    except Exception as e:
        print_error(f"Failed to copy file: {e}")
        return False

def run_dbt_transformation():
    """Run DBT transformation"""
    print_section("Running DBT Transformation")
    
    print_info("Executing: dbt run")
    success, output = run_command("dbt run", cwd=DBT_PROJECT_PATH)
    
    if success:
        print_success("DBT run completed successfully")
        print(output)
        return True
    else:
        print_error(f"DBT run failed: {output}")
        return False

def run_dbt_tests():
    """Run DBT tests (optional)"""
    print_section("Running DBT Tests")
    
    print_info("Executing: dbt test")
    success, output = run_command("dbt test", cwd=DBT_PROJECT_PATH)
    
    if success:
        print_success("All tests passed")
        return True
    else:
        print_warning(f"Some tests failed: {output}")
        return True  # Don't fail pipeline

def export_to_csv():
    """Export Gold tables to CSV"""
    print_section("Exporting Gold Layer to CSV")
    
    try:
        import duckdb
        import pandas as pd
    except ImportError:
        print_error("duckdb and pandas required for export")
        return False
    
    try:
        # Connect to DuckDB
        db_path = DBT_PROJECT_PATH / "target" / "duckdb.db"
        
        if not db_path.exists():
            print_warning(f"Database not found: {db_path}")
            print_info("Using in-memory database instead")
            conn = duckdb.connect(":memory:")
        else:
            conn = duckdb.connect(str(db_path))
        
        # List of Gold tables to export
        gold_tables = [
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
        
        for table in gold_tables:
            try:
                # Query the table
                df = conn.execute(f"SELECT * FROM gold.{table}").fetchdf()
                
                # Export to CSV
                output_path = GOLD_PATH / f"{table}.csv"
                df.to_csv(output_path, index=False)
                
                print_success(f"Exported {table} ({len(df)} rows)")
                
            except Exception as e:
                print_warning(f"Failed to export {table}: {e}")
        
        conn.close()
        return True
        
    except Exception as e:
        print_error(f"Export failed: {e}")
        return False

def generate_summary():
    """Generate summary of transformation"""
    print_section("Summary Report")
    
    try:
        # Count files in each layer
        bronze_files = list(BRONZE_PATH.glob("*.csv"))
        silver_files = list(SILVER_PATH.glob("*.csv"))
        gold_files = list(GOLD_PATH.glob("*.csv"))
        
        print(f"\n{Colors.BOLD}Data Layers:{Colors.ENDC}")
        print(f"  🟤 Bronze: {len(bronze_files)} files")
        print(f"  🩶 Silver: {len(silver_files)} files")
        print(f"  🟡 Gold: {len(gold_files)} files")
        
        # Check DBT documentation
        dbt_docs = DBT_PROJECT_PATH / "target"
        if dbt_docs.exists():
            print(f"\n{Colors.BOLD}DBT Documentation:{Colors.ENDC}")
            print(f"  Generated: {dbt_docs}")
            print(f"  Run 'dbt docs serve' to view")
        
        print(f"\n{Colors.BOLD}Next Steps:{Colors.ENDC}")
        print(f"  1. Review data in {GOLD_PATH}")
        print(f"  2. Open Power BI Desktop")
        print(f"  3. Import CSV files from {GOLD_PATH}")
        print(f"  4. Create relationships and dashboards")
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"\n{Colors.OKGREEN}✓ Pipeline completed at {timestamp}{Colors.ENDC}\n")
        
    except Exception as e:
        print_error(f"Failed to generate summary: {e}")

def main():
    """Main orchestration function"""
    
    print(f"\n{Colors.BOLD}{Colors.HEADER}")
    print("  JOB INTELLIGENT - Data Pipeline")
    print(f"{Colors.ENDC}\n")
    
    # Step 1: Check dependencies
    if not check_dependencies():
        print_error("Please install missing dependencies and try again")
        sys.exit(1)
    
    # Step 2: Initialize DBT
    if not initialize_dbt():
        print_error("Failed to initialize DBT")
        sys.exit(1)
    
    # Step 3: Copy source data
    if not copy_source_data():
        print_warning("Failed to copy source data, continuing...")
    
    # Step 4: Run DBT
    if not run_dbt_transformation():
        print_error("DBT transformation failed")
        sys.exit(1)
    
    # Step 5: Run tests (optional)
    run_dbt_tests()
    
    # Step 6: Export to CSV
    if not export_to_csv():
        print_warning("Failed to export CSV files")
    
    # Step 7: Summary
    generate_summary()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print_error("\n\nPipeline interrupted by user")
        sys.exit(1)
    except Exception as e:
        print_error(f"\nFatal error: {e}")
        sys.exit(1)
