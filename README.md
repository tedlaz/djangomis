# djangomis

A Django based Greek payroll system

# To dockerize it

On the command prompt:

    docker run -d --mount source=dbfiles,target=/misthodosia/dbfiles -p 8090:8000 --name djangomis tedlaz/misthodosia

## Notification

The dbfiles parameter is a permanent volume living in docker volumes path.

On windows the path for wsl2/Ubuntu docker volumes is:

    \\wsl$\docker-desktop-data\version-pack-data\community\docker\volumes
