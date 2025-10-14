#! /usr/bin/env python3

import csv

import csv
import sys

def compare_csv_values(all_fonts_csv_path, mismatched_csv_path, output_file_path=None, ambiguous_file_path=None):
    """
    Compare font names for ambiguity using all_fonts_csv as a baseline for comparisons.

    Args:
        all_fonts_csv_path (str): Path to CSV file with all font names (one column)
        mismatched_csv_path (str): Path to the two-column CSV file with potentially mismatched font names
        output_file_path (str, optional): Path to write unmatching rows
        ambiguous_file_path (str, optional): Path to write ambiguous entries
    """
    unmatching_rows = []
    # Dictionary to track prefixes and their matching strings
    prefix_matches = {}

    # First, load all font names from all_fonts_csv and prime prefix_matches
    try:
        with open(all_fonts_csv_path, 'r', newline='') as all_fonts_file:
            all_fonts_reader = csv.reader(all_fonts_file)
            for row in all_fonts_reader:
                if len(row) >= 1:
                    font_name = row[0]
                    font_name_lower = font_name.lower()
                    if font_name_lower not in prefix_matches:
                        prefix_matches[font_name_lower] = []
                    prefix_matches[font_name_lower].append(font_name)
        print(f"Loaded {len(prefix_matches)} font names from '{all_fonts_csv_path}'")
    except Exception as e:
        print(f"Error loading all fonts CSV: {e}")
        raise

    # Now process the mismatched CSV file
    with open(mismatched_csv_path, 'r', newline='') as csvfile:
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
            else:
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
            # First match is from all_fonts_csv, followed by all ambiguous font family names
            ambiguous_entries.append(matches)

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
    if len(sys.argv) < 3:
        print("Usage: python compare-font-names.py <all_fonts_csv> <mismatched_csv> [output_csv_file] [ambiguous_entries_file]")
        print("Example: python compare-font-names.py all_fonts.csv mismatched_data.csv matches.csv ambiguous.csv")
        sys.exit(1)

    # Get the input CSV file paths from command line arguments
    all_fonts_csv_path = sys.argv[1]
    mismatched_csv_path = sys.argv[2]

    # Get the output CSV file path if provided
    output_csv_path = None
    if len(sys.argv) >= 4:
        output_csv_path = sys.argv[3]

    # Get the ambiguous entries file path if provided
    ambiguous_file_path = None
    if len(sys.argv) >= 5:
        ambiguous_file_path = sys.argv[4]

    try:
        compare_csv_values(all_fonts_csv_path, mismatched_csv_path, output_csv_path, ambiguous_file_path)
    except FileNotFoundError as e:
        print(f"Error: File not found. {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
