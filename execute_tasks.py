import paramiko
import yaml
import logging
from modules import apt_module, nginx_service

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

logger = logging.getLogger('main')
logging.getLogger('paramiko').setLevel(logging.WARNING)

with open('todos.yml', 'r') as file:
    todos = yaml.safe_load(file)

with open('inventory.yml', 'r') as file:
    inventory = yaml.safe_load(file)

MODULES = {
    'apt': apt_module,
    'service': nginx_service,
}

task_success = 0
task_total = len(todos)

try:
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    host_config = inventory['hosts']['webserver']

    client.connect(
        username=host_config['identifier']['ssh_user'],
        password=host_config['identifier']['ssh_password'],
        hostname=host_config['ssh_address'],
        port=host_config['ssh_port']
    )
    logger.info(f"Connexion à webserver ({host_config['ssh_address']}:{host_config['ssh_port']})")

    for task in todos:
        module_name = task['module']
        module_func = MODULES.get(module_name)

        if module_func:
            task['params']['ssh_password'] = host_config['identifier']['ssh_password']

            result = module_func(client, 'webserver', task['params'])

            if result and result.get('success'):
                task_success += 1
        else:
            print(f"[webserver] ⚠️ Module '{module_name}' non implémenté")

    logger.info(f"Fin de traitement pour webserver")
    print(f"\nRésumé :")
    print(f"✅  webserver : {task_success} tâches réussies / {task_total}")

    client.close()
except paramiko.AuthenticationException:
    print("Erreur: Authentification échouée (mauvais username/password)")
except paramiko.SSHException as e:
    print(f"Erreur SSH: {e}")
except Exception as e:
    print(f"Erreur de connexion: {e}")


