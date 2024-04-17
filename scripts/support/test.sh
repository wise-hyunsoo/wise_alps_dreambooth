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

poetry run pytest .
