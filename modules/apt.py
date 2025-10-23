def apt_module(client, hostname, params):

    package_name = params.get('name')
    state = params.get('state')

    if state == 'present':
        command = f"sudo -S apt-get install -y {package_name}"
        action = "installé"
    elif state == 'absent':
        command = f"sudo -S apt-get remove -y {package_name}"
        action = "supprimé"
    else:
        return {
            'success': False,
            'message': f"État '{state}' non reconnu (present/absent)",
            'stdout': ''
        }

    try:
        stdin, stdout, stderr = client.exec_command(command, get_pty=True)

        # Envoyer le mot de passe sudo (récupéré depuis l'inventory)
        sudo_password = params.get('ssh_password')
        stdin.write(sudo_password + '\n')
        stdin.flush()

        # Attendre la fin de l'exécution
        exit_code = stdout.channel.recv_exit_status()
        output = stdout.read().decode('utf-8')
        error = stderr.read().decode('utf-8')

        if exit_code == 0:
            print(f"[{hostname}] ✅  Paquet '{package_name}' {action}")
            return {
                'success': True,
                'message': f"Paquet '{package_name}' {action}",
                'stdout': output
            }
        else:
            print(f"[{hostname}] ❌ Erreur lors de l'installation de '{package_name}': {error}")
            return {
                'success': False,
                'message': f"Erreur: {error}",
                'stdout': output
            }
    except Exception as e:
        print(f"[{hostname}] ❌ Exception lors de l'exécution APT: {str(e)}")
        return {
            'success': False,
            'message': f"Exception: {str(e)}",
            'stdout': ''
        }