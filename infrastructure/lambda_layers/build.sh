#!/bin/bash
echo "********************"
echo "PWD:$(pwd)"
BASE_PWD=$(pwd)
echo "********************"

# A list of every directory to build.
LAYERS="requests_pydantic markdown"

build_layer_from_requirements () {
	###
	# Function to build a zip file from a given requirements.txt file
	# give the directory with the requirements.txt and it will build a zip
	# with the same name as the directory
	###
	PY_VERSION=3.11
	DOCKER_BUILD_IMAGE="public.ecr.aws/sam/build-python3.11:latest-x86_64"
	LAMBDA_LAYERS_DIR="."
	LAYER_NAME=$1

	#poetry export --only=main --without-hashes -f requirements.txt --output $(LAMBDA_LAYERS_DIR)/requirements.txt

	echo "Processing ${LAYER_NAME}/requirements.txt"
#	pushd ..
#	popd
	echo building

	rm -Rv "${LAYER_NAME}.zip"
	rm -Rv ./python

	echo "** ** ** ** ** ** ** ** ** **"
	echo "LS BASE_PWD"
	ls -lah "${BASE_PWD}"
	echo "** ** ** ** ** ** ** ** ** **"
	echo "LS LAYER_NAME"
	ls -lah "./${LAYER_NAME}"
	echo "** ** ** ** ** ** ** ** ** **"

	echo "* * * * * * * * * * * * * * *"
	docker run  \
		-v "$HOME/.netrc":/root/.netrc:ro \
		-v "${BASE_PWD}":/var/task \
		"${DOCKER_BUILD_IMAGE}" \
		/bin/sh -c "pwd ; echo '/var/task' ; ls -lah /var/task ; echo 'LAMBDA_LAYERS_DIR' ; ls -lah ${LAMBDA_LAYERS_DIR} ; echo '********' ; echo 'LAMBDA_LAYERS_DIR/LAYER_NAME' ; ls -lah ${LAMBDA_LAYERS_DIR}/${LAYER_NAME} ; echo '********' ; pip3 install -U pip && pip3 install -t ${LAMBDA_LAYERS_DIR}/python/lib/python${PY_VERSION}/site-packages/  -r ${LAMBDA_LAYERS_DIR}/${LAYER_NAME}/requirements.txt && exit"
	cd "${LAMBDA_LAYERS_DIR}" && ls -lah && zip -r --exclude="*.swp" --exclude="**__pycache__**" --exclude="**/site-packages/boto3*" --exclude="**/site-packages/botocore*" --exclude="**/venv*" "${LAYER_NAME}.zip" ./python
	echo "* * * * * * * * * * * * * * *"

	echo "Clean UP"
	rm -Rv ./python
}

create_requirements_from_poetry () {
	LAYER_NAME=$1
	pushd "$LAYER_NAME" || exit
	poetry lock
	poetry export -f requirements.txt --output ./requirements.txt
	popd || exit
}

# build the list above
for DIR_NAME in $LAYERS
do
	create_requirements_from_poetry "${DIR_NAME}"
	build_layer_from_requirements "${DIR_NAME}"
done

#
## build the common libraries
#rm -v common.zip
#cd common || exit 1
#zip -r --exclude="*.swp" --exclude="**__pycache__**" --exclude="**/venv*" ../common.zip ./python
#cd ..
#
#ls -lah
#echo "build complete"
#exit 0
