import os
import cv2
import numpy as np
import tensorflow as tf
from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as viz_utils
from object_detection.builders import model_builder
from object_detection.utils import config_util
from object_detection.protos import pipeline_pb2
from google.protobuf import text_format

###########################################################################################################

class LymphoCounterModel:
    def __init__(self, IMAGE_PATH, ANNOTATION_PATH, CONFIG_PATH, CHECKPOINT_PATH):
        self.image_path = IMAGE_PATH
        self.annotation_path = ANNOTATION_PATH
        self.config_path = CONFIG_PATH
        self.checkpoint_path = CHECKPOINT_PATH
    
    def load_config(self):
        configs = config_util.get_configs_from_pipeline_file(self.config_path)
        detection_model = model_builder.build(model_config=configs['model'], is_training=False)

        ckpt = tf.compat.v2.train.Checkpoint(model=detection_model)
        ckpt.restore(self.checkpoint_path).expect_partial()
        return detection_model
    
    def cat_index(self):
        return label_map_util.create_category_index_from_labelmap(self.annotation_path)
    
    def load_image(self):
        frame = cv2.imread(self.image_path)
        frame_np = np.array(frame) 
        return frame_np
    
    @tf.function
    def detect_fn(self, image):
    	detection_model = self.load_config()
    	image, shapes = detection_model.preprocess(image)
    	prediction_dict = detection_model.predict(image, shapes)
    	detections = detection_model.postprocess(prediction_dict, shapes)
    	return detections
    
    def detect_image(self, label_id_offset=1, save=True, extract=None, result=None):
        frame = self.load_image()
        category_index = self.cat_index()
        tf.config.run_functions_eagerly(True)
        
        input_tensor = tf.convert_to_tensor(np.expand_dims(frame, 0), dtype=tf.float32)
        detections = self.detect_fn(input_tensor)

        num_detections = int(detections.pop('num_detections'))
        detections = {key: value[0, :num_detections].numpy() for key, value in detections.items()}
        detections['num_detections'] = num_detections

        # detection_classes should be ints.
        detections['detection_classes'] = detections['detection_classes'].astype(np.int64)

        image_np_with_detections = frame.copy()

        image_np_with_detections = viz_utils.visualize_boxes_and_labels_on_image_array(
												image_np_with_detections,
												detections['detection_boxes'],
												detections['detection_classes']+label_id_offset,
												detections['detection_scores'],
												category_index,
												use_normalized_coordinates=True,
												max_boxes_to_draw=20,
												min_score_thresh=.75,
												agnostic_mode=False)

        basename_res = os.path.basename(self.image_path)
        result_paths = os.path.join(result, f"{basename_res}")
        status = cv2.imwrite(result_paths, image_np_with_detections)

        return result_paths