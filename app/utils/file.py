import json
from typing import Any
from langflow.load import load_flow_from_json
from pathlib import Path

class FlowLoadError(Exception):
  """Custom exception for flow loading errors"""
  pass

def load_flow(file_path: str | Path) -> Any:
  try:
    path = Path(file_path)
    
    if not path:
      raise FlowLoadError(f"Flow file not found: {file_path}")
    
    with path.open("r") as f:
      flow_data = json.load(f)
      
    return load_flow_from_json(flow_data)
  
  except json.JSONDecodeError as e:
    raise FlowLoadError(f"Invalid JSON in flow file: {str(e)}")
  except Exception as e:
    raise FlowLoadError(f"Error loading flow: {str(e)}")