from invoke import run
from fabric import task
from patchwork.transfers import rsync

exclude_dirs = [".git", "node_modules", ".cache", ".github", "db.sqlite3",
                'local.db', 'htmlcov', ".env"]


@task
def test(c):
    run("pytest  --cov")
    run("coverage html")

@task
def compile(c):
    run("pip-compile requirements.in -o requirements.txt")

@task
def deploy(ctx):
    run("yarn install", echo=True)
    run("yarn run build", echo=True)
    run("find . -name '__pycache__' |xargs rm -rf ", echo=True)
    rsync(ctx, ".", "apps/github_list", exclude=exclude_dirs)
    with ctx.cd("apps/github_list"):
        with ctx.prefix("source ~/apps/spy_agency/.env/bin/activate"):
            ctx.run("pip install -r requirements.txt")
            ctx.run("python seed.py")
    ctx.run("sudo supervisorctl restart gihub_list")

