import tensorflow as tf
from pathlib import Path
import mlflow
import mlflow.keras
import dagshub

from src.cnnClassifier.entity.config_entity import EvaluationConfig
from src.cnnClassifier.utils.common import save_json


class Evaluation:
    def __init__(self, config: EvaluationConfig):
        self.config = config

    # ---------------------------------------------
    # Create validation data generator
    # ---------------------------------------------
    def _valid_generator(self):

        datagenerator_kwargs = dict(
            rescale=1./255,
            validation_split=0.30
        )

        dataflow_kwargs = dict(
            target_size=self.config.params_image_size[:-1],
            batch_size=self.config.params_batch_size,
            interpolation="bilinear"
        )

        valid_datagenerator = tf.keras.preprocessing.image.ImageDataGenerator(
            **datagenerator_kwargs
        )

        self.valid_generator = valid_datagenerator.flow_from_directory(
            directory=self.config.training_data,
            subset="validation",
            shuffle=False,
            **dataflow_kwargs
        )

    # ---------------------------------------------
    # Load trained model
    # ---------------------------------------------
    @staticmethod
    def load_model(path: Path) -> tf.keras.Model:
        return tf.keras.models.load_model(path)

    # ---------------------------------------------
    # Evaluate model
    # ---------------------------------------------
    def evaluation(self):
        self.model = self.load_model(self.config.path_of_model)
        self._valid_generator()
        self.score = self.model.evaluate(self.valid_generator)
        self.save_score()

    # ---------------------------------------------
    # Save scores locally
    # ---------------------------------------------
    def save_score(self):
        scores = {
            "loss": self.score[0],
            "accuracy": self.score[1]
        }
        save_json(path=Path("scores.json"), data=scores)

    # ---------------------------------------------
    # Log into MLflow + Register model
    # ---------------------------------------------
    def log_into_mlflow(self):

        # Initialize dagshub + mlflow
        dagshub.init(
            repo_owner="sableen-kaur788",
            repo_name="KideyDeepLearning",
            mlflow=True
        )

        mlflow.set_tracking_uri(
            "https://dagshub.com/sableen-kaur788/KideyDeepLearning.mlflow"
        )

        mlflow.set_experiment("Kidney_Detection")

        with mlflow.start_run():

            # Log hyperparameters
            mlflow.log_params(self.config.all_params)

            # Log metrics
            mlflow.log_metrics({
                "loss": self.score[0],
                "accuracy": self.score[1]
            })

            # Register model (creates versions)
            mlflow.keras.log_model(
                self.model,
                artifact_path="model",
                registered_model_name="KidneyTumorModel"
            )

            print("✅ Model logged & registered in MLflow successfully!")
