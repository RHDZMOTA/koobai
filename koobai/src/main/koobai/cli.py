import datetime as dt
from dataclasses import dataclass, field

@dataclass(frozen=True, slots=True)
class CLI:
    now: dt.datetime = field(default_factory=dt.datetime.utcnow)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return

    def reader(self):
        from rhdzmota.ext.streamlit_webapps.runner import Runner

        runner_instance = Runner()
        runner_instance.start_from_function_refname(
            function_name="execute_frontend_entrypoint",
            module_name="koobai.frontend",
        )

