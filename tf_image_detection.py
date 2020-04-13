import os
import tensorflow as tf
import argparse
from PIL import Image, ImageFont, ImageDraw
import colorsys
import numpy as np
from yolo3.utils import letterbox_image
import time
from timeit import default_timer as timer

parser = argparse.ArgumentParser()
parser.add_argument('--image_directory')
parser.add_argument('--result_directory')
parser.add_argument('--model_path')
args = parser.parse_args()
image_directory = args.image_directory
result_directory = args.result_directory
model_path = args.model_path
gpu_options = tf.GPUOptions(per_process_gpu_memory_fraction=0.3)
sess = tf.Session(config=tf.ConfigProto(gpu_options=gpu_options, log_device_placement=False))
graph_def = tf.GraphDef()
with tf.io.gfile.GFile(model_path,'rb') as f:
    graph_def.ParseFromString(f.read())
    sess.graph.as_default()
    tf.import_graph_def(graph_def, name='')
graph = tf.get_default_graph()
image_input = graph.get_tensor_by_name('input_1:0')
boxes = graph.get_tensor_by_name('boxes:0')
scores = graph.get_tensor_by_name('scores:0')
classes = graph.get_tensor_by_name('classes:0')
input_image_shape = graph.get_tensor_by_name('Placeholder_366:0')

classes_path = 'model_data/pineapple_classes.txt'

with open(classes_path) as f:
    class_names = f.readlines()
class_names = [c.strip() for c in class_names]

hsv_tuples = [(x / len(class_names), 1., 1.)
              for x in range(len(class_names))]
colors = list(map(lambda x: colorsys.hsv_to_rgb(*x), hsv_tuples))
colors = list(
    map(lambda x: (int(x[0] * 255), int(x[1] * 255), int(x[2] * 255)),
                colors))

def detect_image(image, image_name): 
    boxed_image = letterbox_image(image, (416, 416)) #416.416
    image_data = np.array(boxed_image, dtype='float32')
    image_data /= 255.
    image_data = np.expand_dims(image_data, 0)  # Add batch dimension.

    start = timer()
    out_boxes, out_scores, out_classes = sess.run(
        [boxes, scores, classes],
        feed_dict={
            image_input: image_data,
            input_image_shape: [image.size[1], image.size[0]],
        })
    end = timer()
    print('Detection time:', end-start)

    font = ImageFont.truetype('Pillow/Tests/fonts/FreeMono.ttf', size=np.floor(3e-2 * image.size[1] + 0.5).astype('int32'))
    thickness = (image.size[0] + image.size[1]) // 300

    for i, c in reversed(list(enumerate(out_classes))):
        predicted_class = class_names[c]
        box = out_boxes[i]
        score = out_scores[i]

        label = '{} {:.6f}'.format(predicted_class, score)
        draw = ImageDraw.Draw(image)
        label_size = draw.textsize(label, font)

        top, left, bottom, right = box
        top = max(0, np.floor(top + 0.5).astype('int32'))
        left = max(0, np.floor(left + 0.5).astype('int32'))
        bottom = min(image.size[1], np.floor(bottom + 0.5).astype('int32'))
        right = min(image.size[0], np.floor(right + 0.5).astype('int32'))

        pos = '{} {} {} {}\n'.format(left, top, right, bottom)
        if top - label_size[1] >= 0:
            text_origin = np.array([left, top - label_size[1]])
        else:
            text_origin = np.array([left, top + 1])

        # My kingdom for a good redistributable image drawing library.
        for i in range(thickness):
            draw.rectangle(
                [left + i, top + i, right - i, bottom - i],
                outline=colors[c])
        draw.rectangle(
            [tuple(text_origin), tuple(text_origin + label_size)],
            fill=colors[c])
        draw.text(text_origin, label, fill=(0, 0, 0), font=font)
        del draw
    return image
for img in os.listdir(image_directory):
    if img.endswith('.jpeg'):
        print(img)
        try:
            image = Image.open(os.path.join(image_directory,img))
        except:
            print()
            print('Open Error! Try again!')
            continue
        else:
            r_image = detect_image(image, img)
            r_image.save(os.path.join(result_directory, img))
