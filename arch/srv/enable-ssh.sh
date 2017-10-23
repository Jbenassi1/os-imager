#!/usr/bin/env bash

PASSWORD=$(/usr/bin/openssl passwd -crypt 'salt')

echo "==> Enabling SSH"
# salt-specific configuration
/usr/bin/useradd --password ${PASSWORD} --comment 'Salt User' --create-home --user-group salt
echo 'Defaults env_keep += "SSH_AUTH_SOCK"' > /etc/sudoers.d/10_salt
echo 'salt ALL=(ALL) NOPASSWD: ALL' >> /etc/sudoers.d/10_salt
/usr/bin/chmod 0440 /etc/sudoers.d/10_salt
/usr/bin/systemctl start sshd.service
