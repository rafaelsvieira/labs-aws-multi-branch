#aws cloudformation create-stack \
#        --stack-name codecommit-finances-api \
#        --template-body file://../cloudformation/codecommit/codecommit.yaml \
#        --parameters file://../cloudformation/codecommit/parameters.json

aws cloudformation create-stack \
        --stack-name codepipeline-finances-api-master \
        --template-body file://../cloudformation/codepipeline/codepipeline.yaml \
        --parameters file://../cloudformation/codepipeline/parameters.json
