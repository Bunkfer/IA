# Git / GitHub - Guía rápida

## 1. Configuración inicial de Git

Configurar el usuario que aparecerá en los commits:

```bash
git config --global user.name "USUARIO"
git config --global user.email "correo@ejemplo.com"
```

Comprobar:

```bash
git config --global --list
```

---

# SSH

Recomendado para equipos donde la red permita conexión SSH con GitHub.

## Crear llave SSH

```bash
ssh-keygen -t ed25519 -C "correo@ejemplo.com"
```

La llave pública estará en:

```text
~/.ssh/id_ed25519.pub
```

Mostrarla:

```bash
cat ~/.ssh/id_ed25519.pub
```

Agregar la llave pública en:

**GitHub → Settings → SSH and GPG keys → New SSH key**

Probar conexión:

```bash
ssh -T git@github.com
```

## Clonar con SSH

```bash
git clone git@github.com:USUARIO/REPOSITORIO.git
```

Ejemplo:

```bash
git clone git@github.com:Bunkfer/IA.git
```

---

# HTTPS

Útil en redes corporativas donde SSH esté bloqueado y el acceso a Internet sea mediante proxy.

## Configurar proxy temporal en WSL

En Windows CMD, consultar el proxy configurado:

```cmd
echo %HTTP_PROXY%
echo %HTTPS_PROXY%
```

Ejemplo de resultado:

```text
http://SERVIDOR_PROXY:PUERTO
```

Donde:

- `SERVIDOR_PROXY` → nombre o dirección del proxy.
- `PUERTO` → puerto utilizado por el proxy.

Configurar temporalmente en WSL:

```bash
export HTTP_PROXY=http://SERVIDOR_PROXY:PUERTO
export HTTPS_PROXY=http://SERVIDOR_PROXY:PUERTO
export http_proxy=$HTTP_PROXY
export https_proxy=$HTTPS_PROXY
```

Comprobar acceso:

```bash
curl -I https://github.com
```

Comprobar acceso de Git al repositorio:

```bash
git ls-remote https://github.com/USUARIO/REPOSITORIO.git
```

## Clonar con HTTPS

```bash
git clone https://github.com/USUARIO/REPOSITORIO.git
```

Para clonar dentro de la carpeta actual:

```bash
git clone https://github.com/Bunkfer/IA.git .
```

---

# Trabajar desde WSL en una carpeta de Windows

Una ruta de Windows:

```text
C:\Users\USUARIO\Desktop\IA
```

se encuentra desde WSL como:

```text
/mnt/c/Users/USUARIO/Desktop/IA
```

Ejemplo:

```bash
cd /mnt/c/Users/USUARIO/Desktop/IA
```

---

# Flujo diario

Antes de comenzar:

```bash
git pull
```

Revisar cambios:

```bash
git status
```

Agregar cambios:

```bash
git add .
```

Crear commit:

```bash
git commit -m "Descripción del cambio"
```

Subir cambios:

```bash
git push
```

Flujo completo:

```bash
git pull
git status
git add .
git commit -m "Descripción del cambio"
git push
```

---

# Comandos útiles

Ver repositorio remoto:

```bash
git remote -v
```

Ver historial:

```bash
git log --oneline
```

Ver último commit:

```bash
git show
```

Ver un commit específico:

```bash
git show HASH
```

Ver rama actual:

```bash
git branch
```

---

# SSH vs HTTPS

| Ambiente | Conexión |
|---|---|
| Laptop personal | SSH |
| Laptop de trabajo / red corporativa | HTTPS + Proxy |

Ambos métodos pueden trabajar sobre el mismo repositorio de GitHub.