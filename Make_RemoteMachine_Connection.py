from netmiko import ConnectHandler


class RemoteMachine:
    default_username = 'linux'
    default_password = 'linux'
    default_machine = 'linux'

    def __init__(self, ip):
        self.username = self.default_username
        self.password = self.default_password
        self.machine = self.default_machine
        self.controller_vm = {'device_type': self.machine, 'ip': ip, 'username': self.username,
                              'password': self.password}
        try:
            self.net_connect = ConnectHandler(**self.controller_vm)
        except Exception as e:
            print(e)
        else:
            print("connection opened to device {}".format(self.controller_vm))

    @property
    def set_ip(self):
        return self.ip

    @set_ip.setter
    def set_ip(self, ip):
        self.ip = ip
        self.controller_vm['ip'] = self.ip

    @property
    def set_password(self):
        return self.password

    @set_password.setter
    def set_password(self, password):
        self.password = password
        self.controller_vm['password'] = self.password

    @property
    def set_username(self):
        return self.username

    @set_username.setter
    def set_username(self, username):
        self.username = username
        self.controller_vm['username'] = self.username

    @property
    def set_machine_type(self):
        return self.machine

    @set_machine_type.setter
    def set_machine_type(self, device_type):
        self.machine = device_type
        self.controller_vm['device_type'] = self.machine

    def close_connection(self):
        self.net_connect.disconnect()

    def open_connection(self):
        try:
            self.net_connect = ConnectHandler(**self.controller_vm)
        except Exception as e:
            print(e)
        else:
            print("New connection opened to device".format(self.controller_vm))
            pass


class MininetVm(RemoteMachine):
    default_username = 'mininet'
    default_password = 'mininet'
    default_machine = 'linux'

    def __init__(self, ip):
        super().__init__(ip)
        self.sudo_pass = 'mininet'

    @property
    def set_sudo_pass(self):
        return self.sudo_pass

    @set_sudo_pass.setter
    def set_sudo_pass(self, password):
        self.sudo_pass = password

    def send_command(self, command, delay=None):
        if delay is None:
            output = self.net_connect.send_command_timing(command)
            if '[sudo] password' in output:
                output = self.net_connect.send_command_timing(self.sudo_pass)
                return output
            return output
        else:
            output = self.net_connect.send_command_timing(command, delay_factor=delay)
            if '[sudo] password' in output:
                output = self.net_connect.send_command_timing(self.sudo_pass, delay_factor=delay)
                return output
            return output

    def clear_mininet_topology(self):
        command = 'sudo mn -c'
        output = self.send_command(command)
        return output


class SdnVM(RemoteMachine):
    default_username = 'sdn'
    default_password = 'sdn'
    default_machine = 'linux'

    def __init__(self, ip):
        super().__init__(ip)
        self.sudo_pass = 'sdn'

    send_command = MininetVm.__dict__["send_command"]
    set_sudo_pass = MininetVm.__dict__["set_sudo_pass"]


class Router(RemoteMachine):
    default_username = 'lab'
    default_password = 'lab123'
    default_machine = 'cisco_ios'

    def __init__(self, ip, router_ios, enable_pass=None):
        self.default_machine = router_ios
        super().__init__(ip)
        if enable_pass is not None:
            self.enable_pass = enable_pass
            self.controller_vm['secret'] = self.enable_pass

    @property
    def set_enable_pass(self):
        return self.enable_pass

    @set_enable_pass.setter
    def set_enable_pass(self, password):
        self.enable_pass = password
        self.controller_vm['secret'] = self.enable_pass



