import argparse


def main():
    parser = argparse.ArgumentParser(
        description="A basic CLI."
    )

    parser.add_argument(
        "command", choices=["train", "run", "listmodels"], help="Command to execute"
    )

    args = parser.parse_args()

    if args.command == "train":
        from backend.ngram.train import train
        train('src/backend/ngram/documents')

    if args.command == "run":
        from backend.api.api import run
        run()

    if args.command == "listmodels":
        from backend.api.models import get_models

        base_urls = ["http://127.0.0.1:4444/v1", "https://api.openai.com/v1"]
        models = get_models(base_urls=base_urls)
        for model in models:
            print(model)

if __name__ == "__main__":
    main()