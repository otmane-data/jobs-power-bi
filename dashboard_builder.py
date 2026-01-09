#!/usr/bin/env python3
"""
Power BI Dashboard Builder
Génère automatiquement les 6 dashboards pour JOB INTELLIGENT
"""

import json
import pandas as pd
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any

class DashboardBuilder:
    """Construire les dashboards Power BI"""
    
    def __init__(self):
        self.csv_folder = Path("d:\\lab2\\data\\gold")
        self.output_dir = Path("d:\\lab2")
        self.log = []
    
    def log_action(self, msg: str, status: str = "✓"):
        timestamp = datetime.now().strftime("%H:%M:%S")
        message = f"[{timestamp}] {status} {msg}"
        self.log.append(message)
        print(message)
    
    # ==========================================
    # DASHBOARD DEFINITIONS
    # ==========================================
    
    def define_all_dashboards(self) -> Dict[str, Dict]:
        """Définir tous les 6 dashboards avec détails complets"""
        self.log_action("Defining dashboards...\n")
        
        dashboards = {
            "Overview": self._dashboard_overview(),
            "Job_Categories": self._dashboard_job_categories(),
            "Skills_Analysis": self._dashboard_skills_analysis(),
            "Geographic": self._dashboard_geographic(),
            "Companies": self._dashboard_companies(),
            "Trends": self._dashboard_trends(),
        }
        
        return dashboards
    
    def _dashboard_overview(self) -> Dict[str, Any]:
        """Dashboard 1: Overview - KPI Summary"""
        self.log_action("  📊 Dashboard 1: Overview (KPI Cards)")
        
        return {
            "name": "Overview",
            "title": "📊 Overview - Key Metrics",
            "description": "High-level KPI summary",
            "layout": "grid",
            "visuals": [
                {
                    "position": (0, 0),
                    "width": 2,
                    "height": 2,
                    "type": "Card",
                    "title": "Total Jobs",
                    "measure": "Total Jobs",
                    "format": "0,0",
                    "color": "#0078D4",
                    "fontsize": 28
                },
                {
                    "position": (2, 0),
                    "width": 2,
                    "height": 2,
                    "type": "Card",
                    "title": "Total Companies",
                    "measure": "Total Companies",
                    "format": "0,0",
                    "color": "#107C10",
                    "fontsize": 28
                },
                {
                    "position": (4, 0),
                    "width": 2,
                    "height": 2,
                    "type": "Card",
                    "title": "Total Locations",
                    "measure": "Total Locations",
                    "format": "0,0",
                    "color": "#FFB900",
                    "fontsize": 28
                },
                {
                    "position": (6, 0),
                    "width": 2,
                    "height": 2,
                    "type": "Card",
                    "title": "Total Skills",
                    "measure": "Total Skills",
                    "format": "0",
                    "color": "#C50F1F",
                    "fontsize": 28
                },
            ]
        }
    
    def _dashboard_job_categories(self) -> Dict[str, Any]:
        """Dashboard 2: Job Categories"""
        self.log_action("  📈 Dashboard 2: Job Categories (Analysis)")
        
        return {
            "name": "Job_Categories",
            "title": "📈 Job Categories Analysis",
            "description": "Jobs breakdown by category",
            "layout": "grid",
            "visuals": [
                {
                    "position": (0, 0),
                    "width": 4,
                    "height": 3,
                    "type": "ColumnChart",
                    "title": "Jobs by Category",
                    "x_axis": "fact_job_offers[job_category]",
                    "y_axis": "Total Jobs",
                    "color": "#0078D4",
                    "sort": "descending"
                },
                {
                    "position": (4, 0),
                    "width": 4,
                    "height": 3,
                    "type": "PieChart",
                    "title": "Category Distribution",
                    "legend": "fact_job_offers[job_category]",
                    "values": "Total Jobs",
                    "data_labels": True
                },
                {
                    "position": (0, 3),
                    "width": 8,
                    "height": 2,
                    "type": "Table",
                    "title": "Category Details",
                    "columns": [
                        "fact_job_offers[job_category]",
                        "Total Jobs",
                        "Data Engineer Count",
                        "Data Scientist Count",
                        "Data Analyst Count",
                        "ML Engineer Count"
                    ]
                }
            ]
        }
    
    def _dashboard_skills_analysis(self) -> Dict[str, Any]:
        """Dashboard 3: Skills Analysis"""
        self.log_action("  🎯 Dashboard 3: Skills Analysis (Top 20)")
        
        return {
            "name": "Skills_Analysis",
            "title": "🎯 Skills Analysis",
            "description": "Top skills in demand",
            "layout": "grid",
            "visuals": [
                {
                    "position": (0, 0),
                    "width": 6,
                    "height": 3,
                    "type": "BarChart",
                    "title": "Top 20 Skills in Demand",
                    "x_axis": "fact_job_skills[skill_name]",
                    "y_axis": "COUNT(fact_job_skills[job_offer_id])",
                    "limit": 20,
                    "sort": "descending",
                    "color": "#107C10"
                },
                {
                    "position": (6, 0),
                    "width": 2,
                    "height": 3,
                    "type": "KPI",
                    "title": "Skills per Job",
                    "measure": "Skills per Job",
                    "format": "0.0",
                    "color": "#FFB900"
                },
                {
                    "position": (0, 3),
                    "width": 8,
                    "height": 2,
                    "type": "Table",
                    "title": "Skills Demand",
                    "columns": [
                        "fact_job_skills[skill_name]",
                        "dim_skills[skill_category]",
                        "COUNT(fact_job_skills[job_offer_id])"
                    ],
                    "sort_column": "COUNT(fact_job_skills[job_offer_id])",
                    "limit": 15
                }
            ]
        }
    
    def _dashboard_geographic(self) -> Dict[str, Any]:
        """Dashboard 4: Geographic"""
        self.log_action("  🗺️  Dashboard 4: Geographic Analysis (Maps)")
        
        return {
            "name": "Geographic",
            "title": "🗺️  Geographic Analysis",
            "description": "Jobs distribution by location",
            "layout": "grid",
            "visuals": [
                {
                    "position": (0, 0),
                    "width": 4,
                    "height": 3,
                    "type": "Map",
                    "title": "Jobs by Location",
                    "location": "dim_location[city]",
                    "latitude": "dim_location[latitude]",
                    "longitude": "dim_location[longitude]",
                    "size": "Total Jobs",
                    "color": "% Remote Jobs"
                },
                {
                    "position": (4, 0),
                    "width": 4,
                    "height": 3,
                    "type": "ColumnChart",
                    "title": "Top 10 Locations",
                    "x_axis": "dim_location[city]",
                    "y_axis": "Total Jobs",
                    "limit": 10,
                    "color": "#107C10"
                },
                {
                    "position": (0, 3),
                    "width": 8,
                    "height": 2,
                    "type": "Table",
                    "title": "Location Details",
                    "columns": [
                        "dim_location[city]",
                        "dim_location[country]",
                        "Total Jobs",
                        "% Remote Jobs"
                    ],
                    "sort_column": "Total Jobs",
                    "limit": 15
                }
            ]
        }
    
    def _dashboard_companies(self) -> Dict[str, Any]:
        """Dashboard 5: Companies"""
        self.log_action("  🏢 Dashboard 5: Companies (Top Hiring)")
        
        return {
            "name": "Companies",
            "title": "🏢 Top Hiring Companies",
            "description": "Companies analysis",
            "layout": "grid",
            "visuals": [
                {
                    "position": (0, 0),
                    "width": 4,
                    "height": 3,
                    "type": "BarChart",
                    "title": "Top 15 Companies",
                    "x_axis": "dim_company[company_name]",
                    "y_axis": "Total Jobs",
                    "limit": 15,
                    "sort": "descending",
                    "color": "#0078D4"
                },
                {
                    "position": (4, 0),
                    "width": 4,
                    "height": 3,
                    "type": "ScatterChart",
                    "title": "Company Hiring Patterns",
                    "x_axis": "dim_company[company_name]",
                    "y_axis": "Total Jobs",
                    "size": "Skills per Job",
                    "limit": 15,
                    "color": "#FFB900"
                },
                {
                    "position": (0, 3),
                    "width": 8,
                    "height": 2,
                    "type": "Table",
                    "title": "Company Details",
                    "columns": [
                        "dim_company[company_name]",
                        "Total Jobs",
                        "Avg Description Length",
                        "Avg Word Count"
                    ],
                    "sort_column": "Total Jobs",
                    "limit": 10
                }
            ]
        }
    
    def _dashboard_trends(self) -> Dict[str, Any]:
        """Dashboard 6: Trends"""
        self.log_action("  📉 Dashboard 6: Trends (Time Series)")
        
        return {
            "name": "Trends",
            "title": "📉 Trends Analysis",
            "description": "Time-based analysis",
            "layout": "grid",
            "visuals": [
                {
                    "position": (0, 0),
                    "width": 4,
                    "height": 3,
                    "type": "LineChart",
                    "title": "Jobs Posted Over Time",
                    "x_axis": "dim_time[date_id]",
                    "y_axis": "Total Jobs",
                    "color": "#0078D4"
                },
                {
                    "position": (4, 0),
                    "width": 4,
                    "height": 3,
                    "type": "AreaChart",
                    "title": "Monthly Trend",
                    "x_axis": "dim_time[month]",
                    "y_axis": "Total Jobs",
                    "color": "#107C10"
                },
                {
                    "position": (0, 3),
                    "width": 8,
                    "height": 2,
                    "type": "Matrix",
                    "title": "Year vs Month Analysis",
                    "rows": "dim_time[year]",
                    "columns": "dim_time[month]",
                    "values": "Total Jobs",
                    "conditional_formatting": True
                }
            ]
        }
    
    # ==========================================
    # GENERATE POWER BI SCRIPT
    # ==========================================
    
    def generate_powerbi_import_script(self, dashboards: Dict[str, Dict]) -> str:
        """Générer un script d'import pour Power BI"""
        self.log_action("\nGenerating Power BI import script...")
        
        script = """// Power BI Dashboard Automation Script
// For: JOB INTELLIGENT
// Generated: """ + datetime.now().isoformat() + """

// ==================================================
// SECTION 1: IMPORT DATA (POWER QUERY - M Language)
// ==================================================

// Query: Load fact_job_offers
let
    Source = Csv.Document(File.Contents("d:\\lab2\\data\\gold\\fact_job_offers.csv"),[Delimiter=",",Columns=null,Encoding=65001,QuoteStyle=QuoteStyle.None]),
    PromoteHeaders = Table.PromoteHeaders(Source,[PromoteAllScalars=true]),
    ChangeTypes = Table.TransformColumnTypes(PromoteHeaders,{})
in
    ChangeTypes

// ==================================================
// SECTION 2: CREATE RELATIONSHIPS
// ==================================================

// Relationship 1: fact_job_offers[published_date_id] -> dim_time[date_id]
// Relationship 2: fact_job_offers[company_id] -> dim_company[company_id]
// Relationship 3: fact_job_offers[location_id] -> dim_location[location_id]
// Relationship 4: fact_job_skills[job_offer_id] -> fact_job_offers[job_offer_id]
// Relationship 5: fact_job_skills[skill_id] -> dim_skills[skill_id]

// ==================================================
// SECTION 3: CREATE MEASURES (DAX)
// ==================================================

"""
        
        # Add all measures
        measures_dax = {
            "Total Jobs": "COUNTA(fact_job_offers[job_offer_id])",
            "Total Companies": "DISTINCTCOUNT(fact_job_offers[company_name])",
            "Total Locations": "DISTINCTCOUNT(fact_job_offers[location])",
            "Total Skills": "DISTINCTCOUNT(fact_job_skills[skill_name])",
            "% Remote Jobs": "DIVIDE(CALCULATE(COUNTA(fact_job_offers[job_offer_id]),fact_job_offers[is_remote]=1),COUNTA(fact_job_offers[job_offer_id]))",
            "% Permanent Jobs": "DIVIDE(CALCULATE(COUNTA(fact_job_offers[job_offer_id]),fact_job_offers[is_permanent]=1),COUNTA(fact_job_offers[job_offer_id]))",
            "Avg Description Length": "AVERAGE(fact_job_offers[description_length])",
            "Avg Word Count": "AVERAGE(fact_job_offers[word_count])",
            "Data Engineer Count": "CALCULATE(COUNTA(fact_job_offers[job_offer_id]),fact_job_offers[job_category]=\"Data Engineer\")",
            "Data Scientist Count": "CALCULATE(COUNTA(fact_job_offers[job_offer_id]),fact_job_offers[job_category]=\"Data Scientist\")",
            "Data Analyst Count": "CALCULATE(COUNTA(fact_job_offers[job_offer_id]),fact_job_offers[job_category]=\"Data Analyst\")",
            "ML Engineer Count": "CALCULATE(COUNTA(fact_job_offers[job_offer_id]),fact_job_offers[job_category]=\"ML Engineer\")",
            "Jobs Last 30 Days": "CALCULATE(COUNTA(fact_job_offers[job_offer_id]),fact_job_offers[published_date]>=TODAY()-30)",
            "Jobs Last 90 Days": "CALCULATE(COUNTA(fact_job_offers[job_offer_id]),fact_job_offers[published_date]>=TODAY()-90)",
            "Skills per Job": "DIVIDE(COUNTA(fact_job_skills[skill_id]),COUNTA(fact_job_offers[job_offer_id]))",
            "Top Skill Count": "MAXX(ALL(fact_job_skills[skill_name]),COUNTA(fact_job_skills[job_offer_id]))",
        }
        
        for measure_name, dax in measures_dax.items():
            script += f"// {measure_name}\n{measure_name} = {dax}\n\n"
        
        script += """
// ==================================================
// SECTION 4: DASHBOARD PAGES
// ==================================================

"""
        
        # Add dashboard specs
        for page_num, (dash_name, dash_info) in enumerate(dashboards.items(), 1):
            script += f"// Page {page_num}: {dash_info['title']}\n"
            script += f"// Description: {dash_info['description']}\n"
            script += f"// Visuals: {len(dash_info['visuals'])}\n\n"
            
            for visual in dash_info['visuals']:
                script += f"  - {visual['type']}: {visual['title']}\n"
            
            script += "\n"
        
        return script
    
    # ==========================================
    # GENERATE DASHBOARD SPECIFICATIONS
    # ==========================================
    
    def generate_dashboard_specifications(self, dashboards: Dict[str, Dict]) -> str:
        """Générer les spécifications détaillées des dashboards"""
        self.log_action("Generating dashboard specifications...")
        
        spec = """# Power BI Dashboard Specifications

## Overview

- **Total Dashboards**: 6
- **Total Visuals**: 19
- **Data Tables**: 9
- **Measures**: 16

---

"""
        
        for page_num, (dash_id, dash_info) in enumerate(dashboards.items(), 1):
            spec += f"""## Dashboard {page_num}: {dash_info['title']}

**Description**: {dash_info['description']}

### Visuals ({len(dash_info['visuals'])}):

"""
            
            for visual_num, visual in enumerate(dash_info['visuals'], 1):
                spec += f"""### {visual_num}. {visual['title']}
- **Type**: {visual['type']}
- **Position**: {visual.get('position', 'N/A')}
- **Size**: {visual.get('width', 'auto')}x{visual.get('height', 'auto')}

"""
                
                # Add visual-specific details
                if visual['type'] == 'Card':
                    spec += f"- **Measure**: {visual.get('measure', 'N/A')}\n"
                    spec += f"- **Format**: {visual.get('format', '0')}\n"
                
                elif visual['type'] in ['ColumnChart', 'BarChart', 'LineChart', 'AreaChart']:
                    spec += f"- **X-Axis**: {visual.get('x_axis', 'N/A')}\n"
                    spec += f"- **Y-Axis**: {visual.get('y_axis', 'N/A')}\n"
                
                elif visual['type'] == 'PieChart':
                    spec += f"- **Legend**: {visual.get('legend', 'N/A')}\n"
                    spec += f"- **Values**: {visual.get('values', 'N/A')}\n"
                
                elif visual['type'] == 'Table':
                    spec += f"- **Columns**: {', '.join(visual.get('columns', []))}\n"
                
                spec += "\n"
            
            spec += "---\n\n"
        
        return spec
    
    # ==========================================
    # GENERATE STEP-BY-STEP GUIDE
    # ==========================================
    
    def generate_step_by_step_guide(self, dashboards: Dict[str, Dict]) -> str:
        """Générer un guide étape par étape pour créer les dashboards"""
        self.log_action("Generating step-by-step guide...")
        
        guide = """# Power BI Dashboard Creation Guide

## Quick Summary

You have 6 dashboards to create with 19 visuals total. Follow this guide step-by-step.

---

## Before You Start

1. ✅ Power BI Desktop installed
2. ✅ 9 CSV files imported
3. ✅ 5 relationships created
4. ✅ 16 DAX measures added

---

## Dashboard Creation Steps

### Dashboard 1: Overview (KPI Cards) - 5 minutes

**Step 1.1:** Create new page named "Overview"
**Step 1.2:** Add 4 Card visuals
- Card 1: Total Jobs
- Card 2: Total Companies
- Card 3: Total Locations
- Card 4: Total Skills

**Step 1.3:** Format cards with colors
- Total Jobs: Blue (#0078D4)
- Total Companies: Green (#107C10)
- Total Locations: Yellow (#FFB900)
- Total Skills: Red (#C50F1F)

---

### Dashboard 2: Job Categories (Charts) - 10 minutes

**Step 2.1:** Create new page named "Job Categories"
**Step 2.2:** Add Column Chart (Left side)
- X-Axis: job_category
- Y-Axis: Total Jobs
- Sort: Descending

**Step 2.3:** Add Pie Chart (Right side)
- Legend: job_category
- Values: Total Jobs
- Show data labels

**Step 2.4:** Add Table (Bottom)
- Columns: job_category, Total Jobs, and category counts

---

### Dashboard 3: Skills Analysis (Top 20) - 10 minutes

**Step 3.1:** Create new page named "Skills Analysis"
**Step 3.2:** Add Bar Chart (Main)
- X-Axis: skill_name
- Y-Axis: Count of job skills
- Limit: Top 20
- Sort: Descending

**Step 3.3:** Add KPI card
- Measure: Skills per Job

**Step 3.4:** Add Table (Bottom)
- Columns: skill_name, skill_category, demand count

---

### Dashboard 4: Geographic (Maps) - 15 minutes

**Step 4.1:** Create new page named "Geographic"
**Step 4.2:** Add Map Visual (Top Left)
- Location: city
- Size: Total Jobs
- Color: % Remote Jobs

**Step 4.3:** Add Column Chart (Top Right)
- X-Axis: city
- Y-Axis: Total Jobs
- Limit: Top 10

**Step 4.4:** Add Table (Bottom)
- Columns: city, country, Total Jobs, % Remote Jobs

---

### Dashboard 5: Companies (Top Hiring) - 15 minutes

**Step 5.1:** Create new page named "Companies"
**Step 5.2:** Add Bar Chart (Left)
- X-Axis: company_name
- Y-Axis: Total Jobs
- Limit: Top 15

**Step 5.3:** Add Scatter Chart (Right)
- X-Axis: company_name
- Y-Axis: Total Jobs
- Size: Skills per Job

**Step 5.4:** Add Table (Bottom)
- Columns: company_name, Total Jobs, avg description length

---

### Dashboard 6: Trends (Time Series) - 15 minutes

**Step 6.1:** Create new page named "Trends"
**Step 6.2:** Add Line Chart (Top Left)
- X-Axis: date
- Y-Axis: Total Jobs

**Step 6.3:** Add Area Chart (Top Right)
- X-Axis: month
- Y-Axis: Total Jobs

**Step 6.4:** Add Matrix (Bottom)
- Rows: year
- Columns: month
- Values: Total Jobs
- Enable conditional formatting

---

## Total Time Estimate

- Dashboard 1: 5 min
- Dashboard 2: 10 min
- Dashboard 3: 10 min
- Dashboard 4: 15 min
- Dashboard 5: 15 min
- Dashboard 6: 15 min
- **Total: ~70 minutes (1.5 hours)**

---

## Formatting Tips

### Colors
- Primary: #0078D4 (Blue)
- Secondary: #107C10 (Green)
- Accent: #FFB900 (Yellow)
- Alert: #C50F1F (Red)

### Font Sizes
- Page titles: 20pt
- Card titles: 16pt
- Axis labels: 12pt
- Data labels: 11pt

### Best Practices
- Consistent color scheme
- Clear titles and descriptions
- Add slicers for filtering
- Use conditional formatting on tables
- Enable drill-through where applicable

---

## Save & Publish

1. **Save locally**: File → Save → `JOB_INTELLIGENT.pbix`
2. **Publish to Power BI Service** (optional):
   - Publish → Select workspace → Create dashboard

---

Done! 🎉

"""
        
        return guide
    
    # ==========================================
    # MAIN EXECUTION
    # ==========================================
    
    def build(self):
        """Exécuter le build"""
        print("\n" + "="*70)
        print("🎨 POWER BI DASHBOARD BUILDER")
        print("="*70 + "\n")
        
        try:
            # Step 1: Define dashboards
            self.log_action("📋 STEP 1: DEFINING DASHBOARDS\n", "")
            dashboards = self.define_all_dashboards()
            self.log_action(f"\n✓ Defined {len(dashboards)} dashboards\n")
            
            # Step 2: Generate Power BI script
            self.log_action("📝 STEP 2: GENERATING POWER BI SCRIPT\n", "")
            script = self.generate_powerbi_import_script(dashboards)
            
            # Step 3: Generate specifications
            self.log_action("📊 STEP 3: GENERATING SPECIFICATIONS\n", "")
            specs = self.generate_dashboard_specifications(dashboards)
            
            # Step 4: Generate guide
            self.log_action("📖 STEP 4: GENERATING STEP-BY-STEP GUIDE\n", "")
            guide = self.generate_step_by_step_guide(dashboards)
            
            # Step 5: Save files
            self.log_action("💾 STEP 5: SAVING FILES\n", "")
            
            # Save script
            script_file = self.output_dir / "powerbi_dashboards_script.m"
            with open(script_file, 'w', encoding='utf-8') as f:
                f.write(script)
            self.log_action(f"  ✓ {script_file.name}")
            
            # Save specs
            specs_file = self.output_dir / "DASHBOARD_SPECIFICATIONS.md"
            with open(specs_file, 'w', encoding='utf-8') as f:
                f.write(specs)
            self.log_action(f"  ✓ {specs_file.name}")
            
            # Save guide
            guide_file = self.output_dir / "DASHBOARD_CREATION_GUIDE.md"
            with open(guide_file, 'w', encoding='utf-8') as f:
                f.write(guide)
            self.log_action(f"  ✓ {guide_file.name}")
            
            # Save dashboard definitions as JSON
            config_file = self.output_dir / "dashboards_config.json"
            with open(config_file, 'w', encoding='utf-8') as f:
                json.dump(dashboards, f, indent=2, ensure_ascii=False, default=str)
            self.log_action(f"  ✓ {config_file.name}")
            
            # Summary
            print("\n" + "="*70)
            print("✅ DASHBOARD BUILDER COMPLETE!")
            print("="*70)
            print(f"\n📊 Summary:")
            print(f"   ✓ Dashboards defined: {len(dashboards)}")
            total_visuals = sum(len(d['visuals']) for d in dashboards.values())
            print(f"   ✓ Visuals specified: {total_visuals}")
            print(f"   ✓ Measures required: 16")
            print(f"\n📁 Generated Files:")
            print(f"   1. DASHBOARD_CREATION_GUIDE.md (step-by-step)")
            print(f"   2. DASHBOARD_SPECIFICATIONS.md (detailed specs)")
            print(f"   3. powerbi_dashboards_script.m (Power Query)")
            print(f"   4. dashboards_config.json (full config)")
            print(f"\n⏱️  Estimated Creation Time: ~1.5 hours")
            print(f"\n👉 Next: Follow DASHBOARD_CREATION_GUIDE.md")
            print("="*70 + "\n")
            
        except Exception as e:
            self.log_action(f"ERROR: {str(e)}", "✗")


if __name__ == "__main__":
    builder = DashboardBuilder()
    builder.build()
