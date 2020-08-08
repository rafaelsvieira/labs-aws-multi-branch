#----------------------------------------------------------------------#
# Lambda for Stack Creation
#----------------------------------------------------------------------#
from boto3 import client
from sys import modules


def referenceCreated(parameters):
    print('Create codepipeline')
    cf_client = client('cloudformation')
    cf_client.create_stack(
        StackName=parameters['stack_name'],
        TemplateURL=parameters['template_path'],
        Parameters=[
            {
                'ParameterKey': 'RepositoryName',
                'ParameterValue': parameters['repository_name'],
                'UsePreviousValue': False
            },
            {
                'ParameterKey': 'BranchName',
                'ParameterValue': parameters['new_branch'],
                'UsePreviousValue': False
            }
        ],
        OnFailure='DELETE',
        Capabilities=['CAPABILITY_NAMED_IAM']
    )

def referenceDeleted(parameters):
    print('Delete codepipeline')
    cf_client = client('cloudformation')
    cf_client.delete_stack(
        StackName=parameters['stack_name']
    )

def referenceUpdated(parameters):
    print('Update codepipeline')
    cloudformation_params=[
        {
            'ParameterKey': 'RepositoryName',
            'UsePreviousValue': True,
        },
        {
            'ParameterKey': 'BranchName',
            'UsePreviousValue': True,
        }
    ]
    cf_client = client('cloudformation')
    cf_client.update_stack(
        StackName=parameters['stack_name'],
        TemplateURL=parameters['template_path'],
        Capabilities=['CAPABILITY_NAMED_IAM'],
        Parameters=cloudformation_params,
    )

def lambda_handler(event, context):
    current_module = modules[__name__]
    parameters = {}
    print(event)
    Region = event['region']
    Account = event['account']
    NewBranch = event['detail']['referenceName']
    parameters['repository_name'] = event['detail']['repositoryName']
    parameters["new_branch"] = event['detail']['referenceName']
    Event = event['detail']['event']
    parameters['template_path']=f'https://cf-template-{Region}-{Account}.s3-{Region}.amazonaws.com/codepipeline.yaml'
    parameters['stack_name']=f'codepipeline-{parameters["repository_name"]}-{NewBranch}'

    print(parameters)

    method = getattr(current_module, Event)

    method(parameters)
