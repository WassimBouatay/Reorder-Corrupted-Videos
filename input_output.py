import cv2
import random
import os


def read_video(video, downsample_ratio=4):
    cap = cv2.VideoCapture(video)
    frames = []
    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret == True:
            smaller_frame = cv2.resize(frame, (frame.shape[1]//downsample_ratio, frame.shape[0]//downsample_ratio))
            frames.append(smaller_frame)
        else:
            break
    return frames


def write_video(input_video, out, order, both_directions=True):
    print("Writing video .. ")
    cap = cv2.VideoCapture(input_video)
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
                  int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    frames = read_video(input_video, downsample_ratio=1)

    out_video = cv2.VideoWriter(out, cv2.VideoWriter_fourcc(*'mp4v'), fps, frame_size)
    for idx in order:
        out_video.write(frames[idx])

    if both_directions:
        ## We also save the reversed video since we do not know if the order we made is correct in time or reversed
        out_video = cv2.VideoWriter(out[:-4]+'_reversed.mp4', cv2.VideoWriter_fourcc(*'mp4v'), fps, frame_size)
        for idx in order[::-1]:
            out_video.write(frames[idx])


def corrupt_video(video, out):
    ## add random images from "data/outliers_to_corrupt/" and shuffle the whole
    cap = cv2.VideoCapture(video)
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
                  int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))

    frames = read_video(video, downsample_ratio=1)
    folder_dir = "data/outliers_to_corrupt"
    outliers = os.listdir(folder_dir)
    for x in outliers:
        img = cv2.imread("data/outliers_to_corrupt/"+x)
        img = cv2.resize(img, frame_size)
        frames.append(img)

    order = list(range(len(frames)))
    random.shuffle(order)

    print("Writing video ..")
    out_video = cv2.VideoWriter(out, cv2.VideoWriter_fourcc(*'mp4v'), fps, frame_size)
    for idx in order:
        out_video.write(frames[idx])
