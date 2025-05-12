from openai import OpenAI

def get_models(base_urls):
    """This function retrieves the models from the specified base URLs. It is not used in the main application because it adds complexity. It is meant to be used for testing purposes via the CLI."""
    models_db = []

    for base_url in base_urls:
        client = OpenAI(base_url=base_url)
        models = client.models.list()

        for model in models:
            # Specifically for Jan
            if "127.0.0.1" in base_url:
                if "status" in model.dict().keys():
                    if model.status == "downloaded":
                        models_db.append(
                            {
                                "id": model.model,
                                "name": model.model,
                                "base_url": base_url,
                            }
                        )
            
            # Speificially for OpenAI
            if 'openai' in base_url:
                models_db.append(
                    {
                        "id": model.id,
                        "name": model.id,
                        "base_url": base_url,
                    }
                )

    return models_db