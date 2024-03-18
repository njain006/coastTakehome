import pandas as pd
import json
from datetime import datetime, timedelta

# Function to parse timestamp from string for data saved in CSV
def parse_timestamp(timestamp_str):
    return datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")

# Function to parse the timestamp from JSON
def parse_timestamp_json(timestamp_str):
    timestamp_data = json.loads(timestamp_str)
    date_str = timestamp_data["date_local"]
    seconds_since_day_start = int(timestamp_data["seconds_since_day_start_local"])
    time_delta = timedelta(seconds=seconds_since_day_start)
    date_time = datetime.strptime(date_str, "%m/%d/%Y") + time_delta
    return date_time

# Function to calculate time difference in hours between two timestamps
def time_diff_hours(timestamp1, timestamp2):
    return abs((timestamp2 - timestamp1).total_seconds() / 3600)

# Function to identify suspicious badge swipes less than 6 hours apart
def identify_suspicious_swipes(data):
    suspicious_swipes = []
    data.sort_values(by='timestamp_local', inplace=True)  # Sort data by timestamp
    for i in range(len(data) - 1):
        current_row = data.iloc[i]
        next_row = data.iloc[i + 1]
        if current_row['badge_id'] == next_row['badge_id']:  # Same badge ID
            time_diff = time_diff_hours(current_row['timestamp_local'], next_row['timestamp_local'])
            if time_diff < 6:  # Less than 6 hours apart
                suspicious_swipes.append((next_row['timestamp_local'], next_row['location'], next_row['badge_id']))
    return suspicious_swipes

# Function to identify badges that have not been swiped for more than 24 hours
def identify_missing_swipes(data):
    missing_swipes = []
    data.sort_values(by='timestamp_local', inplace=True)  # Sort data by timestamp
    for badge_id, group in data.groupby('badge_id'):
        min_timestamp = group['timestamp_local'].min()
        max_timestamp = group['timestamp_local'].max()
        if (max_timestamp - min_timestamp).total_seconds() > 24 * 3600:  # More than 24 hours
            missing_swipes.append((badge_id, max_timestamp))
    return missing_swipes

# Function to identify entries without corresponding exits
def identify_missing_exits(data):
    missing_exits = []
    data.sort_values(by=['badge_id', 'timestamp_local'], inplace=True)  # Sort data by badge ID and timestamp
    for badge_id, group in data.groupby('badge_id'):
        entries = group.index[group['event'] == 'entry']
        exits = group.index[group['event'] == 'exit']
        last_exit = None
        
        for entry_idx in entries:
            if last_exit is None:
                continue
            # Check if there are no exits between the current entry and the last exit
            if not any(exit_idx > last_exit and exit_idx < entry_idx for exit_idx in exits):
                missing_exits.append(badge_id)
            last_exit = entry_idx
    return missing_exits

# Read CSV data
def read_csv_data(file):
    data = pd.read_csv(file)
    data['timestamp_local'] = data['timestamp_local'].apply(parse_timestamp)
    return data

# Read JSON data
def read_json_data(file):
    with open(file, 'r') as f:
        data = json.load(f)
    df = pd.DataFrame(data)
    df['timestamp_local'] = df['timestamp_local'].apply(parse_timestamp_json)
    return df

# Main function
def main():
    csv_file = '20231130155612-ny.csv'  # Example CSV file name, replace with actual file name
    json_file = '20231130155612-ca.json'  # Example JSON file name, replace with actual file name

    # Process CSV data
    csv_data = read_csv_data(csv_file)
    csv_suspicious_swipes = identify_suspicious_swipes(csv_data)
    csv_missing_swipes = identify_missing_swipes(csv_data)
    csv_missing_exits = identify_missing_exits(csv_data)

    # Process JSON data
    json_data = read_json_data(json_file)
    json_suspicious_swipes = identify_suspicious_swipes(json_data)
    json_missing_swipes = identify_missing_swipes(json_data)
    json_missing_exits = identify_missing_exits(json_data)

    # Print suspicious swipes
    print("Suspicious Swipes within 6 hours:")
    all_suspicious_swipes = csv_suspicious_swipes + json_suspicious_swipes
    for swipe in all_suspicious_swipes:
        print("Suspicious swipe within 6 hours at", swipe[0], "in", swipe[1], "by badge ID", swipe[2])

    # Print badges with missing swipes
    print("\nBadges with Missing Swipes (more than 24 hours):")
    all_missing_swipes = csv_missing_swipes + json_missing_swipes
    for badge_id, last_swipe_time in all_missing_swipes:
        print("Badge ID", badge_id, "has not swiped since", last_swipe_time)

    # Print badges with missing exits
    print("\nBadges with Missing Exits:")
    all_missing_exits = csv_missing_exits + json_missing_exits
    for badge_id in all_missing_exits:
        print("Badge ID", badge_id, "has missing exits")

if __name__ == "__main__":
    main()
