import os
from dataclasses import dataclass
from typing import Optional

import streamlit as st
from rhdzmota.ext.streamlit_webapps.page_view import PageView

from koobai.models.character import Character
from koobai.settings import (
    KOOBAI_DEFAULT_CHARACTER_DIRPATH
)


@dataclass(frozen=True, slots=True)
class ChatboxParams:
    character_dirpath: str

    @property
    def slug(self) -> str:
        return os.path.basename(self.character_dirpath)

    @classmethod
    def default(cls, **overwrite) -> 'ChatboxParams':
        defaults = {
            "character_dirpath": KOOBAI_DEFAULT_CHARACTER_DIRPATH
        }
        return cls(**{**defaults, **overwrite})


class Chatbox(PageView):

    def get_chatbox_params(self, character_dirpath: Optional[str] = None):
        query_params = st.query_params.to_dict()
        return {
            "character_dirpath": character_dirpath or query_params.get(
                "character_dirpath",
                KOOBAI_DEFAULT_CHARACTER_DIRPATH
            )
        }

    def chatbox_setup(self, character_dirpath: Optional[str] = None) -> Character:
        chatbox_params = ChatboxParams.default(**self.get_chatbox_params(character_dirpath=character_dirpath))
        chatbox_slug = chatbox_params.slug
        if chatbox_slug not in st.session_state:
            st.session_state[chatbox_slug] = {
                "messages": [],
                "character": (
                    character := Character.from_path(
                        chatbox_params.character_dirpath,
                    )
                )
            }
            character.load_ego(standalone=True)
        return st.session_state[chatbox_slug]["character"]

    def chatbox_register(
            self,
            character: Character,
            role: str,
            message_content: str,
        ):
        # Register user input in message list
        st.session_state[character.slug]["messages"].append(
            {
                "role": role,
                "content": message_content,
            }
        )
        # Display all messages
        for message in st.session_state[character.slug]["messages"]:
            with st.chat_message("user"):
                st.markdown(message["content"])
            with st.chat_message("assistant"):
                with st.spinner('Loading reply...'):
                    message["reply"] = message.get("reply") or character.chat(
                        message=message["content"],
                        stream=False,
                    )
                st.markdown(message["reply"]["message"]["content"])


    def view(self, character_dirpath: Optional[str] = None):
        character = self.chatbox_setup(character_dirpath=character_dirpath)

        if prompt := st.chat_input("Talk to me!"):
            self.chatbox_register(
                role="user",
                character=character,
                message_content=prompt,
            )
