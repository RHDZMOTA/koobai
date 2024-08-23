import os


KOOBAI_OLLAMA_SERVER = os.environ.get(
    "KOOBAI_OLLAMA_SERVER",
    default="http://localhost:11434",
)

KOOBAI_CHARACTER_CONFIG_BASEPATH = os.environ.get(
    "KOOBAI_CHARACTER_CONFIG_BASEPATH",
    default="./koobai/src/configs/characters",
)

KOOBAI_DEFAULT_CHARACTER_DIRPATH = os.environ.get(
    "KOOBAI_DEFAULT_CHARACTER_DIRPATH",
    default=os.path.join(
        KOOBAI_CHARACTER_CONFIG_BASEPATH,
        "olivia_stroustrup",  # Should we use olivia as default?
    )
)
