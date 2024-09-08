# Copyright (c) 2024 AuspicesAI
#
# This file is part of ScytheEx.
#
# ScytheEx is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3.0 as
# published by the Free Software Foundation.
#
# ScytheEx is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with ScytheEx. If not, see <https://www.gnu.org/licenses/>.

import os
import redis
import pandas as pd
import pickle
from sklearn.preprocessing import LabelEncoder
import json
import time
from sklearn.preprocessing import StandardScaler


"""
The following script performs the following operations:
1. Loads pkl files for model input and feature scaling.
2. Loads a pre-trained logistic regression model from a pickle file.
3. Creates LabelEncoder objects to encode and decode categorical variables for 'Protocol', 'Flags', and 'Label' columns.
"""

# Load the pre-trained logistic regression model
with open("models/Neris_LogReg_model.pkl", "rb") as model_file:
    model = pickle.load(model_file)



# Initialize scaler and encoders for data transformation
with open("variables/Neris/scaler.pkl", "rb") as scaler_file:
    scaler = pickle.load(scaler_file)

with open("variables/Neris/Protocol_Encoder.pkl", "rb") as protocol_encoder_file:
    protocol_encoder = pickle.load(protocol_encoder_file)

with open("variables/Neris/Flags_Encoder.pkl", "rb") as flags_encoder_file:
    flags_encoder = pickle.load(flags_encoder_file)

with open("variables/Neris/Label_Encoder.pkl", "rb") as label_encoder_file:
    label_encoder = pickle.load(label_encoder_file)

# Fit and transform the categorical features using encoders
protocol_decoder = protocol_encoder.inverse_transform
flags_decoder = flags_encoder.inverse_transform
label_decoder = label_encoder.inverse_transform

"""
This script connects to a Redis server and subscribes to a specific channel to receive packet data:
1. Establishes a connection to a Redis server using specified host, port, and database index.
2. Subscribes to the 'packet_data' channel to listen for incoming messages.
3. Prints a confirmation message indicating successful subscription and readiness to receive data.
"""

# Establish connection to Redis server
r = redis.Redis(host="100.26.220.36", port=6379, db=0)

# Subscribe to the 'packet_data' channel
pubsub = r.pubsub()
pubsub.subscribe("packet_data")

# Notify user of subscription status
print("Subscribed to 'packet_data'. Waiting for data...")


def upload_to_redis(df, status):
    """
    This function uploads a modified DataFrame to a Redis channel as a JSON string:
    1. Adds a new column 'Status' to the DataFrame based on the provided status.
    2. Filters the DataFrame to specific columns relevant for further processing.
    3. Converts the filtered DataFrame to a JSON format.
    4. Establishes a connection to the Redis server.
    5. Publishes the JSON string to a predefined Redis channel.
    6. Handles connection errors and prints relevant messages.
    """

    # Redis server configuration
    redis_host = "100.26.220.36"
    redis_port = 6380
    redis_db = 0

    # Add the 'Status' column to the DataFrame
    df["Status"] = status
    df = df[
        [
            "id",
            "Duration",
            "Protocol",
            "Source IP",
            "Source Port",
            "Destination IP",
            "Destination Port",
            "Flags",
            "Status",
        ]
    ]

    # Convert DataFrame to JSON for publishing
    df_json = df.to_json(orient="records")

    # Create a Redis connection
    r = redis.Redis(host=redis_host, port=redis_port, db=redis_db)

    # Define the Redis channel
    channel = "prediction_channel"

    try:
        # Publish DataFrame to Redis channel
        r.publish(channel, df_json)
        print(f"Published updated DataFrame to Redis on channel '{channel}'.")
    except redis.exceptions.ConnectionError as e:
        print(f"Failed to connect to Redis: {e}")


