import matlab.engine
import cv2
import json
import os
import sys
sys.path.append('./cp_vton')
sys.path.append('./LIP_JPPNet')

from LIP_JPPNet.evaluate_parsing_JPPNet import *
from cp_vton.test import *
FINE_HEIGHT = 256
FINE_WIDTH = 192
POINT_NUM = 18

class opt():
    def __init__(self, name, stage, data_path, imname, cname, result_dir, checkpoint):
        self.name = name
        self.gpu_ids = ""
        self.workers = 1
        self.batch_size = 4
        self.data_path = data_path
        self.stage = stage
        self.imname = imname
        self.cname = cname
        self.fine_width = 192
        self.fine_height = 256
        self.radius = 5
        self.grid_size = 5
        self.grid_image = 'cp_vton/grid.png'
        self.result_dir = result_dir
        self.checkpoint = checkpoint
        self.shuffle = False

def create_dir(target_root_dir):
    if not os.path.exists(target_root_dir):
        os.makedirs(target_root_dir)
    dir_list = ['cloth', 'cloth-mask', 'image', 'image-parse', 'pose']
    for dir in dir_list:
        full_dir = os.path.join(target_root_dir, dir)
        if not os.path.exists(full_dir):
            os.makedirs(full_dir)


def run_mat(source_root_dir, target_root_dir, imname, cname):
    eng = matlab.engine.start_matlab()
    eng.convert_data(source_root_dir, target_root_dir, imname, cname, FINE_HEIGHT, FINE_WIDTH)
    eng.quit()


def convert_keypoints(source_root_dir, target_root_dir, imname):
        # load image
        im = cv2.imread(source_root_dir + 'image/' + imname)
        h = im.shape[0]
        w = im.shape[1]
        # load keypoints
        key_name = imname[:-4] + '_keypoints.json'
        with open(source_root_dir + 'pose/' + key_name, 'r') as rf:
            pose = json.load(rf)
        key_points = pose['people'][0]['pose_keypoints_2d']

        for i in range(POINT_NUM):
            key_points[3 * i] = key_points[3 * i] / w * FINE_WIDTH
            key_points[3 * i + 1] = key_points[3 * i + 1] / h * FINE_HEIGHT

        pose = {"version": 1.0, "people": [
            {"face_keypoints": [], "pose_keypoints": key_points, "hand_right_keypoints": [],
             "hand_left_keypoints": []}]}
        with open(target_root_dir + 'pose/' + key_name, 'w') as wf:
            json.dump(pose, wf)


def main(source_root_dir, target_root_dir, imname, cname):
    # get pose
    # os.system("OpenPose\\bin\OpenPoseDemo.exe --image_dir data\image\\")
    create_dir(target_root_dir)
    run_mat(source_root_dir, target_root_dir, imname, cname)
    convert_keypoints(source_root_dir, target_root_dir, imname)
    # get segment
    JPPNet_parsing(target_root_dir + 'image/' + imname, checkpoint_dir='LIP_JPPNet/checkpoint/JPPNet-s2', output_dir='data/test/image-parse/')
    # run cp-vton
    gmm_opt = opt(name="gmm_traintest_new", stage="GMM", data_path='data/test', result_dir='data/test', imname=imname, cname=cname, checkpoint='cp_vton/checkpoints/gmm_train_new/gmm_final.pth')
    inference(gmm_opt)
    tom_opt = opt(name="tom_test_new", stage="TOM", data_path='data/test', result_dir='result', imname=imname, cname=cname, checkpoint='cp_vton/checkpoints/tom_train_new/tom_final.pth')
    inference(tom_opt)

if __name__ == '__main__':
    main(source_root_dir='data/raw_data/', target_root_dir='data/test/', imname='000001_0.jpg', cname='000001_1.jpg')