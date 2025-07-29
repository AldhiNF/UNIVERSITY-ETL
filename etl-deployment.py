from prefect.deployments import Deployment
from prefect_github.repository import GitHubRepository

deployment = Deployment.build_from_source(
    name="UNIVERSITY-ETL",
    flow_name="etl_flow",
    source=GitHubRepository.load("github-repository-univ"),
    entrypoint="etl-main.py:etl_flow",
    work_pool_name="etl-workers"
)

deployment.apply()

print("✅ Flow deployed successfully!")