import os
from botocore.exceptions import ClientError
from boto3 import client
from json import loads


def exist_stack(name):
    cf_client = client('cloudformation')
    try:
        cf_client.get_stack_policy(StackName=name)
        return True
    except ClientError:
        return False

def create_event():
    global cloudformation_path
    print('Create event')
    stack_name = 'event-codecommit-lambda'

    if exist_stack(stack_name):
        print('Stack already created.')
        return

    template_path = os.path.abspath(os.path.join(cloudformation_path, 'event/codecommit-lambda.yaml'))
    print(template_path)

    with open(template_path, 'r') as output:
        template = output.read()

    cf_client = client('cloudformation')
    cf_client.create_stack(
        StackName=stack_name,
        TemplateBody=template,
        OnFailure='DELETE',
        Capabilities=['CAPABILITY_NAMED_IAM']
    )

def create_codecommit():
    global cloudformation_path
    print('Create codecommit')
    stack_name = 'codecommit-recommendation-book'

    if exist_stack(stack_name):
        print('Stack already created.')
        return

    template_path = os.path.abspath(os.path.join(cloudformation_path, 'codecommit/codecommit.yaml'))
    parameters_path = os.path.abspath(os.path.join(cloudformation_path, 'codecommit/parameters.json'))
    print(template_path)

    with open(parameters_path, 'r') as output:
        parameters = loads(output.read())

    with open(template_path, 'r') as output:
        template = output.read()

    cf_client = client('cloudformation')
    cf_client.create_stack(
        StackName=stack_name,
        TemplateBody=template,
        Parameters=parameters,
        OnFailure='DELETE',
        Capabilities=['CAPABILITY_NAMED_IAM']
    )

def create_codepipeline():
    global cloudformation_path
    print('Create codepipeline')
    stack_name = 'codepipeline-app-master'

    if exist_stack(stack_name):
        print('Stack already created.')
        return

    template_path = os.path.abspath(os.path.join(cloudformation_path, 'codepipeline/codepipeline.yaml'))
    parameters_path = os.path.abspath(os.path.join(cloudformation_path, 'codepipeline/parameters.json'))
    print(template_path)

    with open(parameters_path, 'r') as output:
        parameters = loads(output.read())

    with open(template_path, 'r') as output:
        template = output.read()

    cf_client = client('cloudformation')
    cf_client.create_stack(
        StackName=stack_name,
        TemplateBody=template,
        Parameters=parameters,
        OnFailure='DELETE',
        Capabilities=['CAPABILITY_NAMED_IAM']
    )


if __name__ == "__main__":
    global cloudformation_path
    current_path = os.path.abspath(__file__)
    file_name = __file__.split('/')[-1]
    current_path = current_path.split(file_name)[0]
    cloudformation_path = os.path.join(current_path, '..', 'cloudformation')
    os.chdir(cloudformation_path)
    create_codecommit()
    create_codepipeline()
    create_event()
