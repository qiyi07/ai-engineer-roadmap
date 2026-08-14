import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from src.agents.agent_service import extract_weather_info

print(extract_weather_info("今天北京25度，晴，微风"))