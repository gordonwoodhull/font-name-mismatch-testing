#! /usr/bin/env python3

import csv

import csv
import sys

def compare_csv_values(file_path, output_file_path=None, ambiguous_file_path=None):
    """
    Read a two-column CSV file and compare values without case sensitivity.

    Args:
        file_path (str): Path to the CSV file
        output_file_path (str, optional): Path to write unmatching rows
        ambiguous_file_path (str, optional): Path to write ambiguous entries
    """
    unmatching_rows = []
    # Dictionary to track prefixes and their matching strings
    prefix_matches = {}
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
                print(f"Row {row_num}: Possibly ambiguous - '{row[1]}' is a prefix of '{row[0]}'")
                # Store the prefix and the matching string
                if value2 not in prefix_matches:
                    prefix_matches[value2] = []
                # Add the original string (not lowercase) to the matches
                prefix_matches[value2].append(row[0])
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

    # Filter and write ambiguous entries (prefixes with multiple matches)
    ambiguous_entries = []
    for prefix, matches in prefix_matches.items():
        if len(matches) > 1:
            # First column is the prefix, followed by all matching strings
            ambiguous_entries.append([prefix] + matches)

    if ambiguous_file_path and ambiguous_entries:
        try:
            with open(ambiguous_file_path, 'w', newline='') as ambiguous_file:
                csv_writer = csv.writer(ambiguous_file)
                csv_writer.writerows(ambiguous_entries)
            print(f"Wrote {len(ambiguous_entries)} ambiguous entries to '{ambiguous_file_path}'")
        except Exception as e:
            print(f"Error writing to ambiguous entries file: {e}")

if __name__ == "__main__":
    # Check if required command line arguments were provided
    if len(sys.argv) < 2:
        print("Usage: python script_name.py <input_csv_file> [output_csv_file] [ambiguous_entries_file]")
        print("Example: python compare_csv.py data.csv matches.csv ambiguous.csv")
        sys.exit(1)

    # Get the input CSV file path from command line arguments
    input_csv_path = sys.argv[1]

    # Get the output CSV file path if provided
    output_csv_path = None
    if len(sys.argv) >= 3:
        output_csv_path = sys.argv[2]

    # Get the ambiguous entries file path if provided
    ambiguous_file_path = None
    if len(sys.argv) >= 4:
        ambiguous_file_path = sys.argv[3]

    try:
        compare_csv_values(input_csv_path, output_csv_path, ambiguous_file_path)
    except FileNotFoundError:
        print(f"Error: File '{input_csv_path}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
