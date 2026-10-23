
from huggingface_hub import create_repo, repo_exists, upload_folder, whoami
from git import Repo
import textwrap
import os


def main(
    repo_id: str,
    directory: str,
    token: str,
    repo_type: str = "space",
    space_sdk: str = "gradio",
    private: bool = False,
    include_readme: bool = False,
    generate_message: bool = False
):
    print("Syncing with Hugging Face Spaces...")

    if "/" not in repo_id:
        # Case namespace is implicit
        username = whoami(token=token)["name"]
        repo_id = f"{username}/{repo_id}"
    print(f"\t- Repo ID: {repo_id}")

    print(f"\t- Directory: {directory}")

    exists = repo_exists(repo_id=repo_id, token=token, repo_type=repo_type)
    if not exists:
        url = create_repo(
            repo_id,
            token=token,
            exist_ok=True,
            repo_type=repo_type,
            space_sdk=space_sdk if repo_type == "space" else None,
            private=private,
        )
        print(f"\t- Repo URL: {url}")

    # Sync folder
    ignore_patterns = ["*.git*", "*README.md*"]
    if include_readme:
        ignore_patterns.remove("*README.md*")
    commit_message = generate_commit_message(generate_message, directory)
    commit_url = upload_folder(
        folder_path=directory,
        repo_id=repo_id,
        repo_type=repo_type,
        token=token,
        commit_message=commit_message,
        ignore_patterns=ignore_patterns
    )
    print(f"\t- Repo synced: {commit_url}")

def generate_commit_message(generate_message: bool, directory: str):
    commit_message = "Synced repo using 'huggingface-sync-action' Github Action"
    if generate_message:
        try:
            repo = Repo(directory, search_parent_directories=True)
            remote_url = repo.remotes.origin.url
            commit_id = repo.head.commit.hexsha
            action_repository = os.getenv("GH_ACTION_REPOSITORY", "Unknown")
            action_ref = os.getenv("GH_ACTION_REF", "Unknown")
            return textwrap.dedent(f"""\
                {commit_message}

                original:
                    - remote: "{remote_url}"
                    - commit: "{commit_id}"
                sync_with_huggingface:
                    - repository: "{action_repository}"
                    - ref: "{action_ref}"
            """)
        except Exception as e:
            print(f"Failed to generate commit message: {e}")
    return commit_message

if __name__ == "__main__":
    from fire import Fire

    Fire(main)
