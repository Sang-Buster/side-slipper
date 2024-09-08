import pandas as pd
from datetime import datetime, timedelta
import pytz
import logging


def clean_and_convert_gps_time(input_file, output_file, encoding="utf-8"):
    # Step 1: Read the CSV file with the specified encoding
    df = pd.read_csv(input_file, encoding=encoding)

    # Remove the row where Index == 0
    df = df[df["Index"] != 0]

    # Drop the Index column
    df.drop(columns=["Index"], inplace=True)

    # Step 2: Convert GPS time to a standard datetime format
    def gps_time_to_est(gps_time):
        if isinstance(gps_time, str):
            try:
                week_number, tow = map(float, gps_time.split(":"))
                gps_epoch = datetime(1980, 1, 6, tzinfo=pytz.utc)
                gps_time_utc = gps_epoch + timedelta(weeks=week_number, seconds=tow)
                gps_time_utc -= timedelta(seconds=18)  # Adjust for leap seconds
                est = pytz.timezone("US/Eastern")
                est_time = gps_time_utc.astimezone(est)  # Convert to EST/EDT
                return est_time
            except ValueError as e:
                logging.error(f"Error converting GPS time '{gps_time}': {e}")

    df["GPS time"] = df["GPS time"].astype(str).apply(gps_time_to_est)

    # Convert GPS time to YMDHHMMSS format
    df["GPS time"] = df["GPS time"].dt.strftime("%Y%m%d%H%M%S")

    # Step 3: Save the cleaned DataFrame to a file
    df.to_csv(output_file, index=False)


clean_and_convert_gps_time("src/data/base_09_04_24.csv", "src/data/base_cleaned.csv")
clean_and_convert_gps_time("src/data/rover_09_04_24.csv", "src/data/rover_cleaned.csv")


def full_join_and_mutate(file1, file2, output_file):
    # Read the cleaned CSV files
    df1 = pd.read_csv(file1)  # Base cleaned
    df2 = pd.read_csv(file2)  # Rover cleaned

    # Perform a right join with suffixes to distinguish columns
    merged_df = pd.merge(
        df1, df2, on="GPS time", how="right", suffixes=("_base", "_rover")
    )

    # Fill missing values with 0 for base columns
    merged_df.fillna(0, inplace=True)

    # Create the beta column using relPosHeading from rover and CoG from base
    merged_df["beta"] = merged_df["relPosHeading"] - merged_df["CoG_base"]

    # Save the result to a new CSV file
    merged_df.to_csv(output_file, index=False)


# Call the function with the appropriate file paths
full_join_and_mutate(
    "src/data/base_cleaned.csv",
    "src/data/rover_cleaned.csv",
    "src/data/merged_cleaned.csv",
)
