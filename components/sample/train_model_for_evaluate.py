from kfp import dsl


@dsl.component(
    # https://cloud.google.com/vertex-ai/docs/training/pre-built-containers
    # TODO: Choose a training base image from the above link
    base_image="us-docker.pkg.dev/vertex-ai/training/tf-cpu.2-12.py310:latest",
    packages_to_install=[
        "tensorflow_decision_forests~=1.2",
    ],
)
def train_model(
    model_dir: str,
    label_column: str,
    train_bucket_name: str,
    train_bucket_object: str,
):
    # Add your training code here
    import pandas as pd
    import tensorflow_decision_forests as tfdf

    train_pd_df = pd.read_parquet(f"/gcs/{train_bucket_name}/{train_bucket_object}")
    train_ds = tfdf.keras.pd_dataframe_to_tf_dataset(train_pd_df, label=label_column)

    # Specify the model.
    model = tfdf.keras.RandomForestModel(verbose=2)

    # Train the model.
    model.fit(train_ds)

    # Save the model
    model.save(model_dir)
