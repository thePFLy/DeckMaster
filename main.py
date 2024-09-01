from core.modules import Modules
from core.system import System
from core.api import app
from os import getpid, kill
from signal import SIGTERM

# Variables
module = Modules()
system = System()
module.load()


@app.get(path="/core/list_modules", name="Lister les modules")
async def list_modules():
    """
    Requête permettant de lister tout les modules chargés ou mal-chargés par le core.
    """
    return {
        "modules_ok": module.modules_names(),
        "modules_fail": module.modules_list_error
    }


app.
@app.get(path="/core/informations", name="Informations sur ReDeck")
async def informations():
    """
    Renvoie quelques informations intéressantes sur le projet !
    """
    return {
        "Auteur": system.get_value(key="AUTHOR"),
        "Version": system.get_value(key="VERSION"),
        "Description": system.get_value(key="DESCRIPTION"),
        "Remerciements": system.get_value(key="THANKS"),
        "Github": system.get_value(key="GITHUB")
    }


@app.get(path="/core/restart", name="Redémarrer ReDeck")
async def restart():
    """
    Recherche du PID Python pour kill le process.
    ReDeck étant reglé via systemctl, il est prévu que ce dernier relance ReDeck si le service était innactif !
    """
    return kill(getpid(), SIGTERM)
