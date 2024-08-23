import os
import enum


class TemplateHelper:
    basepath: str = os.path.dirname(__file__)

    @classmethod
    def ls(cls):
        return [
            file for file in os.listdir(cls.basepath)
            if file.endswith(".txt")
        ]

    @classmethod
    def get(cls, filename: str) -> str:
        if filename not in cls.ls():
            raise ValueError(f"File not found: {filename}")
        filepath = os.path.join(cls.basepath, filename)
        with open(filepath, "r") as file:
            return file.read()


class Template(enum.Enum):
    MODELFILE = TemplateHelper.get(filename="modelfile.txt")
    SYSTEM_INSTR = TemplateHelper.get(filename="system_instr.txt")
