import os
import re

# WARNING: This pattern is not robust. It will fail if the target_image is not matched the below in the decorator.
TARGET_IMAGE_NAME_TAG_PATTERN = re.compile(
    r"target_image=f\"{CONTAINER_REPOSITORY}/(.*?)\""
)


def find_target_image_name_tag(file_path: bytes):
    with open(file_path) as f:
        read = f.read()
        match = TARGET_IMAGE_NAME_TAG_PATTERN.search(read)
        if match:
            return match.group(1)


def find_python_files(path):
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(".py"):
                yield root, file


def find_containerized_python_components():
    for file_root, file_name in find_python_files("components"):
        path = os.path.join(file_root, file_name)
        target_image_name_tag = find_target_image_name_tag(path)
        if target_image_name_tag:
            yield f"{file_name},{file_root},{target_image_name_tag}"


components = [component for component in list(find_containerized_python_components())]

print(" ".join(components))
