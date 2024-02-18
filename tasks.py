"""
This is a helper script to build the project.
This task.py is not supposed to be bundled into the finished project and should
only be used to define utility function that would be usefull as a cli function
during development.
"""
import os
import sys
import datetime
import subprocess
from invoke.tasks import task
from pathlib import Path

PROJECT_NAME = "gpt4all"
PYTHON_VERSION = "3.9"
VENV = "venv"
BUILD_INCLUDE = [
    'gpt4all_webapp',
    'ui',
    #'src',
    'templates',
    'version',
    'util',
    #'locale',
]

BUILD_ENTRYPOINT = "dashboard.main:main"
BASE_DIR = Path(__file__).parent
with open(BASE_DIR / 'version', 'r') as f:
    VERSION = f.read()

def get_current_build():
    """
    Used by several functions to get the most recent build.
    """
    build_path = Path("./build/") / f"{PROJECT_NAME}-{VERSION}.pyz"
    if build_path.is_file():
        return build_path
    else:
        sys.exit(f"Die neueste Version {VERSION} wurde noch nicht gebaut. Führe erst 'invoke build' aus.")


@task
def test(c):
    """
    Specify tests to run before packaging.
    """
    c.run("safety check")

@task
def sync(c, skip_compile=False, update=False, dry_run=False):
    """
    Uses the pip-tools functions compile and sync to download the most stable
    dependency configuration for your current system.
    """
    c.run("pip install pip-tools")
    if skip_compile:
        print('skipping compiling ...')
    else:
        print('compiling ...')
        c.run(f"pip-compile requirements/prod.in {'-U' if update else ''} {'-n' if dry_run else ''}")
        c.run(f"pip-compile requirements/dev.in {'-U' if update else ''} {'-n' if dry_run else ''}")
    c.run(f"pip-sync requirements/dev.txt {'-n' if dry_run else ''}")


@task
def build(c):
    """
    Builds the current project with a bundler tool.
    For now it only supports shiv.
    """
    if Path("./build/").is_dir():
        if Path(f"./build/{PROJECT_NAME}-{VERSION}.pyz").is_file():
            response = input(f"Version {VERSION} existiert bereits. Trotzdem bauen und ersetzen? y/n: ")
            if not response == "y":
                print("breche ab")
                return

    print('starte die Tests')
    test(c)

    c.run("rm -rf dist/")

    print("installiere requirements in temporäres Verzeichnis")
    c.run("pip install -r requirements/prod.txt --target dist/ -q")

    c.run(f"cp -r -t dist manage.py {' '.join([dir for dir in BUILD_INCLUDE])}")

    c.run("mkdir -p build")

    print("baue .pyz Datei")
    shiv_path = f"{VENV}/bin/shiv"
    if os.environ.get('USING_DOCKER'):
        shiv_path = "shiv"
    c.run(f"{shiv_path} --site-packages dist --compressed -p '/usr/bin/env python{PYTHON_VERSION}' -o build/{PROJECT_NAME}-{VERSION}.pyz -e {BUILD_ENTRYPOINT}")

    print("räume auf")
    #c.run(f"rm -rf dist/")

    print(f"Version {VERSION} gebaut")


def deploy_to_target(c, target):
    """
    Generic function taking a target and deploying the project to it
    how the deployment works may be adjusted to the current project depending
    on your target system.
    args:
        target (string): ssh target to deploy the bundled project to
    """
    build_path = get_current_build()

    project_path = f"/home/{PROJECT_NAME}/{PROJECT_NAME}"

    print("erstelle build Ordner")
    c.run(f"ssh {target} mkdir -p {project_path}/build")

    print(f"kopiere build {PROJECT_NAME}-{VERSION}.pyz")
    c.run(f"scp {build_path} {target}:{project_path}/build/")

    print("kopiere css/javascript to target")
    c.run(f"scp -r \"{str(BASE_DIR)}/static\" {target}:{project_path}")

    print("erstelle symlink")
    c.run(f"ssh {target} ln -sf {project_path}/build/{PROJECT_NAME}-{VERSION}.pyz {project_path}/{PROJECT_NAME}.pyz")

    print("starte gunicorn service neu")
    c.run(f"ssh {target} systemctl restart {PROJECT_NAME}@gunicorn.service")

    print(f'deployment abgeschlossen {datetime.datetime.now()}')


@task
def deploy_test(c):
    """
    Should be used to deploy the project the target_test defined in .invoke.yml
    """
    user_input = input(f'Möchtest du den build "{PROJECT_NAME}-{VERSION}.pyz" auf dem Test-Server veröffentlichen? Tippe "test": ')
    if user_input == 'test':
        deploy_to_target(c, c['target_test'])
    else:
        print('breche ab')

@task
def deploy_prod(c):
    """
    Should be used to deploy the project the target_prod defined in .invoke.yml
    """
    user_input = input(f'Möchtest du den build "{PROJECT_NAME}-{VERSION}.pyz" auf dem Produktiv-Server veröffentlichen? Tippe "produktiv": ')
    if user_input == 'produktiv':
        deploy_to_target(c, c['target_prod'])
    else:
        print('breche ab')


@task
def create_sphinxdoc(c, module_dir=BASE_DIR):
    """
    Creates a documentation using sphinx but its still WIP.
    """
    print(f"Generate .rst files of {module_dir}")
    c.run(f"sphinx-apidoc -o docs/source/_templates {module_dir}")
    print("build html")
    c.run("sphinx-build -b html docs/source/ docs/build/html")

sys.path.append(__file__)
import tasks

@task
def example_invoke_task(ctx):
    """
    Generates an documentation file of tasks.py. Its experimental, ugly
    and pretty redundant when you have to describe this file in a readme anyway.
    """
    with open(f"{BASE_DIR}/docs/source/invoke.rst", "w") as module_file:
        module_file.write("invoke \n======== \n\n")
        module_file.close()

    tasks_dict = tasks.__dict__
    print(tasks_dict)
    for key in tasks_dict.keys():
        if type(tasks_dict[key]) == type(example_invoke_task):
            #print(key, tasks_dict[key], type(tasks_dict[key]), type(example_invoke_task))
            task_function = tasks_dict[key]
            print(task_function.name)
            name_for_invoke = task_function.name.replace("_", "-")
            help_string = subprocess.check_output(f"inv {name_for_invoke} --help").decode("utf-8")
            with open("docs/source/invoke.rst", "a") as module_file:
                module_file.write(f"| @task \n| **{task_function.name}** \n\n")
                module_file.write(f"{help_string} \n| \n| \n")
                module_file.close()

@task
def create_translation(c, translation="en"):
    """
    Generates file out of translation strings and compiles all available translations.
    args:
        translation (string): language code used by django
    """
    c.run(f"python manage.py makemessages -i venv --locale {translation} --domain django")
    c.run(f"python manage.py compilemessages --locale {translation}")

@task
def create_all_translations(c, ignore=None):
    """
    Generates all translations for a list of language strings.
    """
    supportet_languages = ["en", "de"]
    for lang in supportet_languages:
        create_translation(c, lang)
