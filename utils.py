import cv2
import numpy as np
from scipy.spatial import distance
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import ImageGrid
from sklearn.cluster import KMeans


def find_outliers(frames, outlier_threshold=0.1, auto=False):
  list_of_hist = []
  n_bins = 4
  for frame in frames:
    list_of_hist.append(cv2.calcHist([frame], [0, 1, 2], None, [n_bins, n_bins, n_bins], [0, 256, 0, 256, 0, 256]))

  list_of_hist = np.array(list_of_hist).reshape((len(list_of_hist), n_bins*n_bins*n_bins)) / (n_bins*n_bins*n_bins)
  median_hist = np.median(list_of_hist, axis=0)
  differences = np.array([distance.cosine(hist, median_hist) for hist in list_of_hist])

  if auto:
    kmeans = KMeans(n_clusters=2, random_state=0, n_init="auto").fit(differences.reshape(len(differences), 1))
    outlier_threshold = min(kmeans.cluster_centers_)[0]*5
    m1, m2 = min(kmeans.cluster_centers_)[0], max(kmeans.cluster_centers_)[0]
    cluster_1 = differences[kmeans.labels_ == 0]
    cluster_2 = differences[kmeans.labels_ == 1]
    m1, m2 = np.mean(cluster_1), np.mean(cluster_2)
    v1, v2 = np.std(cluster_1), np.std(cluster_2)
    if m1 > m2:
        m1, m2 = m2, m1
        v1, v2 = v2, v1
    outlier_threshold = m1 + (m2-m1)/(v1+v2)*v1

    print('Auto threshold: {:.3f}'.format(outlier_threshold))

  outliers = np.array([x for x in range(len(differences)) if differences[x] > outlier_threshold])
  print("Number of ouliers: ", len(outliers))
  return outliers, differences


def reorder_frames(frame_list):
    differences = distance.cdist(frame_list, frame_list, 'euclidean')

    ## First we order the frames 
    first_img = 0 # Random start
    ordered = [first_img]
    for _ in range( len(frame_list)-1):
      last_img = ordered[-1]
      arg_l = np.argsort(differences[last_img]) 
      # closest img to the current one not in the ordered list
      i = 0
      while(arg_l[i] in ordered):
        i += 1
      to_add = arg_l[i]

      if len(ordered) > 1:
        first_img = ordered[0]
        arg_l_start = np.argsort(differences[first_img]) 
        i = 0
        while(arg_l_start[i] in ordered):
          i += 1
        to_add_begining = arg_l_start[i]
        if differences[first_img][to_add_begining] < differences[last_img][to_add]:
          ordered = [to_add_begining] + ordered
        else:
          ordered.append(to_add)
      else:
        ordered.append(to_add)

    # find the real starting frame 
    idx_max_diff = 0
    max_diff = differences[len(differences)-1][ordered[0]]
    for i in range(len(ordered)-1):
      if differences[ordered[i]][ordered[i+1]] > max_diff:
        max_diff = differences[ordered[i]][ordered[i+1]]
        idx_max_diff = i+1

    real_start = idx_max_diff
    ordered = ordered[real_start:] + ordered[0:real_start]
    return ordered


def show_outliers(frames, outliers, differences):
    "shows a sample of outliers"

    _ = plt.hist(differences, bins=30)
    plt.title("Histogram of cosine-similarity between each frame and the median frame")
    plt.show()
    if len(outliers) == 0:
        return

    cpt = 0
    outliers = outliers[:10]
    if len(outliers) < 10:
        figure, axis = plt.subplots(2, len(outliers)//2, figsize=(35, 10))
        n_col = len(outliers)//2
    else:
        figure, axis = plt.subplots(2, 5, figsize=(35, 10))
        n_col = 5

    for idx in outliers:
        axis[cpt//n_col, cpt%n_col].imshow(frames[idx])
        axis[cpt//n_col, cpt%n_col].set_title("{:.2f}".format(differences[idx]))
        cpt += 1
        if cpt == 2*n_col:
            break
    plt.show()