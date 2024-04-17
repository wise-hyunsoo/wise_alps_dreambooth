import os

from kfp import dsl

CONTAINER_REPOSITORY = os.getenv("CONTAINER_REPOSITORY")


@dsl.component(
    base_image=f"{CONTAINER_REPOSITORY}/custom-tf-cpu.2-12.py310:latest",
    install_kfp_package=False,
)
def train_model(
    model_dir: str,
    label_column: str,
    train_bucket_name: str,
    train_bucket_object: str,
):
    # Add your training code here
    import tensorflow as tf

    mnist = tf.keras.datasets.mnist
    (x_train, y_train), (x_test, y_test) = mnist.load_data()
    x_train, x_test = x_train / 255.0, x_test / 255.0

    model = tf.keras.models.Sequential(
        [
            tf.keras.layers.Flatten(input_shape=(28, 28)),
            tf.keras.layers.Dense(128, activation="relu"),
            tf.keras.layers.Dropout(0.2),
            tf.keras.layers.Dense(10, activation="softmax"),
        ]
    )
    model.compile(
        optimizer="adam",
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"],
    )
    model.fit(x_train, y_train, epochs=2)

    # NOTE: To use one of these prebuilt containers, you must save your model as one or more model artifacts
    #   that comply with the requirements of the prebuilt container.
    #   https://cloud.google.com/vertex-ai/docs/training/exporting-model-artifacts
    model.save(model_dir)
