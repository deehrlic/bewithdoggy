# bewithdoggy

Dataset can be found at: https://pjreddie.com/darknet/yolo/
We used the YOLOv3-320 configuration based on the tutorial here: https://thinkinfi.com/yolo-object-detection-using-python-opencv/

File Purposes:

*opencv.py* - This files stores the classification function and does the post-processing, including the SCP file transfer

*controller.py* - This file operates the servo motors after receiving instructions from opencv.py

*direction.txt* - the file that stored the next direction that both above files reference

