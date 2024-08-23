from rhdzmota.ext.streamlit_webapps.page_view_switcher import PageViewSwitcher

from koobai.frontend.view_chatbox import Chatbox
from koobai.frontend.view_character_panel import CharacterPanel


def execute_frontend_entrypoint():
    # View instance
    view_chatbox = Chatbox()
    view_character_panel = CharacterPanel()
    # Switcher instance
    switcher = PageViewSwitcher.from_page_views(
        switcher_name="koobai",
        page_views=[
            view_character_panel,
            view_chatbox,
        ]
    )
    return switcher.run(
        initial_page_key=view_character_panel.refname
    )

