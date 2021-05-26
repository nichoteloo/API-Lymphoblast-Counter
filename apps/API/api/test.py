from lib import LymphoCounterModel

WORKSPACE_PATH = 'Tensorflow/workspace'
ANNOTATION_PATH = WORKSPACE_PATH+'/annotations/label_map.pbtxt'
MODEL_PATH = WORKSPACE_PATH+'/models'
CONFIG_PATH = MODEL_PATH+'/my_ssd_mobnet/pipeline.config'
CHECKPOINT_PATH = MODEL_PATH+'/my_ssd_mobnet/bagus versi ssd 1/ckpt-9'

if __name__ == "__main__":
	model = LymphoCounterModel(IMAGE_PATH="img_1.jpg", ANNOTATION_PATH=ANNOTATION_PATH, CONFIG_PATH=CONFIG_PATH, CHECKPOINT_PATH=CHECKPOINT_PATH)
	model.detect_image()