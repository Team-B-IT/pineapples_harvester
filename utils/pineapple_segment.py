import cv2
def ripe_pineapple_segment(img, img_type='RGB'):
    '''
    Segment ripe pineapple with color
    Returns:
        np.array: Image threshold that 0 is non pineapple and 255 is pineapple
    '''
    if img_type == 'BGR':
        img_HSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    elif img_type == 'RGB':
        img_HSV = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
    else:
        raise ValueError('Image type must be RGB or BGR')
    low_H = 0
    high_H = 20
    low_S = 40
    high_S = 255
    low_V = 80
    high_V = 255
    img_th = cv2.inRange(img_HSV, (low_H, low_S, low_V), (high_H, high_S, high_V))
    morph_size = 2
    element = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2*morph_size + 1, 2*morph_size+1), (morph_size, morph_size))
    img_th = cv2.morphologyEx(img_th, cv2.MORPH_OPEN, element)
    return img_th
    
