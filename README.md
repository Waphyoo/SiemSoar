# SiemSoar

┌──(kali㉿DESKTOP-KQAT41L)-[/mnt/c/Users/nonny/OneDrive/Desktop/SiemSoar]
└─$ git clone https://github.com/wazuh/wazuh-docker.git -b v4.12.0

https://documentation.wazuh.com/current/deployment-options/docker/wazuh-container.html

<img width="578" height="149" alt="image" src="https://github.com/user-attachments/assets/6797e567-1403-4bec-914d-3e3286097de8" />


┌──(kali㉿DESKTOP-KQAT41L)-[/mnt/c/Users/nonny/OneDrive/Desktop/SiemSoar/wazuh-docker]
└─$ cd single-node/

┌──(kali㉿DESKTOP-KQAT41L)-[/mnt/c/Users/nonny/OneDrive/Desktop/SiemSoar/wazuh-docker/single-node]
└─$ ls
config  docker-compose.yml  generate-indexer-certs.yml  README.md

┌──(kali㉿DESKTOP-KQAT41L)-[/mnt/c/Users/nonny/OneDrive/Desktop/SiemSoar/wazuh-docker/single-node]
└─$ docker-compose -f generate-indexer-certs.yml run --rm generator

┌──(kali㉿DESKTOP-KQAT41L)-[/mnt/c/Users/nonny/OneDrive/Desktop/SiemSoar/wazuh-docker/single-node]
└─$ docker-compose up -d
