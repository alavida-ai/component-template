import os

import inngest

COMPONENT_NAME = os.getenv("COMPONENT_NAME", "component")

inngest_client = inngest.Inngest(
    app_id=COMPONENT_NAME,
    event_key=os.getenv("INNGEST_EVENT_KEY"),
)
