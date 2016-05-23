# OSTP - Openvpn SSH TOTP Project

Inspired by [totp-ssh-fluxer](https://github.com/benjojo/totp-ssh-fluxer/), this is a small script that allows me to access any host on my openvpn network from anywhere in the world as long as I have my phone

Meant to be installed to /opt/ostp/, or at least create the directory. To get them on your phone just copy the contents of the proper .url file to [this site](http://goqr.me/) and point your authenticator app in the general direction of the QR code it generates.

Depends on iptables, probably conflicts with ufw. Because the redirection is done in PREROUTING, established connections won't be affected when the code changes
