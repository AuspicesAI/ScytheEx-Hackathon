import os
import redis
import pandas as pd
import pickle
from sklearn.preprocessing import LabelEncoder
import json

train = pd.read_csv("data/training.csv")
test = pd.read_csv("data/testing.csv")
combined_df = pd.concat([train, test], ignore_index=True)
df = combined_df.sample(frac=1).reset_index(drop=True)

proto_encoder = LabelEncoder()
service_encoder = LabelEncoder()
state_encoder = LabelEncoder()
attack_cat_encoder = LabelEncoder()
attack_cat_decoder = LabelEncoder()
with open("models/16_XGBoost_model.pkl", "rb") as model_file:
    model = pickle.load(model_file)


protocol_encoder = LabelEncoder()
flags_encoder = LabelEncoder()
label_encoder = LabelEncoder()

protocol_decoder = protocol_encoder.inverse_transform
flags_decoder = flags_encoder.inverse_transform
label_decoder = label_encoder.inverse_transform

with open("models/Neris_XGBoost_model.pkl", "rb") as model_file:
    model = pickle.load(model_file)


# Setup Redis connection
r = redis.Redis(host="5.tcp.eu.ngrok.io", port=16200, db=0)

# Subscribe to the channelcd ai
pubsub = r.pubsub()
pubsub.subscribe("processed_data_channel")

print("Subscribed to 'processed_data_channel'. Waiting for data...")



def upload_to_redis(df, status):
    redis_host = "localhost"
    redis_port = 6380
    redis_db = 0

    # Add the array as a new column to the DataFrame
    df["packet_status"] = status

    # Convert DataFrame to JSON for publishing
    df_json = df.to_json(orient="records")

    # Create a Redis connection
    r = redis.Redis(host=redis_host, port=redis_port, db=redis_db)

    # Define the channel
    channel = "prediction_channel"

    # Publish DataFrame to the Redis channel
    r.publish(channel, df_json)

    print(f"Published updated DataFrame to Redis on channel '{channel}'.")


def prepare_df(raw_data):
    input_df = input_df.astype(
        {
            "Duration": "float64",
            "Packets": "int64",
            "Bytes": "int64",
            "Flows": "int64",
            "Source Port": "int64",
            "Destination Port": "int64",
            "Bytes per Packet": "float64",
            "Packets per Second": "float64",
            "Bytes per Second": "float64",
            "Is Encrypted Traffic": "int64",
            "Common Port Usage": "int64",
        }
    )
    titles = [
        "Duration",
        "Protocol",
        "Flags",
        "Packets",
        "Bytes",
        "Flows",
        "Label",
        "Source Port",
        "Destination Port",
        "Bytes per Packet",
        "Packets per Second",
        "Bytes per Second",
        "Is Encrypted Traffic",
        "Common Port Usage",
    ]
    df = pd.DataFrame(raw_data)
    df = df[titles]

    df["Duration"] = df["Duration"].replace(0.000, 0.001)
    df["Bytes per Packet"] = df.apply(
        lambda row: row["Bytes"] / row["Packets"] if row["Packets"] > 0 else 0, axis=1
    )
    # Calculate 'Packets per Second' and 'Bytes per Second' if duration is not zero
    df["Packets per Second"] = df.apply(
        lambda row: row["Packets"] / row["Duration"] if row["Duration"] > 0 else 0,
        axis=1,
    )
    df["Bytes per Second"] = df.apply(
        lambda row: row["Bytes"] / row["Duration"] if row["Duration"] > 0 else 0, axis=1
    )

    def clean_port(port):
        try:
            # Attempt to convert port to integer
            return int(port)
        except ValueError:
            # If conversion fails, return 0
            return 0

    df["Destination Port"] = df["Destination Port"].apply(clean_port)

    def is_encrypted_protocol(port):
        encrypted_ports = {443, 22, 993, 995, 465, 587, 636, 989, 990, 992, 1194, 500}
        return 1 if port in encrypted_ports else 0

    def is_common_port(port):
        common_ports = {80, 443, 21, 22, 25, 110, 143, 3306, 3389, 5900, 53, 23}
        return 1 if port in common_ports else 0

    df["Destination Port"] = df["Destination Port"].astype(int)
    df["Is Encrypted Traffic"] = df["Destination Port"].apply(is_encrypted_protocol)
    df["Common Port Usage"] = df["Destination Port"].apply(is_common_port)
    df.drop(["Destination IP", "Source IP"], axis=1, inplace=True)

    return df


def prepare_input(input_df):
    try:
        df["Protocol"] = protocol_encoder.transform(df["Protocol"])
    except ValueError:
        # Replace unknown labels with "RTP"
        protocol_encoder.transform("RTP")


    try:
        df["Flags"] = protocol_encoder.transform(df["Flags"])
    except ValueError:
        # Replace unknown labels with "RTP"
        protocol_encoder.transform("PAC_")
    print(input_df)

    return input_df


def predict(input_data):
    prediction = model.predict(input_data)
    return label_encoder.inverse_transform(prediction)


def main():
    for message in pubsub.listen():
        if message["type"] == "message":
            data = json.loads(message["data"])
            print("Received data:", data)
            print(data)
            df = prepare_df(data)
            input_data = prepare_input(df)
            prediction = predict(input_data)
            input_data["id"] = data["id"]
            upload_to_redis(input_data["id"], prediction)


if __name__ == "__main__":
    main()
