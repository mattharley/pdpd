# [obsolete] create lambda layers

    pip install --target ./python pydantic
    zip -r layer_name.zip python

## Preferred method: create lambda layers with docker

update requirements.txt

    docker run -v "$PWD":/var/task "public.ecr.aws/sam/build-python3.11" /bin/sh -c "pip install -t python/lib/python3.11/site-packages/  -r requirements.txt  ; exit"
    zip -r --exclude="*.swp" --exclude=**__pycache__** --exclude="boto3*" --exclude="botocore*" --exclude="/venv*" layer_name.zip python 
    rm -R python
