from huggingface_hub import create_repo, upload_folder, whoami


def main(
    repo_id: str,
    directory: str,
    token: str,
    repo_type: str = "space",
    space_sdk: str = "gradio",
    private: bool = False,
):
    print("Syncing with Hugging Face Spaces...")

    if "/" not in repo_id:
        # Case namespace is implicit
        username = whoami(token=token)["name"]
        repo_id = f"{username}/{repo_id}"
    print(f"\t- Repo ID: {repo_id}")

    print(f"\t- Directory: {directory}")
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
    commit_url = upload_folder(
        folder_path=directory,
        repo_id=repo_id,
        repo_type=repo_type,
        token=token,
        commit_message="Synced repo using 'sync_with_huggingface' Github Action",
        ignore_patterns=["*.git*", "*README.md*"],
    )
    print(f"\t- Repo synced: {commit_url}")


if __name__ == "__main__":
    from fire import Fire

    Fire(main)
