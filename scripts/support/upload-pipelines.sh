export PYTHONPATH="${PYTHONPATH}:../:./components"

poetry run python ./scripts/support/upload_pipelines.py
