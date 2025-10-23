def nginx_service(client, hostname, params):
    service_name = params.get('name')
    state = params.get('state')

    if state == 'started':
        command = f"sudo -S systemctl start {service_name}"
        action = "démarré"
    elif state == 'stopped':
        command = f"sudo -S systemctl stop {service_name}"
        action = "arrêté"
    else:
        return {
            'success': False,
            'message': f"État '{state}' non reconnu (started/stopped)",
            'stdout': ''
        }

    try:
        stdin, stdout, stderr = client.exec_command(command, get_pty=True)

        sudo_password = params.get('ssh_password')
        if sudo_password:
            stdin.write(sudo_password + '\n')
            stdin.flush()

        exit_code = stdout.channel.recv_exit_status()
        output = stdout.read().decode('utf-8')
        error = stderr.read().decode('utf-8')

        if exit_code == 0:
            print(f"[{hostname}] ✅  Service '{service_name}' {action}")
            return {
                'success': True,
                'message': f"Service '{service_name}' {action}",
                'stdout': output
            }
        else:
            print(f"[{hostname}] ❌  Erreur lors du démarrage du service '{service_name}': {error}")
            return {
                'success': False,
                'message': f"Erreur: {error}",
                'stdout': output
            }
    except Exception as e:
        print(f"[{hostname}] ❌ Exception lors de l'exécution du service: {str(e)}")
        return {
            'success': False,
            'message': f"Exception: {str(e)}",
            'stdout': ''
        }