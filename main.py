from core.modules import Modules
from core.system import System
from core.api import app, update_swagger
from fastapi.responses import FileResponse, Response
from os import getpid, kill
from signal import SIGTERM
from atexit import register
from sys import modules
from uvicorn import run

# Variables
module = Modules()
system = System()
trad = system.show_traduction


def remove_import_references():
    for module_name in module.list_modules_folder():
        print(f"-> Checking if {module_name} has been loaded...")
        process_modules = module.is_module_imported(module=module_name, log=True)
        if process_modules["response"]:
            print("--> Trying to remove imports...")
            for module_name_process in process_modules["result"]:
                modules.pop(module_name_process)


register(remove_import_references)


@app.get(
    path="/core/load_module",
    name=trad(key="load_module_name"),
    description=trad(key="load_module_desc"),
    tags=["Core"]
)
async def load_module(module_name: str):
    response = module.load(module=module_name)
    update_swagger()
    return response


@app.get(
    path="/core/informations",
    name=trad(key="information_core_name"),
    description=trad(key="information_core_desc"),
    tags=["Core"]
)
async def informations():
    return {
        f"{trad(key='information_core_author')}": system.get_value(key="AUTHOR"),
        f"{trad(key='information_core_version')}": system.get_value(key="VERSION"),
        f"{trad(key='information_core_description')}": system.get_value(key="DESCRIPTION"),
        f"{trad(key='information_core_thanks')}": system.get_value(key="THANKS"),
        "GitHub": system.get_value(key="GITHUB")
    }


@app.get(
    path="/core/restart",
    name=trad(key="restart_name"),
    description=trad(key="restart_desc"),
    tags=["Core"]
)
async def restart():
    remove_import_references()
    return kill(getpid(), SIGTERM)


@app.get(
    path="/core/is_imported",
    name=trad(key="is_imported_name"),
    description=trad(key="is_imported_desc"),
    tags=["Core"]
)
async def is_imported(module_name: str, details: bool = False):
    return module.is_module_imported(module=module_name, log=details)


@app.get(
    path="/core/css",
    name=trad(key="css_name"),
    description=trad(key="css_desc"),
    tags=["Core"]
)
async def get_css(filename: str, module: str = None):
    return Response(content=system.get_css(module=module, filename=filename), media_type="text/css")


@app.get(
    path="/core/html",
    name=trad(key="html_name"),
    description=trad(key="html_desc"),
    tags=["Core"]
)
async def get_css(filename: str, module: str = None):
    return Response(content=system.get_html(module=module, filename=filename), media_type="text/html")


@app.get(
    path="/core/image",
    name=trad(key="image_name"),
    description=trad(key="image_desc"),
    tags=["Core"]
)
async def get_css(filename: str, module: str = None, extention: str = "png"):
    return FileResponse(path=system.get_image(module=module, filename=filename, extention=extention))


run(app=app)
