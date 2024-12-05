from typing import Dict, Type
from src.services.audio_files_service import process_audio_transcription
import os
import sys

from src.tasks.base_task import BaseTask
from src.tasks.base_task_v2 import BaseTaskV2
from src.tasks.week1.day1_antycaptcha import AntyCaptcha
from src.tasks.week1.day2_creature_authorization import CreatureAuthorization
from src.tasks.week1.day3_calibration import Calibration
from src.tasks.week1.day4_censure import Censure
from src.tasks.week2.day1_mp3 import Mp3
from src.tasks.week2.day3_robot_id import RobotId
from src.tasks.week2.day4_categories import Category
from src.tasks.week2.day5.day5_multimodal import MultimodalTask
from src.tasks.week3.S03E01_documents import Documents
from src.tasks.week3.S03E02_embedding.S03E02_embedding import EmbeddingTask
from src.tasks.week3.S03E03.S03E03_database import Database

# Map task names to their corresponding classes
TASK_MAP: Dict[str, Type[BaseTask | BaseTaskV2]] = {
    "audio": process_audio_transcription,  # Special case
    "antycaptcha": AntyCaptcha,
    "creature": CreatureAuthorization,
    "calibration": Calibration,
    "censure": Censure,
    "mp3": Mp3,
    "robot": RobotId,
    "category": Category,
    "multimodal": MultimodalTask,
    "documents": Documents,
    "embedding": EmbeddingTask,
    "database": Database,
}

def run_task(task_name: str) -> None:
    """
    Run a specific task based on the task name.
    
    Args:
        task_name: Name of the task to run (must be a key in TASK_MAP)
    """
    if task_name not in TASK_MAP:
        raise ValueError(f"Unknown task: {task_name}. Available tasks: {', '.join(TASK_MAP.keys())}")
    
    task_class = TASK_MAP[task_name]
    
    # Special handling for audio transcription
    if task_class == process_audio_transcription:
        task_class(os.path.expanduser("~/Desktop/test.mp3"))
        return
    
    # For all other tasks, instantiate and run
    task = task_class()
    result = task.run()
    print(f"Task {task_name} completed with result: {result}")

def main():
    # Get task name from command line argument, default to "database"
    task_to_run = sys.argv[1] if len(sys.argv) > 1 else "database"
    run_task(task_to_run)

if __name__ == "__main__":
    main() 