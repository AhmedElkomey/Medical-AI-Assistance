import mlflow
import mlflow.pytorch
from typing import Dict, Any, Optional
import torch
from datetime import datetime
import logging
from pathlib import Path

class MedicalMLflowTracker:
    """MLflow experiment tracking for medical AI models"""
    
    def __init__(self, 
                 experiment_name: str,
                 tracking_uri: Optional[str] = None,
                 artifacts_uri: Optional[str] = None):
        self.logger = logging.getLogger(__name__)
        
        # Configure MLflow
        if tracking_uri:
            mlflow.set_tracking_uri(tracking_uri)
        if artifacts_uri:
            mlflow.set_artifact_uri(artifacts_uri)
            
        # Set up experiment
        self.experiment = mlflow.set_experiment(experiment_name)
        
    def start_run(self, run_name: Optional[str] = None) -> mlflow.ActiveRun:
        """Start a new MLflow run"""
        return mlflow.start_run(run_name=run_name or f"run_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
    
    def log_model_training(self,
                          model: torch.nn.Module,
                          metrics: Dict[str, float],
                          params: Dict[str, Any],
                          artifacts: Dict[str, Path]) -> None:
        """Log model training details, metrics, and artifacts"""
        
        with self.start_run():
            # Log model parameters
            mlflow.log_params(params)
            
            # Log metrics
            mlflow.log_metrics(metrics)
            
            # Log the PyTorch model
            mlflow.pytorch.log_model(
                model,
                "model",
                registered_model_name=f"medical_ai_{datetime.now().strftime('%Y%m%d')}",
                conda_env=self._get_conda_env()
            )
            
            # Log additional artifacts
            for name, path in artifacts.items():
                mlflow.log_artifact(str(path), name)
            
            # Log system metrics
            if torch.cuda.is_available():
                mlflow.log_param("gpu_name", torch.cuda.get_device_name(0))
                mlflow.log_param("gpu_memory", torch.cuda.get_device_properties(0).total_memory)
    
    def log_medical_validation(self,
                             validation_results: Dict[str, Any],
                             model_version: str) -> None:
        """Log medical-specific validation metrics"""
        
        with self.start_run(run_name=f"medical_validation_{model_version}"):
            # Log validation metrics
            mlflow.log_metrics({
                "medical_accuracy": validation_results.get("accuracy", 0),
                "safety_score": validation_results.get("safety_score", 0),
                "citation_accuracy": validation_results.get("citation_accuracy", 0)
            })
            
            # Log validation details
            mlflow.log_dict(validation_results, "validation_details.json")
    
    def _get_conda_env(self) -> Dict[str, Any]:
        """Generate Conda environment specification"""
        return {
            'name': 'medical_ai_env',
            'channels': ['defaults', 'pytorch', 'conda-forge'],
            'dependencies': [
                'python=3.9',
                'pytorch',
                'transformers',
                'pandas',
                'numpy',
                'scikit-learn'
            ]
        }