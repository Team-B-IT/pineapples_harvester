import sys
import argparse
import os
from yolo import YOLO, detect_video
from PIL import Image


def detect_img(yolo, input, output):

    for img in os.listdir(input):
        if img.endswith('.jpeg'):
            print(img)
            try:
                image = Image.open(os.path.join(input, img))
            except:
                print()
                print('Open Error! Try again!')
                continue
            else:
                r_image = yolo.detect_image(image, img)
                r_image.show()
                r_image.save(os.path.join(output, img))
    yolo.close_session()


FLAGS = None

if __name__ == '__main__':
    # class YOLO defines the default value, so suppress any default here
    parser = argparse.ArgumentParser(argument_default=argparse.SUPPRESS)
    '''
    Command line options
    '''
    parser.add_argument(
        '--model_path', type=str,
        help='path to model weight file, default ' +
        YOLO.get_defaults("model_path")
    )

    parser.add_argument(
        '--anchors', type=str,
        help='path to anchor definitions, default ' +
        YOLO.get_defaults("anchors_path")
    )

    parser.add_argument(
        '--classes', type=str,
        help='path to class definitions, default ' +
        YOLO.get_defaults("classes_path")
    )

    parser.add_argument(
        '--gpu_num', type=int,
        help='Number of GPU to use, default ' +
        str(YOLO.get_defaults("gpu_num"))
    )

    parser.add_argument(
        '--image', default=False, action="store_true",
        help='Image detection mode'
    )
    '''
    Command line positional arguments -- for video detection mode
    '''
    parser.add_argument(
        "--input", nargs='?', type=str, required=False, default='./path2your_video',
        help="Video input path or input images folder"
    )

    parser.add_argument(
        "--output", nargs='?', type=str, default="",
        help="[Optional] Video output path or output images folder"
    )

    FLAGS = parser.parse_args()
    print(FLAGS)

    if FLAGS.image:
        """
        Image detection mode
        """
        print("Image detection mode")
        if "input" in FLAGS:
            detect_img(YOLO(**vars(FLAGS)), FLAGS.input, FLAGS.output)
        else:
            print("Must specify at least video_input_path.  See usage with --help.")
    
    elif "input" in FLAGS:
        detect_video(YOLO(**vars(FLAGS)), FLAGS.input, FLAGS.output)
    else:
        print("Must specify at least video_input_path.  See usage with --help.")
