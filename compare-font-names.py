#! /usr/bin/env python3

import csv

import csv
import sys

def compare_csv_values(file_path, output_file_path=None):
    """
    Read a two-column CSV file and compare values without case sensitivity.
    
    Args:
        file_path (str): Path to the CSV file
    """
    unmatching_rows = []
    with open(file_path, 'r', newline='') as csvfile:
        csv_reader = csv.reader(csvfile)
        
        # Skip header row if it exists (uncomment if needed)
        # next(csv_reader)
        
        for row_num, row in enumerate(csv_reader, 1):
            # Check if the row has exactly two columns
            if len(row) != 2:
                print(f"Row {row_num} does not have exactly two columns. Skipping.")
                continue
            
            # Extract the two values and convert to lowercase for case-insensitive comparison
            value1, value2 = row[0].lower(), row[1].lower()
            
            # Compare the values
            if value1 == value2:
                print(f"Row {row_num}: Values match - '{row[0]}' and '{row[1]}' are identical (ignoring case)")
            if value1.startswith(value2):
                print(f"Row {row_num}: False positive - '{row[1]}' is a prefix of '{row[0]}'")
            else:
                unmatching_rows.append(row)
    if output_file_path and unmatching_rows:
        try:
            with open(output_file_path, 'w', newline='') as outfile:
                csv_writer = csv.writer(outfile)
                csv_writer.writerows(unmatching_rows)
            print(f"\nWrote {len(unmatching_rows)} true positive rows to '{output_file_path}'")
        except Exception as e:
            print(f"Error writing to output file: {e}")

if __name__ == "__main__":
    # Check if required command line arguments were provided
    if len(sys.argv) < 2:
        print("Usage: python script_name.py <input_csv_file> [output_csv_file]")
        print("Example: python compare_csv.py data.csv matches.csv")
        sys.exit(1)
    
    # Get the input CSV file path from command line arguments
    input_csv_path = sys.argv[1]
    
    # Get the output CSV file path if provided
    output_csv_path = None
    if len(sys.argv) >= 3:
        output_csv_path = sys.argv[2]
    
    try:
        compare_csv_values(input_csv_path, output_csv_path)
    except FileNotFoundError:
        print(f"Error: File '{input_csv_path}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
