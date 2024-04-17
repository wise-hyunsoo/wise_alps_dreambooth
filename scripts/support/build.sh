export CONTAINER_REPOSITORY=asia-northeast3-docker.pkg.dev/dev-ai-project-357507/kfp-components
PROJECT_NAME=$(poetry run python -c "with open('./pyproject.toml', 'rb') as f: project_toml = __import__('tomli').load(f);print(project_toml['tool']['poetry']['name'])")
export PROJECT_NAME=${PROJECT_NAME}
echo "PROJECT_NAME: ${PROJECT_NAME}"

# Open Docker, only if is not running
if (! docker stats --no-stream ); then
  # On Mac OS this would be the terminal command to launch Docker
  open /Applications/Docker.app

# Wait until Docker daemon is running and has completed initialisation
while (! docker stats --no-stream ); do
  # Docker takes a few seconds to initialize
  echo "Waiting for Docker to launch..."
  sleep 1
done
fi

read -a COMPONENTS <<< $(poetry run python scripts/support/find_containerized_python_components.py 2>&1)
for component in "${COMPONENTS[@]}"
  do
    IFS=,
    set $component
    FILE_NAME=$1
    FILE_ROOT=$2
    IMAGE_NAME_TAG="${3//\{PROJECT_NAME\}/$PROJECT_NAME}"
    # IMAGE_NAME_TAG=$(echo $3 | sed "s/{PROJECT_NAME}/${PROJECT_NAME}/")

    export PYTHONPATH="${PYTHONPATH}:./${FILE_ROOT}"

    echo "FILE_NAME: ${FILE_NAME}"
    echo "FILE_ROOT: ${FILE_ROOT}"
    echo "IMAGE_NAME_TAG: ${IMAGE_NAME_TAG}"

    poetry run kfp components build $FILE_ROOT/ --component-filepattern $FILE_NAME --overwrite-dockerfile --no-build-image

    echo "" >> "$FILE_ROOT/Dockerfile"
    echo "ENV ENVIRONMENT=dev" >> "$FILE_ROOT/Dockerfile"

    docker buildx build --platform linux/amd64 --load --tag $CONTAINER_REPOSITORY/$IMAGE_NAME_TAG $FILE_ROOT/
    rm -f $FILE_ROOT/.dockerignore $FILE_ROOT/Dockerfile $FILE_ROOT/kfp_config.ini $FILE_ROOT/runtime-requirements.txt
  done

echo "@@@@@@@@@@@@@@@ PYTHONPATH: ${PYTHONPATH}"
