import argparse
from input_output import corrupt_video, write_video, read_video
from utils import find_outliers, reorder_frames, show_outliers


def main():
    parser = argparse.ArgumentParser(description='Reorder video')
    parser.add_argument("-v", "--video", required=True,
                        help="Input video file")
    parser.add_argument("-o", "--out", required=True, help="Output video file")
    parser.add_argument('--auto_threshold',  action='store_true', 
                        help="The threshold used to find the outliers is automatically calculated by kmeans")
    parser.add_argument('-m', "--mode", default='reorder', required=True,
                        help='modes can be reorder or corrupt')
    parser.add_argument('--show_outliers',  action='store_true', 
                        help="whether or not to show the found outliers")

    args = parser.parse_args()
    assert args.mode in ['reorder', 'corrupt']

    if args.mode == 'corrupt':
      corrupt_video(args.video, args.out)
    
    elif args.mode == 'reorder':
      frames = read_video(args.video)
      outliers, differences = find_outliers(frames, outlier_threshold=0.1, auto=args.auto_threshold)
      if args.show_outliers:
        show_outliers(frames, outliers, differences)

      clean_frames = [f.flatten() for i, f in enumerate(frames) if i not in outliers]
      clean_frames_idx = [i for i in range(len(frames)) if i not in outliers]

      order = reorder_frames(clean_frames)
      real_order = [clean_frames_idx[x] for x in order] # to consider removed frames
      write_video(args.video, args.out, real_order)
                              
    else:
      print('args.mode should be reorder or corrupt')


if __name__ == "__main__":
    main()
