from prefect.filesystems import GitHub
from prefect.deployments import Deployment


github_block = GitHub.load("zoom")

github_dep = Deployment.build_from_flow(
    flow=etl_web_to_gcs,
    name="github-flow",
    infrastructure=github_block,
)

if __name__ == "__main__":
    github_dep.apply()