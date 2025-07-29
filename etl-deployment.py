from prefect import flow
from prefect_github.repository import GitHubRepository

# Load GitHub repository block yang sudah kamu buat di Prefect Cloud
github_repository_block = GitHubRepository.load("github-repo")

# Deploy flow dari repositori GitHub
flow.from_source(
    source=github_repository_block,
    entrypoint="etl-main.py:etl_flow",  # nama fungsi di dalam file
).deploy(
    name="university-etl",
    work_pool_name="etl-workers"
)

print("Flow deployed successfully!")