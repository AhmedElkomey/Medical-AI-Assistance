import mlflow
import mlflow.pytorch
from typing import Dict, Any, Optional


class MedicalModelRegistry:
    """Handle model versioning and deployment stages"""
    
    def __init__(self, registry_uri: Optional[str] = None):
        if registry_uri:
            mlflow.set_registry_uri(registry_uri)
        
    def promote_model(self,
                     model_name: str,
                     version: int,
                     stage: str) -> None:
        """Promote model to specified stage (staging/production)"""
        client = mlflow.tracking.MlflowClient()
        client.transition_model_version_stage(
            name=model_name,
            version=version,
            stage=stage
        )
    
    def get_latest_production_model(self, model_name: str) -> mlflow.pyfunc.PyFuncModel:
        """Retrieve the latest production model"""
        return mlflow.pyfunc.load_model(f"models:/{model_name}/Production")
    
    def compare_model_versions(self,
                             model_name: str,
                             version1: int,
                             version2: int) -> Dict[str, Any]:
        """Compare metrics between two model versions"""
        client = mlflow.tracking.MlflowClient()
        
        run1 = client.get_run(client.get_model_version(model_name, version1).run_id)
        run2 = client.get_run(client.get_model_version(model_name, version2).run_id)
        
        return {
            'metrics_v1': run1.data.metrics,
            'metrics_v2': run2.data.metrics,
            'params_v1': run1.data.params,
            'params_v2': run2.data.params
        }