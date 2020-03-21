import sys
import argparse
import os
import json
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
        '--config_path', nargs='?', type=str, default='config/inference.json',
        help='path to config file, default config/inference.cfg'
    )

    parser.add_argument(
        "--input", nargs='?', type=str, required=False, default='./path2your_image',
        help="Input images path or folder"
    )

    parser.add_argument(
        "--output", nargs='?', type=str, default="",
        help="[Optional] Output images folder"
    )

    FLAGS = parser.parse_args()
    print(FLAGS)

    """
    Image detection mode
    """
    print("Image detection mode")
    if "input" in FLAGS:
        with open(FLAGS.config_path) as json_data_file:
            config = json.load(json_data_file)
        
        print(config)
        
        # model = dict(config._sections['model'])

        # model['gpu_num'] = int(model['gpu_num'])
        # model['iou'] = float(model['iou'])
        # model['gpu_num'] = int(model['gpu_num'])
        # print(model)
        detect_img(YOLO(**config), FLAGS.input, FLAGS.output)
    else:
        print("Must specify at least input image.  See usage with --help.")
