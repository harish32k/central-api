# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START aiplatform_predict_custom_trained_model_sample]
from typing import Dict, List, Union
from google.cloud import aiplatform
from google.protobuf import json_format
from google.protobuf.struct_pb2 import Value
from utils.get_api import get_endpoint
import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.path.join('tokens', 'aiServiceAccountKey.json')



def predict_custom_trained_model_sample(
    project: str,
    endpoint_id: str,
    instances: Union[Dict, List[Dict]],
    location: str = "us-west1",
    api_endpoint: str = "us-west1-aiplatform.googleapis.com",
):
    """
    `instances` can be either single instance of type dict or a list
    of instances.
    """
    # The AI Platform services require regional API endpoints.
    client_options = {"api_endpoint": api_endpoint}
    # Initialize client that will be used to create and send requests.
    # This client only needs to be created once, and can be reused for multiple requests.
    client = aiplatform.gapic.PredictionServiceClient(client_options=client_options)
    # The format of each instance should conform to the deployed model's prediction input schema.
    instances = instances if type(instances) == list else [instances]
    instances = [
        json_format.ParseDict(instance_dict, Value()) for instance_dict in instances
    ]
    parameters_dict = {}
    parameters = json_format.ParseDict(parameters_dict, Value())
    endpoint = client.endpoint_path(
        project=project, location=location, endpoint=endpoint_id
    )
    response = client.predict(
        endpoint=endpoint, instances=instances, parameters=parameters
    )
    print("response")
    print(" deployed_model_id:", response.deployed_model_id)
    # The predictions are a google.protobuf.Value representation of the model's predictions.
    predictions = response.predictions
    #for prediction in predictions:
    #    print(" prediction:", dict(prediction))

    return predictions

def post_process(results, task):
    if task == "object":
        u_results = []
        for result in results:
            u_result = dict(result)
            u_detections = []
            for detection in u_result["detections"]:
                u_detections.append(dict(detection))
            u_result["detections"] = u_detections
            u_results.append(u_result)
        return u_results
    elif task == "depth":
        u_results = {}
        for result in results:
            u_result = dict(result)
            key = list(u_result.keys())[0]
            u_results[key] = u_result[key]
        # temp = dict(results[0])
        # k = list(temp.keys())[0]
        # v = str(temp[k])
        # print(k, v[:2])
        return u_results

def call_model(input_data, task):
    model_info = get_endpoint(task)
    if model_info["active"] == "0":
        return None
    # [END aiplatform_predict_custom_trained_model_sample]
        
    results = predict_custom_trained_model_sample(
        project=model_info["project"],
        endpoint_id=model_info["endpoint"],
        location=model_info["location"],
        instances=input_data["instances"]
    )
    processed_results = post_process(results, task)
    return processed_results