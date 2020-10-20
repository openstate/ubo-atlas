# UBO Atlas
Website showing how transparant the implementations of the Ultimate Beneficial Owners (UBO) registers of all EU country are.


## Requirements
[Docker Compose](https://docs.docker.com/compose/install/)

## Run
- Clone or download this project from GitHub:
- Copy `config.py.example` to `config.py` and edit it
   - Create a SECRET_KEY as per the instructions in the file
- Production
   - `cd docker`
   - `sudo docker-compose up -d`
- Development; Flask debug will be turned on which automatically reloads any changes made to Flask files so you don't have to restart the whole application manually
   - `cd docker`
   - `docker-compose -f docker-compose.yml -f docker-compose-dev.yml up -d`
   - Retrieve the IP address of the nginx container `docker inspect ubo_nginx_1` and add it to your hosts file `/etc/hosts`: `<IP_address> uboatlas.eu`
- Useful commands
   - Remove and rebuild everything
      - Production: `docker-compose down --rmi all && docker-compose up -d`
      - Development: `docker-compose -f docker-compose.yml -f docker-compose-dev.yml down --rmi all && docker-compose -f docker-compose.yml -f docker-compose-dev.yml up -d`
   - Reload Nginx: `sudo docker exec ubo_nginx_1 nginx -s reload`
   - Reload uWSGI (only for production as development environment doesn't use uWSGI and automatically reloads changes): `sudo touch uwsgi-touch-reload`
