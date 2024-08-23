import os
import textwrap
from typing import Optional

import streamlit as st
from rhdzmota.ext.streamlit_webapps.page_view import PageView

from koobai.models.character import Character
from koobai.frontend.view_chatbox import Chatbox
from koobai.settings import (
    KOOBAI_CHARACTER_CONFIG_BASEPATH
)


class CharacterPanel(PageView):
    
    def characters(self, basepath: Optional[str] = None):
        basepath = basepath or KOOBAI_CHARACTER_CONFIG_BASEPATH
        return [
            dirpath
            for dirname in os.listdir(basepath)
            if (
                "cookiecutter" not in dirname and
                "undefined" not in dirname and
                os.path.isdir(dirpath := os.path.join(basepath, dirname))
            )
        ]

    def character_panel(
            self,
            ncols: int,
            row_container_height: int = 350,
        ):
        characters = self.characters()
        total_characters = len(characters)
        for i in range(round(0.5 + total_characters / ncols)):
            #with st.container(height=row_container_height):
            for j, col in enumerate(st.columns(ncols)):
                index = i * ncols + j
                if index >= total_characters:
                    break
                tile = col.container(height=row_container_height)
                character_dirpath = characters[index]
                character_slug = os.path.basename(character_dirpath)
                profile = os.path.join(character_dirpath, "profile.png")
                if tile.button(f"Chat with: {character_slug}", key=f"chat-with-{character_slug}"):
                    with st.spinner("Loading chatbox..."):
                        self.forward(
                            Chatbox.refname,
                            character_dirpath=character_dirpath,
                        )
                if os.path.exists(profile):
                    tile.image(profile, use_column_width=True)
                else:
                    tile.markdown(
                        textwrap.dedent(
                            f"""
                            #### {character_slug}
                            _Undefined Profile_
                            """
                        )
                    )

    def view(self):
        st.markdown("# Character Panel")

        self.character_panel(
            ncols=3,
            row_container_height=350,
        )

