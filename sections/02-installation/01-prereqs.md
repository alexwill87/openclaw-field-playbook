# 01 - Installation des Prérequis Système

Pour une installation fluide d'OpenClaw sur votre serveur ou VPS Ubuntu, il est essentiel de préparer votre système avec les prérequis nécessaires. Cette section vous guide à travers l'installation de Docker, Redis, Python et leurs dépendances.

## 1. Mettre à jour votre système

Il est toujours recommandé de commencer par mettre à jour les paquets de votre système :

```bash
sudo apt update && sudo apt upgrade -y
```

## 2. Installation de Docker (pour les agents conteneurisés)

OpenClaw utilise Docker pour isoler les agents et leurs environnements. Suivez ces étapes pour installer Docker Engine sur Ubuntu :

1.  **Installer les dépendances requises :**
    ```bash
sudo apt install -y ca-certificates curl gnupg
    ```

2.  **Ajouter la clé GPG officielle de Docker :**
    ```bash
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
    ```

3.  **Ajouter le dépôt Docker aux sources APT :**
    ```bash
echo \
  "deb [arch=\"$(dpkg --print-architecture)\" signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \\
  \"$(. /etc/os-release && echo \"$VERSION_CODENAME\")\" stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
    ```

4.  **Mettre à jour l'index des paquets et installer Docker Engine :**
    ```bash
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
    ```

5.  **Ajouter votre utilisateur au groupe `docker` :**
    Pour que votre utilisateur puisse exécuter des commandes Docker sans `sudo` (recommandé pour OpenClaw), ajoutez-le au groupe `docker`. Remplacez `your-username` par votre nom d'utilisateur (ex: `omar`).
    ```bash
sudo usermod -aG docker your-username
    ```
    **IMPORTANT :** Pour que ce changement prenne effet, vous devrez vous déconnecter et vous reconnecter à votre session SSH, ou redémarrer le démon Docker et votre session OpenClaw Gateway.
    ```bash
newgrp docker # Pour actualiser le groupe dans la session courante
sudo systemctl restart docker # Redémarrer le service Docker
sudo openclaw gateway restart # Redémarrer le gateway OpenClaw pour l'agent
    ```

6.  **Vérifier l'installation de Docker :**
    ```bash
docker run hello-world
    ```

## 3. Installation de Redis (pour le caching et les sessions des agents)

Redis est un magasin de données en mémoire, essentiel pour le caching et la gestion des sessions de nombreux agents. Pour une installation souveraine sur votre VPS :

```bash
sudo apt install -y redis-server
```

Après l'installation, vous pouvez vérifier que Redis tourne :

```bash
sudo systemctl status redis-server
```

## 4. Installation de Python et de son environnement virtuel

OpenClaw et de nombreux agents Python nécessitent un environnement Python bien configuré. Nous recommandons l'utilisation d'un environnement virtuel (`venv`).

1.  **Installer les dépendances Python nécessaires :**
    ```bash
sudo apt install -y python3 python3-pip python3.12-venv python3.12-dev
    ```

2.  **Créer et activer un environnement virtuel (dans le répertoire de votre projet agent) :**
    ```bash
python3 -m venv venv
source venv/bin/activate
    ```

Ces étapes fournissent une base solide pour le déploiement d'OpenClaw et de ses agents sur votre VPS Ubuntu.
