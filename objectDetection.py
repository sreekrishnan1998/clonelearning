
from detectron2.engine import DefaultPredictor
import detectron2
from detectron2.utils.logger import setup_logger
setup_logger()
from detectron2.utils.video_visualizer import VideoVisualizer
from detectron2.config import get_cfg
from detectron2.data import MetadataCatalog
from detectron2.utils.visualizer import ColorMode, Visualizer
from detectron2 import model_zoo
from PIL import Image 
import PIL 
import cv2
import numpy as np
import tqdm
class Detector:

    def __init__(self, model_type = "objectDetection"):
        self.cfg = get_cfg()
        self.cfg.merge_from_file(r'C:\Users\HARI\detectron2\configs\COCO-Detection\faster_rcnn_R_50_FPN_3x.yaml')
        self.cfg.MODEL.WEIGHTS = (r'C:\Users\HARI\detectron2\model_final.pth')
        self.cfg.DATALOADER.NUM_WORKERS = 2
        self.cfg.MODEL.ROI_HEADS.NUM_CLASSES = 1
        self.cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.8
        self.cfg.MODEL.DEVICE = "cpu" # cpu or cuda
        self.cfg.DATASETS.TRAIN = ("trainDataset",)
        self.predictor = DefaultPredictor(self.cfg)

    def onImage(self, imagePath):
        image = cv2.imread(imagePath)
        if np.shape(image) != ():
        #if image is not None:
          
          predictions = self.predictor(image)
        
          invoice_metadata = MetadataCatalog.get("trainDataset")

          viz = Visualizer(image[:,:,::-1],metadata= invoice_metadata,scale=.75,instance_mode=ColorMode.IMAGE_BW )#instance_mode=ColorMode.IMAGE_BW)
        
          output = viz.draw_instance_predictions(predictions['instances'].to('cpu'))
          filename = 'result.jpg'
          cv2.imwrite(filename, output.get_image()[:,:,::-1])

          outtput_pred_boxes = predictions["instances"].pred_boxes
          counter = 0
          for i in outtput_pred_boxes.__iter__():
              counter += 1

          if(counter>=1):
            return "INVOICE IS TAMPERED"
          else:
            return 'INVOICE NOT TAMPERED'


        
        
       

        
        
        #cv2.imshow("Result",output.get_image()[:,:,::-1])
        #print("My ouput:",output["instances"])

    cv2.waitKey(0)
    cv2.destroyAllWindows()
