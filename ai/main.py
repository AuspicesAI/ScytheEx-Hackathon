import os
import redis
import pandas as pd
import pickle
from sklearn.preprocessing import LabelEncoder
import xgboost as xgb

train = pd.read_csv("data/training.csv")
test = pd.read_csv("data/testing.csv")
combined_df = pd.concat([train, test], ignore_index=True)
df = combined_df.sample(frac=1).reset_index(drop=True)
proto_encoder = LabelEncoder()
service_encoder = LabelEncoder()
state_encoder = LabelEncoder()
attack_cat_encoder = LabelEncoder()
attack_cat_decoder = LabelEncoder()
attack_cat_decoder.fit(attack_cat_encoder.classes_)
with open("16_XGBoost_model.pkl", "rb") as model_file:
    model = pickle.load(model_file)

df["proto"] = proto_encoder.fit_transform(df["proto"])
df["service"] = service_encoder.fit_transform(df["service"])
df["state"] = state_encoder.fit_transform(df["state"])
df["attack_cat"] = attack_cat_encoder.fit_transform(df["attack_cat"])


def fetch_data_from_db():
    # Setup Redis connection
    redishost = "localhost"
    redis_port = 6379
    redis_db = 0
    client = redis.Redis(host=redishost, port=redis_port, db=redis_db)

    # Setup Redis Pub/Sub
    pubsub = client.pubsub()
    pubsub.subscribe("packet_stream")

    print("Subscribed to 'packet_stream', listening for new messages...")
    try:
        for message in pubsub.listen():
            if message["type"] == "message":
                print("Received Data:", message["data"].decode("utf-8"))

    except KeyboardInterrupt:
        print("Stopped listening to 'packet_stream'")
    finally:
        pubsub.close()
        return message["data"].decode("utf-8")


def upload_output_to_db(input_data, prediction):
    pass


def prepare_input(input):

    input_df = pd.DataFrame(input)
    input_df["proto"] = proto_encoder.fit_transform(input_df["proto"])
    input_df["service"] = service_encoder.fit_transform(input_df["service"])
    input_df["state"] = state_encoder.fit_transform(input_df["state"])

    return input_df


def predict(input_data):
    return model.predict(input_data)


def prepare_output(output):
    return attack_cat_decoder.inverse_transform(output)


def main():
    raw_data = fetch_data_from_db()
    input_data = prepare_input(raw_data)
    prediction = predict(input_data)
    upload_output_to_db()


if __name__ == "__main__":
    main()
