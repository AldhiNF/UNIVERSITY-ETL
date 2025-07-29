from prefect import flow
from prefect.deployments import Deployment
from prefect_github.repository import GitHubRepository

# Load GitHub repository block yang sudah dibuat di Prefect Cloud
github_repository_block = GitHubRepository.load("github-repository-univ")

# Buat deployment dari source GitHub
deployment = Deployment.build_from_source(
    name="UNIVERSITY-ETL",
    flow_name="etl_flow",  # nama fungsi flow kamu
    source=github_repository_block,
    entrypoint="main.py:run_pipeline",  # file dan fungsi flow
    work_pool_name="etl-workers",
)

# Simpan deployment
deployment.apply()

print("Flow deployed successfully!")