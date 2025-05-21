#!/usr/bin/env python3
"""Main script to run the solar data analysis for all countries."""
import os
import sys
import json
import pandas as pd
from datetime import datetime
from pathlib import Path
import numpy as np

# Add project root to path
project_root = str(Path(__file__).parent.parent)
if project_root not in sys.path:
    sys.path.append(project_root)

from src.data.loader import load_solar_data, process_solar_data
from src.data.analyzer import analyze_solar_data, generate_plots

class NpEncoder(json.JSONEncoder):
    """Custom JSON encoder for NumPy data types"""
    def default(self, obj):
        if isinstance(obj, (np.integer, np.int64, np.int32, np.int16, np.int8)):
            return int(obj)
        elif isinstance(obj, (np.floating, np.float64, np.float32, np.float16)):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, (np.datetime64, pd.Timestamp)):
            return obj.isoformat()
        return super().default(obj)

# Configuration
COUNTRIES = ['benin', 'sierraleone', 'togo']
REPORTS_DIR = os.path.join(project_root, 'reports')
FIGURES_DIR = os.path.join(REPORTS_DIR, 'figures')


def ensure_directories():
    """Ensure all required directories exist."""
    os.makedirs(REPORTS_DIR, exist_ok=True)
    os.makedirs(FIGURES_DIR, exist_ok=True)


def analyze_country(country: str) -> dict:
    """Run analysis for a single country.
    
    Args:
        country: Name of the country to analyze
        
    Returns:
        Dictionary containing analysis results and metadata
    """
    print(f"\nAnalyzing data for {country.title()}...")
    
    # Load and process data
    try:
        df = load_solar_data(country)
        df_clean, metadata = process_solar_data(df, country)
        
        # Perform analysis
        analysis = analyze_solar_data(df_clean, country)
        plots = generate_plots(df_clean, country, FIGURES_DIR)
        
        return {
            'country': country,
            'status': 'success',
            'metadata': metadata,
            'analysis': analysis,
            'plots': plots,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
    except Exception as e:
        print(f"Error analyzing {country}: {str(e)}")
        return {
            'country': country,
            'status': 'error',
            'error': str(e),
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }


def generate_markdown_report(results: list, output_file: str):
    """Generate a markdown report from the analysis results.
    
    Args:
        results: List of analysis results for each country
        output_file: Path to save the markdown report
    """
    with open(output_file, 'w', encoding='utf-8') as f:
        # Header
        f.write("# Solar Energy Analysis Report\n\n")
        f.write(f"*Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M')}*\n\n")
        
        # Table of Contents
        f.write("## Table of Contents\n")
        f.write("- [Summary](#summary)\n")
        for country in COUNTRIES:
            f.write(f"- [{country.title()} Analysis](#{country.lower()}-analysis)\n")
        f.write("\n")
        
        # Summary Section
        f.write("## Summary\n\n")
        f.write("### Key Findings by Country\n\n")
        f.write("| Country | Mean GHI (W/m²) | Max GHI (W/m²) | Solar Hours | Status |\n")
        f.write("|---------|----------------|----------------|-------------|--------|\n")
        
        for result in results:
            if result['status'] == 'success':
                ghi = result['analysis'].get('solar_potential', {})
                f.write(f"| {result['country'].title()} | {ghi.get('mean_ghi', 'N/A')} | {ghi.get('max_ghi', 'N/A')} | {ghi.get('solar_hours', 'N/A')} | ✅ Success |\n")
            else:
                f.write(f"| {result['country'].title()} | N/A | N/A | N/A | ❌ Error |\n")
        
        # Individual Country Sections
        for result in results:
            if result['status'] != 'success':
                continue
                
            country = result['country']
            analysis = result['analysis']
            
            f.write(f"\n## {country.title()} Analysis\n\n")
            
            # Add figures if available
            if result.get('plots'):
                plots = result['plots']
                if 'ghi_timeseries' in plots:
                    rel_path = os.path.relpath(plots['ghi_timeseries'], os.path.dirname(output_file))
                    f.write(f"![GHI Time Series]({rel_path})\n\n")
                
                if 'daily_profile' in plots:
                    rel_path = os.path.relpath(plots['daily_profile'], os.path.dirname(output_file))
                    f.write(f"![Daily Profile]({rel_path})\n\n")
            
            # Add key metrics
            f.write("### Key Metrics\n\n")
            f.write("| Metric | Value |\n")
            f.write("|--------|-------|\n")
            
            solar_pot = analysis.get('solar_potential', {})
            for metric, value in solar_pot.items():
                f.write(f"| {metric.replace('_', ' ').title()} | {value} |\n")
            
            # Add top correlations
            corr = analysis.get('correlation_analysis', {}).get('top_correlations', {})
            if corr:
                f.write("\n### Top Correlations with GHI\n\n")
                f.write("| Variable | Correlation |\n")
                f.write("|----------|-------------|\n")
                for var, val in corr.items():
                    f.write(f"| {var} | {val:.3f} |\n")


def main():
    """Main execution function."""
    print("Starting solar data analysis...")
    ensure_directories()
    
    # Run analysis for all countries
    results = []
    for country in COUNTRIES:
        result = analyze_country(country)
        results.append(result)
    
    # Save raw results
    results_file = os.path.join(REPORTS_DIR, 'analysis_results.json')
    try:
        with open(results_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, cls=NpEncoder, ensure_ascii=False)
        print(f"\nAnalysis complete! Report saved to: {results_file}")
    except Exception as e:
        print(f"\nError saving results: {str(e)}")
        print("Partial results will be printed to console:")
        print(json.dumps(results, indent=2, default=str, ensure_ascii=False))
    
    # Generate markdown report
    report_file = os.path.join(REPORTS_DIR, 'solar_analysis_report.md')
    generate_markdown_report(results, report_file)
    print(f"Raw results saved to: {report_file}")


if __name__ == "__main__":
    main()
