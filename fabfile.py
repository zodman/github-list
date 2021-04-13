from invoke import run
from fabric import task


@task
def test(c):
    run("pytest  --cov")
    run("coverage html")
