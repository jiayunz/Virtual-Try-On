# Virtual-Try-On

This project has implemented a complete procedure of virtual try on based on [cp-vton](https://github.com/sergeywong/cp-vton), [OpenPose](https://github.com/CMU-Perceptual-Computing-Lab/openpose) and [JPPNet](https://github.com/Engineering-Course/LIP_JPPNet).

## Installation
* Clone this project to your directory.
* Download [OpenPose](https://github.com/CMU-Perceptual-Computing-Lab/openpose) to the```OpenPose``` directory and compile it according to its instruction.
* Download pre-trained model for [JPPNet](https://github.com/Engineering-Course/LIP_JPPNet) and put it under ```LIP_JPPNet/checkpoint/JPPNet-s2/```. There should be 4 files in this directory: checkpoint, model.ckpt-xxx.data-xxx, model.ckpt-xxx.index, model.ckpt-xxx.meta.
* Download pre-trained models for [cp-vton](https://github.com/sergeywong/cp-vton) and put them under ```cp_vton/checkpoints/```. There should be two folders as ```gmm_train_new``` and ```tom_train_new``` in this directory. The authors have not provided the original models but you may download the models from [a re-implemented one](https://github.com/cinastanbean/cp-vton).

## Usage
* Put the image and cloth under ```data/image```.
* Run ```python try_on.py``` to get the result.
* The result will be put in ```result/```.