def prepare_df(raw_data):
    """
    Processes the raw data into a structured DataFrame:
    1. Cleans port numbers by attempting to convert them to integers; returns 0 for invalid conversions.
    2. Standardizes the 'Flags' column to use the first entry for all rows.
    3. Applies transformations to ports, durations, and calculates new columns:
       - Converts duration of 0.000 to 0.001 to avoid division errors.
       - Calculates 'Bytes per Packet', 'Packets per Second', and 'Bytes per Second'.
       - Identifies whether traffic is encrypted and whether common ports are used.
    4. Cleans and structures the DataFrame by selecting specific columns and setting appropriate data types.
    5. Drops unnecessary IP address columns and reformats the 'Duration' column to three decimal places.
    Returns the structured DataFrame ready for further analysis.
    """

    def clean_port(port):
        try:
            return int(port)
        except ValueError:
            return 0

    raw_data["Flags"] = raw_data["Flags"][0]
    index_values = range(len(raw_data))
    df = pd.DataFrame(raw_data, index=index_values)

    df["Destination Port"] = df["Destination Port"].apply(clean_port)
    df["Destination Port"] = df["Destination Port"].astype(int)
    df["Source Port"] = df["Source Port"].apply(clean_port)
    df["Source Port"] = df["Source Port"].astype(int)

    df["Duration"] = df["Duration"].replace(0.000, 0.001)
    df["Bytes per Packet"] = df.apply(
        lambda row: row["Bytes"] / row["Packets"] if row["Packets"] > 0 else 0, axis=1
    )
    df["Packets per Second"] = df.apply(
        lambda row: row["Packets"] / row["Duration"] if row["Duration"] > 0 else 0,
        axis=1,
    )
    df["Bytes per Second"] = df.apply(
        lambda row: row["Bytes"] / row["Duration"] if row["Duration"] > 0 else 0, axis=1
    )

    def is_encrypted_protocol(port):
        encrypted_ports = {443, 22, 993, 995, 465, 587, 636, 989, 990, 992, 1194, 500}
        return 1 if port in encrypted_ports else 0

    def is_common_port(port):
        common_ports = {80, 443, 21, 22, 25, 110, 143, 3306, 3389, 5900, 53, 23}
        return 1 if port in common_ports else 0

    df["Is Encrypted Traffic"] = df["Destination Port"].apply(is_encrypted_protocol)
    df["Common Port Usage"] = df["Destination Port"].apply(is_common_port)
    df["Duration"] = df["Duration"].apply(lambda x: "{:.3f}".format(x))
    df.drop(["Destination IP", "Source IP"], axis=1, inplace=True)
    df = df.astype(
        {
            "Bytes": "float64",
            "Destination Port": "int64",
            "Bytes per Packet": "float64",
            "Packets per Second": "float64",
            "Bytes per Second": "float64",
            "Is Encrypted Traffic": "int64",
            "Common Port Usage": "int64",
        }
    )
    titles = [
        "Protocol",
        "Flags",
        "Bytes",
        "Destination Port",
        "Bytes per Packet",
        "Packets per Second",
        "Bytes per Second",
        "Is Encrypted Traffic",
        "Common Port Usage",
    ]
    df = df[titles]
    return df


def prepare_input(df):
    """
    Transforms categorical features 'Protocol' and 'Flags' in the DataFrame using pre-fitted encoders:
    1. Attempts to transform the 'Protocol' column using a pre-fitted LabelEncoder. If the encoder encounters
       an unknown label, it replaces those unknown labels with 'RTP' and retries the transformation.
    2. Similarly, attempts to transform the 'Flags' column. If unknown labels are found, replaces them
       with 'PAC_' before retrying the transformation.
    Returns the modified DataFrame with encoded categorical features.
    """

    try:
        # Transform 'Protocol' with pre-fitted encoder; handle unknown labels
        df["Protocol"] = protocol_encoder.transform(df["Protocol"])
    except ValueError:
        # Replace unknown labels with "RTP"
        unknown_protocol_labels = ~df["Protocol"].isin(protocol_encoder.classes_)
        df.loc[unknown_protocol_labels, "Protocol"] = "RTP"
        df["Protocol"] = protocol_encoder.transform(df["Protocol"])

    try:
        # Transform 'Flags' with pre-fitted encoder; handle unknown labels
        df["Flags"] = flags_encoder.transform(df["Flags"])
    except ValueError:
        # Replace unknown labels with "PAC_"
        unknown_flags_labels = ~df["Flags"].isin(flags_encoder.classes_)
        df.loc[unknown_flags_labels, "Flags"] = "PAC_"
        df["Flags"] = flags_encoder.transform(df["Flags"])

    return df


def predict(input_data):
    """
    Predicts the class labels for given input data:
    1. Scales the input data using a pre-fitted scaler to match the scale used during model training.
    2. Makes predictions using a pre-trained model.
    3. Transforms the predicted labels back to their original categorical form using a pre-fitted label encoder.
    Returns the decoded predictions as the original categorical labels.
    """

    # Scale the input data to match training data scale
    scaled_input_data = scaler.transform(input_data)

    # Make predictions using the pre-trained model
    prediction = model.predict(scaled_input_data)

    # Decode the predictions to original labels
    return label_encoder.inverse_transform(prediction)


def check_blacklist(data):
    blacklist = ["192.168.0.1"]

    if data["Source IP"] or data["Destination IP"] in blacklist:
        return True
    else:
        return False


def main():
    """
    Main execution function that listens for incoming data on a Redis subscription,
    processes the data, makes predictions, and uploads results back to Redis:
    1. Listens continuously for new messages on a Redis subscription.
    2. For each new message, it loads the data into a DataFrame, preprocesses it, and prepares it for prediction.
    3. Displays a notification for a new prediction attempt.
    4. Converts the incoming data into a format suitable for the prediction model.
    5. Uses the `predict` function to obtain predictions for the prepared data.
    6. Converts the original message data into a DataFrame to be uploaded along with the prediction.
    7. Uploads the original data and its prediction back to Redis.
    8. Prints the prediction result.
    """

    # Listen for messages on the Redis subscription
    for message in pubsub.listen():
        if message["type"] == "message":
            # Deserialize the incoming JSON data
            data = json.loads(message["data"])

            # Prepare and clean the data
            df = prepare_df(data)
            input_data = prepare_input(pd.DataFrame(df.iloc[[0]]))

            # Notify about the new prediction attempt
            print("\n\n########## New Prediction ##########")
            print(input_data)

            if check_blacklist(input_data):
                continue
            else:
                # Predict using the prepared data
                prediction = predict(input_data)

                # Create the DataFrame for uploading
                data = pd.DataFrame(data, [0])

                # Upload the results back to Redis
                upload_to_redis(data.copy(), prediction)

                # Print the prediction outcome
                print(f"{prediction[0]}")


if __name__ == "__main__":
    main()
