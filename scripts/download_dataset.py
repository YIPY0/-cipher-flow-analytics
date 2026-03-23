"""
CIPHER-FLOW ANALYTICS — Dataset Download Helper
Downloads CIC-IDS2017 dataset files.

Note: The dataset is hosted at UNB and is approximately 2.8 GB.
If direct download fails, download manually from:
https://www.unb.ca/cic/datasets/ids-2017.html
"""
import os
import sys
import urllib.request
import logging

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("download")

# These are the mirror URLs — update if UNB changes them
CIC_FILES = {
    "Monday-WorkingHours.pcap_ISCX.csv": "http://205.174.165.80/CICDataset/CIC-IDS-2017/Dataset/MachineLearningCSV/MachineLearningCVE/Monday-WorkingHours.pcap_ISCX.csv",
    "Tuesday-WorkingHours.pcap_ISCX.csv": "http://205.174.165.80/CICDataset/CIC-IDS-2017/Dataset/MachineLearningCSV/MachineLearningCVE/Tuesday-WorkingHours.pcap_ISCX.csv",
    "Wednesday-workingHours.pcap_ISCX.csv": "http://205.174.165.80/CICDataset/CIC-IDS-2017/Dataset/MachineLearningCSV/MachineLearningCVE/Wednesday-workingHours.pcap_ISCX.csv",
    "Thursday-WorkingHours-Morning-WebAttacks.pcap_ISCX.csv": "http://205.174.165.80/CICDataset/CIC-IDS-2017/Dataset/MachineLearningCSV/MachineLearningCVE/Thursday-WorkingHours-Morning-WebAttacks.pcap_ISCX.csv",
    "Thursday-WorkingHours-Afternoon-Infilteration.pcap_ISCX.csv": "http://205.174.165.80/CICDataset/CIC-IDS-2017/Dataset/MachineLearningCSV/MachineLearningCVE/Thursday-WorkingHours-Afternoon-Infilteration.pcap_ISCX.csv",
    "Friday-WorkingHours-Morning.pcap_ISCX.csv": "http://205.174.165.80/CICDataset/CIC-IDS-2017/Dataset/MachineLearningCSV/MachineLearningCVE/Friday-WorkingHours-Morning.pcap_ISCX.csv",
    "Friday-WorkingHours-Afternoon-PortScan.pcap_ISCX.csv": "http://205.174.165.80/CICDataset/CIC-IDS-2017/Dataset/MachineLearningCSV/MachineLearningCVE/Friday-WorkingHours-Afternoon-PortScan.pcap_ISCX.csv",
    "Friday-WorkingHours-Afternoon-DDos.pcap_ISCX.csv": "http://205.174.165.80/CICDataset/CIC-IDS-2017/Dataset/MachineLearningCSV/MachineLearningCVE/Friday-WorkingHours-Afternoon-DDos.pcap_ISCX.csv",
}


def download():
    dest = settings.DATASET_DIR
    dest.mkdir(parents=True, exist_ok=True)

    for filename, url in CIC_FILES.items():
        filepath = dest / filename
        if filepath.exists():
            logger.info("Already exists: %s", filename)
            continue
        logger.info("Downloading %s …", filename)
        try:
            urllib.request.urlretrieve(url, filepath)
            logger.info("  Saved → %s", filepath)
        except Exception as e:
            logger.error("  Failed: %s", e)
            logger.error("  Download manually from https://www.unb.ca/cic/datasets/ids-2017.html")


if __name__ == "__main__":
    download()