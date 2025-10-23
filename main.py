import paramiko
import yaml

with open('todos.yml', 'r') as file:
    todos = yaml.safe_load(file)

with open('inventory.yml', 'r') as file:
    inventory = yaml.safe_load(file)

local_file_path = './text.txt'
remote_file_path = './Downloads/text.txt'

command = 'cat ./Downloads/text.txt'


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
    sftp = client.open_sftp()
    print("Connexion réussie au serveur Debian!")
    print(f"Connecté à {client.get_transport().getpeername()}")

    sftp.put(local_file_path, remote_file_path)
    stdin, stdout, stderr = client.exec_command(command)
    print("result", stdout.read())
    sftp.close()
    client.close()
except paramiko.AuthenticationException:
    print("Erreur: Authentification échouée (mauvais username/password)")
except paramiko.SSHException as e:
    print(f"Erreur SSH: {e}")
except Exception as e:
    print(f"Erreur de connexion: {e}")


