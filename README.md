# Reorder-Corrupted-Videos
A corrupted video is a video that has random frames added to it and then shuffled. The goal is to remove the random images and reorder the video.
The solution provided in this repo allows you to save the both ordered and reversed videos.


# Dependencies
Please install the required dependencies with:

```
pip install --upgrade pip setuptools wheel
pip install -r requirement.txt
```

# How to use
There are two modes:

```corrupt``` mode: can be used to corrupt a clean video. The random images that will be added are the images in the folder ```data\outliers_to_corrupt```.
Example:
```
python .\main.py -m corrupt -v .\data\video_to_corrupt.mp4 -o .\data\corrupted_video_2.mp4 
```

```reorder``` mode: can be used to remove the outliers and reorder a video. 
Example:
```
python .\main.py -m reorder -v .\data\corrupted_video.mp4 -o .\output\reorder_corrupted_video.mp4 --show_outliers --auto_threshold
```

--auto_threshold: Choses an automatique threshold to filter outliers using kmeans, otherwise 0.1 will be the default threshold.

--show_outliers: shows the distribution of the frames compared to a median frame, and shows some of the removed frames that are counted as outliers.
