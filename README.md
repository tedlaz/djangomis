# djangomis

A Django based Greek payroll system

# To dockerize it

    docker run -d --mount source=dbfiles,target=/misthodosia/dbfiles -p 8090:8000 --name djangomis tedlaz/misthodosia

On windows the path for wsl2 docker volumes is:

    \\wsl$\docker-desktop-data\version-pack-data\community\docker\volumes
