#!/usr/bin/env python3
"""Script to inspect the structure of the data files."""
import os
import pandas as pd
from pathlib import Path

def inspect_file(filepath):
    """Inspect a single data file and return its basic properties."""
    print(f"\nInspecting file: {filepath}")
    
    # First, check file size and encoding
    file_size = os.path.getsize(filepath) / (1024 * 1024)  # in MB
    print(f"File size: {file_size:.2f} MB")
    
    # Try to determine encoding
    encodings = ['utf-8', 'latin1', 'iso-8859-1', 'cp1252']
    detected_encoding = None
    
    for encoding in encodings:
        try:
            with open(filepath, 'r', encoding=encoding) as f:
                # Read first few lines to check encoding
                for _ in range(5):
                    line = f.readline()
                    if not line:
                        break
            detected_encoding = encoding
            print(f"Can be read with encoding: {encoding}")
            break
        except UnicodeDecodeError:
            continue
    
    if not detected_encoding:
        print("Could not determine file encoding with standard codecs")
        return
    
    # Try to read the first few lines as text
    print("\nFirst 5 lines of the file:")
    with open(filepath, 'r', encoding=detected_encoding) as f:
        for i, line in enumerate(f):
            print(f"{i+1}: {line.strip()}")
            if i >= 4:  # Only show first 5 lines
                break
    
    # Try to read with pandas
    print("\nTrying to read with pandas:")
    try:
        # First try reading without any date parsing
        df = pd.read_csv(filepath, encoding=detected_encoding, nrows=10)
        print("\nDataFrame info:")
        print(df.info())
        print("\nFirst 5 rows:")
        print(df.head())
        
        # If there's a timestamp column, try to parse it
        ts_cols = [col for col in df.columns if 'time' in col.lower() or 'date' in col.lower()]
        if ts_cols:
            print(f"\nTimestamp columns found: {ts_cols}")
            for ts_col in ts_cols:
                print(f"\nSample values from '{ts_col}':")
                print(df[ts_col].head().values)
                
                # Try to parse as datetime
                try:
                    parsed_dates = pd.to_datetime(df[ts_col], errors='coerce')
                    print("\nParsed dates:")
                    print(parsed_dates.head())
                    print(f"Number of valid dates: {parsed_dates.notna().sum()}/{len(parsed_dates)}")
                except Exception as e:
                    print(f"Error parsing dates: {e}")
    
    except Exception as e:
        print(f"Error reading with pandas: {e}")

def main():
    """Main function to inspect all data files."""
    data_dir = Path(__file__).parent.parent / 'data'
    print(f"Data directory: {data_dir}")
    
    # List all CSV files in the data directory
    csv_files = list(data_dir.glob('*.csv'))
    
    if not csv_files:
        print("No CSV files found in the data directory.")
        return
    
    print(f"Found {len(csv_files)} CSV files:")
    for i, file in enumerate(csv_files, 1):
        print(f"{i}. {file.name} ({file.stat().st_size / (1024 * 1024):.2f} MB)")
    
    # Inspect each file
    for file in csv_files:
        inspect_file(file)

if __name__ == "__main__":
    main()
