# webcam-yolo

Scripts for using yolo to detect custom objects in webcam video feed.

The main files to pay attention to are as follows:

* `train.ipynb` is a notebook for fine-tuning a yolo model on a given dataset (e.g., exported from [label-studio](https://labelstud.io/)). Instructions are in the notebook. It's meant to be run in google colab with the dataset mounted in from a google drive.

* `webcam_yolo_osc.py` is a python script that loads a given (trained) yolo model, reads frames from a webcam, detects the highest-confidence object using the model, and sends an OSC message to /yolo with the x and y coordinates of the center of the detected object (in a loop). Lots of parameters are set as variables at the top of the file.

For convenience, `requirements.txt` is the standard python requirements file and `shell.nix` is a nix environment for running `webcam_yolo_osc.py`.
