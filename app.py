from src.services.audio_files_service import process_audio_transcription
import os

from src.tasks.week1.day1_antycaptcha import AntyCaptcha
from src.tasks.week1.day2_creature_authorization import CreatureAuthorization
from src.tasks.week1.day3_calibration import Calibration

def main():
    # process_audio_transcription(os.path.expanduser("")) #e.g."~/Desktop/test.mp3"
    # creature_authorization = CreatureAuthorization()
    # creature_authorization.process()

    calibration = Calibration()
    print(calibration.run())

if __name__ == "__main__":
    main() 