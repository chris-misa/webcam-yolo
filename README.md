# webcam-yolo

Scripts for using yolo to detect custom objects in webcam video feed.

The main files are:

* `train.ipynb` is a notebook for fine-tuning a yolo model on a given dataset (e.g., exported from [label-studio](https://labelstud.io/)). Instructions are in the notebook. It's meant to be run in google colab with the dataset mounted in from a google drive. You can also upload a zip file.

* `webcam_yolo_osc.py` is a python script that loads a given (trained) yolo model, reads frames from a webcam, detects the highest-confidence object using the model, and sends an OSC message to /yolo with the x and y coordinates of the center of the detected object (in a loop). Lots of parameters are set as variables at the top of the file.

# Requirements

Python version 3.10 or 3.9. More recent versions also might work depending on the platform (see "Platform Notes").

Python library requirements are listed in `requirements.txt`.

# Installation

The easiest way is to use a python virtual environment (venv) by running the following commands:

```
$ python -m venv ./venv
$ source ./venv/bin/activate
(venv) $ pip install --upgrade pip
(venv) $ pip install -r requirements.txt
```

## Platform Notes

**MacOS**

Tested on MacOS 15.6 (python 3.9.6) and MacOS 15.7 (python 3.10 from homebrew).

Note that the newer version of python included by default in MacOS 15.7 appears to have some issues supporting the particular mix of python libraries required here. Hopefully this will get fixed in future MacOS releases.

**Linux**

Tested on nixos-25.11 (python 3.11.14). The included `shell.nix` creates an environment with additional system dependencies required by the opencv python library.

**Windows**

Not tested.

# Running Training

Run `train.ipynb` in a jupyter environment like google colab. Instructions for setting up your own local jupyter environment are outside the scope of this README.

# Running Object Detection

## Setup

First, open `webcam_yolo_osc.py` in a text editor and make the following changes to specify where OSC messages should be sent and which particular trained model to use (and possibly also which camera to use if you have multiple cameras).

**OSC Destination**

Edit the definition of `ENDPOINTS`, to include the IP address, UDP port number pairs that describe which OSC endpoints to send to. For example, if you have an OSC process listening on the local computer on port 8000 and another listening on a remote computer with IP address 1.2.3.4 listening on port 8080, you might write

```
ENDPOINTS = [
  ("127.0.0.1", 8000),
  ("1.2.3.4", 8080),
]
```

**Trained Model**

Edit the definition of `model` to point to the file with the model weights that you exported from `train.ipynb`. For example, if you exported a weight file called "my-weights.py" to this directory, you might write

```
model = YOLO("my-weights.py")
```

To test without your own trained weights, you can use a generic pre-trained YOLO model by passing the name of the model you want to use to `YOLO()`. For example,

```
model = YOLO("yolo26n.pt")
```

Note however, that the current version of `webcam_yolo_osc.py` only supports a single class so if you run it with multi-class models (like `yolo26n.pt`) you won't be able to use the class labels the model is also producing. (If you want this feature, submit a PR!)

**Camera**

Edit the definition of `capture` to point to the camera you want to use. The cv2 library refers to cameras by index number. The index 0 seems to refer to the default camera. If you plug in another, it seems to show up as index 2. Might take some experimentation.

## Running

Once everything is properly set up, start the object detection process by simply running

```
(venv) $ python webcam_yolo_osc.py
```

Note that if you are in a new shell/terminal, you'll need to change to this directory and enter the python virtual environment first, e.g., by  running:

```
$ cd path/to/this/directory
$ source ./venv/bin/activate
(venv) $ python webcam_yolo_osc.py
```

The script should open a window where you can monitor the results and start sending OSC messages to the endpoints you specified in the setup.

To stop it, click on the window (to make sure it's in the foreground) and press "q". (Or click on the terminal window and press "CTRL-C".)
