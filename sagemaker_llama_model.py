# First, retrieve the LLaMA-3 model URI and deploy it using SageMaker:
#       a. Create a Notebook Instance in SageMaker
#
# Create a new Notebook instance.
#       b. Deploy the LLaMA-3 Model
#
#Use the following code to deploy the LLaMA-3 model:

import sagemaker
from sagemaker import get_execution_role

# Create a SageMaker session
sagemaker_session = sagemaker.Session()

# Get the role
role = get_execution_role()

# Retrieve the container image URI for LLaMA-3
llama3_image_uri = "INSERT_LLAMA3_IMAGE_URI_HERE"

# Create a SageMaker model
llama3_model = sagemaker.model.Model(
    image_uri=llama3_image_uri,
    role=role,
    sagemaker_session=sagemaker_session
)

# Deploy the model
predictor = llama3_model.deploy(instance_type="ml.m5.large", initial_instance_count=1)
