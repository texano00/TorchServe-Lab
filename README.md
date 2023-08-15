# TorchServe Lab
**Inference** **stress tests** tests using [TorchServe](https://pytorch.org/serve/) (most models from **HuggingFace**).\
The intent of this repo is to report some test with very different configurations, ex:
* using CPU instead of GPU
* TorchServe settings
* GPU time slicing
* GPU sharing
* Scaling on Kubernetes

to understand what could be the best perfomance setup for an inference enterprise environment at scale.

For the load I used [JMeter tool](https://jmeter.apache.org/).

First of all, from the official TorchServe they declare that TorchServe is production ready.
> TorchServe can be used for many types of inference in production settings.

# Tests
## Local development
Even if could not give an interesting contribution for running inference at scale, this was my starting point.\
I tested the serving of [SamLowe/roberta-base-go_emotions](SamLowe_roberta-base-go_emotions) model from HuggingFace  incresing the parallel users as below:
* 15
* 30
* 60

I did exactly the same test using both devices of my PC:
* Intel(R) Core(TM) i7-4710HQ CPU @ 2.50GHz
* NVIDIA GeForce GTX 850M

In conclusion:
* 15 parallel users were faster on GPU than CPU by on avarage the 130%
* 30 parallel users were faster on GPU than CPU by on avarage the 160%
* 60 parallel users were faster on GPU than CPU by on avarage the 80%



Below the avarage response time graphs.

### Using CPU
#### 15 users
<img src=JMeter/results/local/SamLowe_roberta-base-go_emotions/CPU/Response%20Time%20Graph-15users.png>

#### 30 users
<img src=JMeter/results/local/SamLowe_roberta-base-go_emotions/CPU/Response%20Time%20Graph-30users.png>

#### 60 users
<img src=JMeter/results/local/SamLowe_roberta-base-go_emotions/CPU/Response%20Time%20Graph-60users.png>

### Using GPU
#### 15 users
<img src=JMeter/results/local/SamLowe_roberta-base-go_emotions/GPU/Response%20Time%20Graph-15users.png>

#### 30 users
<img src=JMeter/results/local/SamLowe_roberta-base-go_emotions/GPU/Response%20Time%20Graph-30users.png>

#### 60 users
<img src=JMeter/results/local/SamLowe_roberta-base-go_emotions/GPU/Response%20Time%20Graph-60users.png>

## Kubernetes
{
  "code": 503,
  "type": "ServiceUnavailableException",
  "message": "Model \"SamLowe_roberta-base-go_emotions\" has no worker to serve inference request. Please use scale workers API to add workers."
}


# Useful links
* TorchServe configurations
https://pytorch.org/serve/configuration.html
* hp official Doc https://pytorch.org/serve/
* `nvtop` like `htop` but for Nvidia GPU

# Setup
## 1. Get HuggingFace models
```
cd source 

git clone https://huggingface.co/SamLowe/roberta-base-go_emotions

git clone https://huggingface.co/nlptown/bert-base-multilingual-uncased-sentiment

git clone https://huggingface.co/facebook/detr-resnet-50

git clone https://huggingface.co/runwayml/stable-diffusion-v1-5

```
## 2. Prepare container image
```
cd model_store

# generate .mar model for nlptown_bert-base-multilingual-uncased-sentiment model
torch-model-archiver -f --model-name "nlptown_bert-base-multilingual-uncased-sentiment" --version 1.0 \
--serialized-file ../source/bert-base-multilingual-uncased-sentiment/pytorch_model.bin \
--extra-files "../source/bert-base-multilingual-uncased-sentiment/config.json,../source/bert-base-multilingual-uncased-sentiment/special_tokens_map.json,../source/bert-base-multilingual-uncased-sentiment/tokenizer_config.json,../source/bert-base-multilingual-uncased-sentiment/vocab.txt" \
--handler "../handlers/transformers_classifier_torchserve_handler.py"

# generate .mar model for SamLowe_roberta-base-go_emotions
torch-model-archiver -f --model-name "SamLowe_roberta-base-go_emotions" --version 1.0 \
--serialized-file ../source/roberta-base-go_emotions/pytorch_model.bin \
--extra-files "../source/roberta-base-go_emotions/config.json,../source/roberta-base-go_emotions/merges.txt,../source/roberta-base-go_emotions/special_tokens_map.json,../source/roberta-base-go_emotions/tokenizer_config.json,../source/roberta-base-go_emotions/tokenizer.json,../source/roberta-base-go_emotions/trainer_state.json,../source/roberta-base-go_emotions/vocab.json" \
--handler "../handlers/transformers_classifier_torchserve_handler.py"

# generate .mar model for facebook_detr-resnet-50
torch-model-archiver -f --model-name "facebook_detr-resnet-50" --version 1.0 \
--serialized-file ../source/detr-resnet-50/pytorch_model.bin \
--extra-files "../source/detr-resnet-50/config.json,,../source/detr-resnet-50/preprocessor_config.json" \
--handler "../handlers/transformers_classifier_torchserve_handler_object_detection.py"

```

## 3. Build container image
```
# note: choose the FROM_IMAGE you prefer

cd docker
# NOTE!!! In order to take the right latest patch of cuda base image, I had to edit build_image
./build_image.sh -t my_base_torchserve:1.0-gpu --gpu --cudaversion cu116

docker build -t my_custom_torchserve:latest-gpu -f docker/Dockerfile --build-arg FROM_IMAGE=my_base_torchserve:1.0-gpu .

```

## 4. Run TorchServe

### docker compose
```
# make sure that config.properties is as you expect

# comment/uncomment docker-compose capabilities GPU based on your needs

# run it
docker compose up -d
```


5. Test it
By default TorchServe exposes 3 ports:
* 8080 for inference
* 8081 for management
* 8082 for metrics

Tip: if you call inference/management service with OPTION method it will come back the swagger json.

```
# basic inference API
curl --location 'http://127.0.0.1:8080/predictions/<modelName>' \
--header 'Content-Type: text/plain' \
--data 'Hi guys, how are you?'
```

### kubernetes
```
cd kubernetes

# customize as you prefer the chart, than
helm upgrade -i torchserve torchserve

# install ndivia-device-plugin
k create ns nvidia-device-plugin
kubectl create cm -n nvidia-device-plugin nvidia-plugin-configs \
    --from-file=config=dp-example-config0.yaml

helm upgrade -i nvdp nvdp/nvidia-device-plugin \
  --namespace nvidia-device-plugin \
  --create-namespace \
  --set config.name=nvidia-plugin-configs \
  --version 0.14.1


```