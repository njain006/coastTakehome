# Anomaly Detection System

This project implements an anomaly detection system for monitoring employee badge swipes across multiple locations. The system analyzes historical swipe data to identify suspicious patterns such as swipes at different locations within a short time frame, long stays, and missing swipes.

## Installation

1. Clone the repository to your local machine:

    ```
    git clone git@github.com:njain006/coastTakehome.git
    ```

2. Navigate to the project directory:

    ```
    cd anomaly-detection
    ```

3. Ensure that Python 3.x and the required libraries are installed. You can install the required libraries using pip:

    ```
    pip install -r requirements.txt
    ```

## Usage

1. Place the CSV and JSON data files containing swipe data in the project directory.

2. Update the `csv_file` and `json_file` variables in the `main` function of `anomaly_detection.py` with the names of your CSV and JSON files, respectively.

3. Run the `anomaly_detection.py` script:

    ```
    python anomaly_detection.py
    ```

4. The script will output suspicious swipes, badges with missing swipes (more than 24 hours), and any other identified anomalies.

## Assumptions

Please review the assumptions made in the implementation by referring to the "Assumptions" section in the README.md file.
 