import os
import redis
import pandas as pd
import pickle
from sklearn.preprocessing import LabelEncoder
import json
import time
from sklearn.preprocessing import StandardScaler


# Load the data
# Since your data appears to be tab-separated, we use sep='\s+' which handles multiple spaces
df = pd.read_csv("data/LogRegNeris.csv")
dfs = pd.read_csv("data/EncoderNeris.csv")
dfs.drop(["Label", "Unnamed: 0"], axis=1, inplace=True)

with open("models/Neris_LogReg_model.pkl", "rb") as model_file:
    model = pickle.load(model_file)

scaler = StandardScaler()
scaler.fit(dfs)
protocol_encoder = LabelEncoder()
flags_encoder = LabelEncoder()
label_encoder = LabelEncoder()

protocol_encoder.fit_transform(df["Protocol"])
flags_encoder.fit_transform(df["Flags"])
label_encoder.fit_transform(df["Label"])
protocol_decoder = protocol_encoder.inverse_transform
flags_decoder = flags_encoder.inverse_transform
label_decoder = label_encoder.inverse_transform

print(
    list(zip(label_encoder.classes_, label_encoder.transform(label_encoder.classes_)))
)


with open("models/Neris_LogReg_model.pkl", "rb") as model_file:
    model = pickle.load(model_file)


# Setup Redis connection
<<<<<<< HEAD
r = redis.Redis(host="2.tcp.eu.ngrok.io", port=16468, db=0)
=======
r = redis.Redis(host="7.tcp.eu.ngrok.io", port=13716, db=0)
>>>>>>> 39e4a84a79c07a7dfd5458e9043564ec8eef750b

# Subscribe to the channelcd ai
pubsub = r.pubsub()
pubsub.subscribe("packet_data")

print("Subscribed to 'packet_data'. Waiting for data...")


def upload_to_redis(df, status):
    redis_host = "2.tcp.eu.ngrok.io"
    redis_port = 19900
    redis_db = 0

    # Add the array as a new column to the DataFrame
    df["packet_status"] = status
    # Convert DataFrame to JSON for publishing
    df_json = df.to_json(orient="records")

    # Create a Redis connection
    r = redis.Redis(host=redis_host, port=redis_port, db=redis_db)

    print(df)

    # Define the channel
    channel = "prediction_channel"

    try:
        # Publish DataFrame to the Redis channel
        r.publish(channel, df_json)
        print(f"Published updated DataFrame to Redis on channel '{channel}'.")
    except redis.exceptions.ConnectionError as e:
        print(f"")


def prepare_df(raw_data):
    def clean_port(port):
        try:
            # Attempt to convert port to integer
            return int(port)
        except ValueError:
            # If conversion fails, return 0
            return 0

    raw_data["Flags"] = raw_data["Flags"][-1]
    df = pd.DataFrame(raw_data)

    df["Destination Port"] = df["Destination Port"].apply(clean_port)
    df["Destination Port"] = df["Destination Port"].astype(int)
    df["Source Port"] = df["Source Port"].apply(clean_port)
    df["Source Port"] = df["Source Port"].astype(int)

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
            "Duration": "float64",
            "Packets": "float64",
            "Bytes": "float64",
            "Flows": "float64",
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
        "Source Port",
        "Destination Port",
        "Bytes per Packet",
        "Packets per Second",
        "Bytes per Second",
        "Is Encrypted Traffic",
        "Common Port Usage",
    ]
    df = df[titles]
    df.drop(["Flows", "Duration", "Source Port", "Packets"], axis=1, inplace=True)
    return df


def prepare_input(df):
    try:
        print(df["Protocol"])
        df["Protocol"] = protocol_encoder.transform(df["Protocol"])
    except ValueError:
        # Replace unknown labels with "RTP"
        print(df["Protocol"])
        unknown_protocol_labels = ~df["Protocol"].isin(protocol_encoder.classes_)
        df.loc[unknown_protocol_labels, "Protocol"] = "RTP"
        df["Protocol"] = protocol_encoder.transform(df["Protocol"])
        print(df["Protocol"])

    try:
        df["Flags"] = flags_encoder.transform(df["Flags"])
    except ValueError:
        # Replace unknown labels with "RTP"
        unknown_flags_labels = ~df["Flags"].isin(flags_encoder.classes_)
        df.loc[unknown_flags_labels, "Flags"] = "PAC_"
        df["Flags"] = flags_encoder.transform(df["Flags"])

    return df


def predict(input_data):
    scaled_input_data = scaler.transform(input_data)
    prediction = model.predict(scaled_input_data)
    return label_encoder.inverse_transform(prediction)


def main():
    results = {
        "Prediction": []
    }  # Initialize results as a dictionary with an empty list
    i = 0
    for message in pubsub.listen():
        i += 1
        if message["type"] == "message":
            data = json.loads(message["data"])
            print(f'{data["Destination IP"]}: {data["Source IP"]}')
            df = prepare_df(data)
            input_data = prepare_input(pd.DataFrame(df.iloc[[0]]))
            print("\n\n########## New Prediction ##########")
            print(input_data)
            prediction = predict(input_data)
            input_data["id"] = data["id"]
            # upload_to_redis(input_data["id"].copy(), prediction)
            print(f'{input_data["id"].copy()}: {prediction}')


# def main():
#     dff = df[df["Label"] == "Botnet"]
#     dff = pd.DataFrame(dff.iloc[[24000]])
#     dff.drop("Label", axis=1, inplace=True)
#     print(dff)
#     input_data = prepare_input(pd.DataFrame(dff.iloc[[0]]))
#     data = {
#         "Protocol": [10],
#         "Flags": [28],
#         "Bytes": [66.0],
#         "Destination Port": [80],
#         "Bytes per Packet": [66.0],
#         "Packets per Second": [1000.0],
#         "Bytes per Second": [66000.0],
#         "Is Encrypted Traffic": [0],
#         "Common Port Usage": [1],
#     }
#     input_data = pd.DataFrame(data)
#     prediction = predict(input_data)
#     # upload_to_redis(input_data["id"].copy(), prediction)
#     print(f"{prediction}")


# def main():
#     data = {
#         "id": "1714749086420-b2b7810a-4127-4df0-af2e-c2199845e225",
#         "Duration": 73.30608129501343,
#         "Protocol": "TCP",
#         "Source IP": "192.168.1.13",
#         "Source Port": 33199,
#         "Destination IP": "192.229.221.95",
#         "Destination Port": 80,
#         "Flags": ["PA", "S", "A_"],
#         "Packets": 3,
#         "Bytes": 410,
#         "Flows": 10,
#     }
#     df = prepare_df(data)
#     input_data = prepare_input(pd.DataFrame(df.iloc[[0]]))
#     print("\n\n########## New Prediction ##########")
#     print(input_data)
#     prediction = predict(input_data)
#     input_data["id"] = data["id"]
#     # upload_to_redis(input_data["id"].copy(), prediction)
#     print(f'{input_data["id"].copy()}: {prediction}')


if __name__ == "__main__":
    main()
