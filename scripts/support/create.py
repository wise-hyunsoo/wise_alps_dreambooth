import re

from jinja2 import Template

PIPELINE_ENUM_PATH = "pipelines/support/pipelines.py"
NAME_PATTERN = re.compile(r"^[a-z][a-z0-9_]*$")


def create_file(template, output, **kwargs):
    with open(template) as tf:
        template = Template(tf.read())
        with open(output, "w") as f:
            f.write(template.render(**kwargs))


def create_component(component_name):
    if not NAME_PATTERN.match(component_name):
        print(
            "Component name must be in snake_case and start with a letter. Please try again."
        )
        return

    template = "scripts/support/templates/component.py.jinja2"
    output = f"components/{component_name}.py"
    create_file(
        template,
        output,
        component_name=component_name,
    )

    print("Component created successfully! 🎉")
    print("You can find it here: ", output)


def create_pipeline(pipeline_name):
    if not len(pipeline_name) >= 4:
        print("Pipeline name must be at least 4 characters long. Please try again.")
        return

    if not NAME_PATTERN.match(pipeline_name):
        print(
            "Pipeline name must be in snake_case and start with a letter. Please try again."
        )
        return

    template = "scripts/support/templates/pipeline.py.jinja2"
    output = f"pipelines/{pipeline_name}.py"
    create_file(
        template,
        output,
        pipeline_name=pipeline_name,
    )

    import_template = Template(
        "from pipelines.{{pipeline_name}} import {{pipeline_name}}"
    )
    import_statement = import_template.render(
        {
            "pipeline_name": pipeline_name,
        }
    )

    enum_member_template = Template(
        '    {{PIPELINE_NAME}} = ({{pipeline_name}}, "{{pipeline_name_kebab_case}}.yaml")'
    )
    enum_member_statement = enum_member_template.render(
        {
            "pipeline_name": pipeline_name,
            "pipeline_name_kebab_case": pipeline_name.replace("_", "-"),
            "PIPELINE_NAME": pipeline_name.upper(),
        }
    )

    with open(PIPELINE_ENUM_PATH, "r") as original:
        original_data = original.read()
        with open(PIPELINE_ENUM_PATH, "w") as modified:
            modified.write(
                f"{import_statement}"
                + "\n"
                + original_data
                + enum_member_statement
                + "\n"
            )

    print("Pipeline created successfully! 🎉")
    print("You can find it here: ", output)
