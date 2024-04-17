export CONTAINER_REPOSITORY=asia-northeast3-docker.pkg.dev/dev-ai-project-357507/kfp-components
PROJECT_NAME=$(poetry run python -c "with open('./pyproject.toml', 'rb') as f: project_toml = __import__('tomli').load(f);print(project_toml['tool']['poetry']['name'])")
export PROJECT_NAME=${PROJECT_NAME}
echo "PROJECT_NAME: ${PROJECT_NAME}"

export PYTHONPATH="${PYTHONPATH}:../:./components"
read -a COMPONENTS <<< $(poetry run python scripts/support/find_containerized_python_components.py 2>&1)
for component in "${COMPONENTS[@]}"
  do
    IFS=,
    set $component
    FILE_ROOT=$2
    export PYTHONPATH="${PYTHONPATH}:./${FILE_ROOT}"
  done

echo "@@@@@@@@@@@@@@@ PYTHONPATH: ${PYTHONPATH}"

mkdir -p pipelines/compiled
poetry run python ./scripts/support/compile.py
