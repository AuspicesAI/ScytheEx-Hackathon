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

df["proto"] = proto_encoder.fit_transform(df["proto"])
df["service"] = service_encoder.fit_transform(df["service"])
df["state"] = state_encoder.fit_transform(df["state"])
df["attack_cat"] = attack_cat_encoder.fit_transform(df["attack_cat"])


def fetch_data_from_db():
    # Setup Redis connection
    r = redis.Redis(host="6.tcp.eu.ngrok.io", port=19939, db=0)

    # Subscribe to the channel
    pubsub = r.pubsub()
    pubsub.subscribe("processed_data_channel")

    print("Subscribed to 'processed_data_channel'. Waiting for data...")
    i = 0
    # Listen for new messages
    for message in pubsub.listen():
        if message["type"] == "message":
            i += 1
            data = json.loads(message["data"])
            print("Received data:", data)
            if i == 1:
                df = pd.DataFrame([data])  # Create DataFrame with the first message
            else:
                df = pd.concat(
                    [df, pd.DataFrame([data])], ignore_index=True
                )  # Concatenate subsequent messages

            if i < 5:
                return df


def upload_output_to_db(input_data, prediction):
    pass


def prepare_input(input_df):
    input_df = input_df.astype(
        {
            "dur": "float64",
            "synack": "float64",
            "ackdat": "float64",
            "stcpb": "int64",
            "dtcpb": "int64",
            "trans_depth": "int64",
            "response_body_len": "int64",
            "ct_src_dport_ltm": "int64",
            "ct_dst_sport_ltm": "int64",
            "is_ftp_login": "int64",
            "ct_ftp_cmd": "int64",
            "ct_flw_http_mthd": "int64",
            "is_sm_ips_ports": "int64",
        }
    )
    titles = [
        "dur",
        "proto",
        "service",
        "state",
        "stcpb",
        "dtcpb",
        "synack",
        "ackdat",
        "trans_depth",
        "response_body_len",
        "ct_src_dport_ltm",
        "ct_dst_sport_ltm",
        "is_ftp_login",
        "ct_ftp_cmd",
        "ct_flw_http_mthd",
        "is_sm_ips_ports",
    ]

    tcp_state_mapping = {
        "LISTEN": "no",  # No direct action, waiting state
        "SYN_SENT": "REQ",  # Request sent, waiting for reply
        "SYN_RECEIVED": "INT",  # Intermediate state, part of handshake
        "ESTABLISHED": "CON",  # Connection successfully established
        "FIN_WAIT_1": "FIN",  # In the process of closing
        "FIN_WAIT_2": "FIN",  # In the process of closing
        "CLOSE_WAIT": "CLO",  # Waiting to close the connection
        "CLOSING": "CLO",  # In the process of closing
        "LAST_ACK": "CLO",  # Final acknowledgement state in closing
        "TIME_WAIT": "CLO",  # Waiting to ensure the remote TCP received the acknowledgment of its connection termination request
        "CLOSED": "CLO",  # No connection state at all
    }

    input_df = input_df[titles]

    input_df[input_df.select_dtypes(include="object").columns] = input_df[
        input_df.select_dtypes(include="object").columns
    ].apply(lambda x: x.str.lower())

    services = df["service"].unique()
    input_df["service"] = input_df["service"].apply(
        lambda x: x if x in services else "-"
    )

    states = df["state"].unique()

    input_df["state"] = input_df["state"].map(tcp_state_mapping)
    input_df["state"] = input_df["state"].apply(lambda x: x if x in states else "no")

    input_df["proto"] = proto_encoder.transform(input_df["proto"])
    input_df["service"] = service_encoder.transform(input_df["service"])
    input_df["state"] = state_encoder.transform(input_df["state"])
    print(input_df)

    return input_df


def predict(input_data):
    prediction = model.predict(input_data)
    return attack_cat_encoder.inverse_transform(prediction)


def prepare_output(output):
    return attack_cat_encoder.inverse_transform(output)


def main():
    raw_data = fetch_data_from_db()
    print(raw_data)
    input_data = prepare_input(raw_data)
    prediction = predict(input_data)
    print(prediction)
    # upload_output_to_db()


if __name__ == "__main__":
    main()
