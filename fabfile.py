from fabric import Connection, Config, task
from invoke import Exit
import getpass

# Name of the git repository
GIT_REPO = 'ubo-atlas'

# Path of the directory
DIR = '/home/projects/%s' % (GIT_REPO)

# Server name
SERVER = 'Fluorine'


@task
def deploy(c):
    sudo_pass = getpass.getpass("Enter your sudo password on %s: " % SERVER)
    config = Config(overrides={'sudo': {'password': sudo_pass}})
    c = Connection(SERVER, config=config)

    # Pull from GitHub
    c.run(
        'bash -c "cd %s && git pull git@github.com:openstate/%s.git"' % (
            DIR,
            GIT_REPO
        )
    )

    # Reload app
    c.run('bash -c "cd %s && touch uwsgi-touch-reload"' % (DIR))
