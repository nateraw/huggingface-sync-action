from pathlib import Path
from huggingface_hub import upload_file, create_repo

def main(
    repo_id,
    directory,
    token,
):
    print("Syncing with Hugging Face Spaces...")
    print(f"\t- Repo ID: {repo_id}")
    print(f"\t- Directory: {directory}")
    url = create_repo(repo_id, token=token, exist_ok=True)
    print(f"\t- Repo URL: {url}")
    for filepath in Path(directory).glob("*"):
        if filepath.is_file() and filepath.suffix in ['.py', '.txt']:
            print("\t\t- Uploading", filepath)
            upload_file(
                path_or_fileobj=str(filepath),
                path_in_repo=filepath.name,
                token=token,
                repo_id=repo_id,
            )
        else:
            print("\t\t- Skipping", filepath)

if __name__ == "__main__":
    from fire import Fire

    Fire(main)
