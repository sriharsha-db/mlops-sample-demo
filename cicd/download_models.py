from mlflow.tracking.client import MlflowClient
from argparse import ArgumentParser
from pathlib import Path
import mlflow
import shutil
import os

class DownloadModels():
    def __init__(self) -> None:
        self.mlflow_client = MlflowClient()
        
        self.parser = ArgumentParser()
        self.parser.add_argument("env")
        self.parser.add_argument('model_name')

    def parse_args(self) -> None:
        args = self.parser.parse_args()
        self.model_name = args.model_name
        self.env = args.env
        print(f"env={self.env}, model name={self.model_name}")
        if self.model_name is None:
            raise RuntimeError('model name is not passed')

    def _format_model_uri(self, stage: str='Production') -> str:
        return f"models:/{self.model_name}/{stage}"

    def _download_models(self) -> None:
        model_path = self._format_model_uri()
        raw_model_path = os.path.join(model_path, 'data/feature_store/raw_model')
        downloaded_model_path = mlflow.artifacts.download_artifacts(raw_model_path)
        print('downloaded models path -',downloaded_model_path)
        print('files in downloaded path -',','.join(os.listdir(downloaded_model_path)))
        self._copy_models(downloaded_model_path)

    def _copy_models(self, downloaded_path) -> None:
        dest = 'service/models'
        Path(dest).mkdir(parents=True, exist_ok=True)
        shutil.copy(f"{downloaded_path}/model.pkl", f"{dest}/model.pkl")
        shutil.copy(f"{downloaded_path}/requirements.txt", f"{dest}/requirements.txt")

    def run_download_models(self) -> None:
        self._download_models()

if __name__ == '__main__':
    obj = DownloadModels()
    obj.parse_args()
    obj.run_download_models()
