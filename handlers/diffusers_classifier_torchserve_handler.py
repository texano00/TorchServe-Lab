from abc import ABC
import json
import logging
import os
import subprocess
import torch
from diffusers import StableDiffusionPipeline

from ts.torch_handler.base_handler import BaseHandler

logger = logging.getLogger(__name__)


class TransformersClassifierHandler(BaseHandler, ABC):
    """
    Transformers text classifier handler class. This handler takes a text (string) and
    as input and returns the classification text based on the serialized transformers checkpoint.
    """
    def __init__(self):
        logger.info('__init__ TransformersClassifierHandler')
        super(TransformersClassifierHandler, self).__init__()
        self.initialized = False

    def initialize(self, ctx):
        logger.info('initialize TransformersClassifierHandler')
        self.manifest = ctx.manifest

        properties = ctx.system_properties
        model_dir = properties.get("model_dir")
        # self.device = torch.device("cuda:" + str(properties.get("gpu_id")) if torch.cuda.is_available() else "cpu")
        logger.info("Device: %s", self.device)
        print("model_dir: ", model_dir)

        device = None
        if(torch.cuda.is_available()):
            logger.info("Cuda is available. Using GPU")
            logger.info("Cuda device count: %s", torch.cuda.device_count())
            logger.info("Cuda device name: %s", torch.cuda.get_device_name(0))
            logger.info("Cuda current device: %s", torch.cuda.current_device())
            device = properties.get("gpu_id")
        else:
            logger.info("Cuda is not available. Using CPU")
            device = -1
            
        self.pipe = StableDiffusionPipeline.from_pretrained(model_dir, torch_dtype=torch.float16, device=device)
        self.pipe = self.pipe.to("cuda")        
        logger.debug('StableDiffusionPipeline model from path {0} loaded successfully'.format(model_dir))

        self.initialized = True

    def preprocess(self, data):
        """ Very basic preprocessing code - only tokenizes.
            Extend with your own preprocessing steps as needed.
        """
        logger.info("Performing preprocessing")
        logger.info(data)
        logger.info(data[0])
        logger.info("Received text: '%s'", data[0]['body'])

        return data

    def inference(self, inputs):
        """
        Predict the class of a text using a trained transformer model.
        """
        # NOTE: This makes the assumption that your model expects text to be tokenized  
        # with "input_ids" and "token_type_ids" - which is true for some popular transformer models, e.g. bert.
        # If your transformer model expects different tokenization, adapt this code to suit 
        # its expected input format.
        logger.info("Performing inference")
        logger.info(inputs)
        
        prediction = self.pipe(inputs[0]['body'])
        logger.info("Model predicted: '%s'", prediction)
        logger.info("Model predicted after")

        return prediction

    def postprocess(self, inference_output):
        logger.info("Performing postprocessing")    
        # TODO: Add any needed post-processing of the model predictions here
        return [inference_output]


_service = TransformersClassifierHandler()


def handle(data, context):
    try:
        if not _service.initialized:
            _service.initialize(context)

        if data is None:
            return None

        data = _service.preprocess(data)
        data = _service.inference(data)
        data = _service.postprocess(data)

        return data
    except Exception as e:
        raise e