import os
import textwrap
from typing import Union, Optional
from dataclasses import dataclass, asdict

import yaml
from ollama import Client

from koobai.templates import Template
from koobai.settings import (
    KOOBAI_OLLAMA_SERVER
)


@dataclass(frozen=True, slots=True)
class CharacterBasics:
    name: str
    age: Union[str, int]
    occupation_headline: str
    education_headline: str

@dataclass(frozen=True, slots=True)
class CharacterAppearance:
    height: Union[str, float]
    build: str
    hair: str
    eyes: str
    clothing_style: str


class LLMOllama:
    ollama_client: Optional[Client] = None

    @classmethod
    def update_ollama_server(cls, url: str):
        cls.ollama_client = Client(host=url)


@dataclass(frozen=True, slots=True)
class Character(LLMOllama):
    slug: str
    basics: CharacterBasics
    appearance: CharacterAppearance
    background: Optional[str] = None
    backstory: Optional[str] = None
    motivations: Optional[str] = None
    personality_traits: Optional[str] = None
    skills: Optional[str] = None
    weaknesses: Optional[str] = None
    overwrite_ollama_server_url: Optional[str] = None
    disable_ollama_client: bool = False

    def __post_init__(self):
        if not self.disable_ollama_client:
            self.update_ollama_server(
                self.overwrite_ollama_server_url or KOOBAI_OLLAMA_SERVER
            )

    @classmethod
    def from_path(cls, dirpath: str) -> 'Character':
        slug = os.path.basename(dirpath)
        # Load the character basics
        character_basics_path = os.path.join(
            dirpath,
            "basics.yaml",
        )
        with open(character_basics_path, "r") as file:
            character_basics = CharacterBasics(
                **yaml.safe_load(file.read())
            )
        # Load the character appearance
        character_appearance_path = os.path.join(
            dirpath,
            "appearance.yaml",
        )
        with open(character_appearance_path, "r") as file:
            character_appearance = CharacterAppearance(
                **yaml.safe_load(file.read())
            )
        # Load the character general context
        character_optionals = {
            key: open(filepath).read()
            for key in [
                "background",
                "backstory",
                "motivations",
                "personality_traits",
                "skills",
                "weaknesses",
            ]
            if os.path.exists(
                filepath := os.path.join(
                    dirpath,
                    f"{key}.txt"
                )
            )
        }
        return cls(
            slug=slug,
            basics=character_basics,
            appearance=character_appearance,
            **character_optionals
        )

    def load_ego(
            self,
            # LLM Configuration
            temperature: float = 1.2,
            top_k: int = 60,
            top_p: float = 0.95,
            # Modelfile additional configs
            basemodel: Optional[str] = None,
            # Invoke ego form the standalone character?
            # The alternative is to add the books as context
            standalone: bool = False,
        ):
        # TODO: Validate if model already exists

        basemodel = basemodel or "llama3.1"
        modelfile = Template.MODELFILE.value.format(
            basemodel=basemodel,
            temperature=temperature,
            top_k=top_k,
            top_p=top_p,
            system_instr=Template.SYSTEM_INSTR.value.format(
                **asdict(self.basics),
                **asdict(self.appearance),
                background=self.background,
                backstory=self.backstory,
                motivations=self.motivations,
                personality_traits=self.personality_traits,
                skills=self.skills,
                weaknesses=self.weaknesses,
            )
        )
        if standalone:
            return self.ollama_client.create(
                model=self.slug,
                modelfile=modelfile
            )
        return 

    def chat(self, message: str, stream: bool = False): 
        return self.ollama_client.chat(
            model=self.slug,
            messages=[
                {
                    "role": "user",
                    "content": message,
                }
            ],
            stream=stream,
        )
