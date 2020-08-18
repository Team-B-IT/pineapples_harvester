import pyrealsense2 as rs
import numpy as np
import cv2
import time


class realSenseStream():
    def __init__(self, path='./', w=1280, h=720):
        super().__init__()
        self.config = rs.config()  # Assign to realsense configuration
        self.pipeline = rs.pipeline()  # Assign to realsense pipeline
        self.path = path
        if self.path[-1] != '/':
            self.path = self.path + '/'
        self.pv_width = w
        self.pv_height = h
        self.size_config(self.pv_width, self.pv_height)
        self.profile = self.pipeline.start(self.config)

    def size_config(self, w, h):
        self.config.enable_stream(rs.stream.color, w, h, rs.format.bgr8, 30)
        self.config.enable_stream(rs.stream.depth, w, h, rs.format.z16, 30)

    def take_image(self):
        # Getting the depth sensor's depth scale (see rs-align example for explanation)
        depth_sensor = self.profile.get_device().first_depth_sensor()
        depth_scale = depth_sensor.get_depth_scale()
        print("Depth Scale is: " , depth_scale)
        
        while True:
            align_to = rs.stream.color
            align = rs.align(align_to)
            frames = self.pipeline.wait_for_frames()
            aligned_frames = align.process(frames)
            

			# Get aligned frames
            aligned_depth_frame = aligned_frames.get_depth_frame() # aligned_depth_frame is a 640x480 depth image
            color_frame = aligned_frames.get_color_frame()

			# Validate that both frames are valid
            if not aligned_depth_frame or not color_frame:
                continue
			
            # Generate depth map of image
            depth_map = [[0 for i in range(self.pv_width)] for j in range(self.pv_height)]

            for y in range(self.pv_height):
                for x in range(self.pv_width):
                    dist = aligned_depth_frame.get_distance(x, y)
                    depth_map[y][x] = float("{0:.10f}".format(dist))
                    # depth_map[y][x] = dist

            mid_x = int(self.pv_width / 2)
            mid_y = int(self.pv_height / 2)
            print(mid_x,'x',mid_y, ':', round(aligned_depth_frame.get_distance(mid_x, mid_y), 2), 'm')


            # Convert images to numpy arrays 
            # name = str(int(time.time()*1000.0))
            name = 'tmp'
            color_image = np.asanyarray(color_frame.get_data())
            imgName = self.path + name + '.jpeg'
            dataName = self.path + name + '.txt'


            # Write depth data to file
            f = open(dataName, 'w')
            for y in range(self.pv_height):
                for x in range(self.pv_width):
                    f.write(str(depth_map[y][x]) + ' ')
                if y != self.pv_height - 1:
                  f.write('\n')
            f.close()

            cv2.imwrite(imgName, color_image)
            cv2.waitKey(30)
            return imgName, dataName, color_image

    
    def get_frame(self):
        while True:
            frames = self.pipeline.wait_for_frames()
            color_frame = frames.get_color_frame()

            if not color_frame:
                continue
            # Convert images to numpy arrays
            # color_image = np.asanyarray(color_frame.get_data())
            x = np.asanyarray(color_frame.get_data())
            img = cv2.cvtColor(x,cv2.COLOR_BGR2RGB) #loi in ra anh
            img1=cv2.resize(img,dsize=(0,0),fx=0.72,fy=1,interpolation = cv2.INTER_AREA)
        
            # x = np.array(image)
            # imgName = self.path + str(int(time.time()*1000.0)) + '.jpeg'
            # cv2.imwrite(imgName, color_image) #lưu ảnh kiểu mảng numpy vào 1 file mới tên là imgName
            # cv2.waitKey(30)
            return img1

    def __del__(self):
        self.pipeline.stop()

if __name__ == '__main__':
    rss = realSenseStream()
    for i in range(10):
        rss.take_image()
        time.sleep(1)
