# create lambda layers

    pip install --target ./python pydantic
    zip -r layer_name.zip python

## updated create with docker

update requirements.txt

    docker run -v "$PWD":/var/task "public.ecr.aws/sam/build-python3.11" /bin/sh -c "pip install -t python/lib/python3.11/site-packages/  -r requirements.txt  ; exit"
    zip -r layer_name.zip python
    rm -R python
