# checkdoor

This simple Python script is designed to detect malicious bash aliases and functions overriding the `sudo` command (to steal the credentials etc). It can also find fake sudo binaries overriding the real one (whose path is before the real path in $PATH).

In the future, the tool will also check the permissions and ownership of the file.

WARNING  This script DOES NOT guarantee the integrity of the real sudo binary; it only detects third binaries and functions hijacking the command flow. Use an IDS for that.
