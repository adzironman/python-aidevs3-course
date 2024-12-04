from src.services.audio_files_service import process_audio_transcription
import os

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

def main():
    # process_audio_transcription(os.path.expanduser("")) #e.g."~/Desktop/test.mp3"
    # creature_authorization = CreatureAuthorization()
    # creature_authorization.process()

    # calibration = Calibration()
    # print(calibration.run())

    # censure = Censure()
    # censure.run()

    # mp3 = Mp3()
    # mp3.run()

    # robot_id = RobotId()
    # robot_id.run()

    # category = Category()
    # category.run()

    # multimodal = MultimodalTask()
    # multimodal.run()

    # documents = Documents()
    # documents.run()

    embedding = EmbeddingTask()
    embedding.run()

if __name__ == "__main__":
    main() 