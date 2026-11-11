from managed_deepagents import define_browser

# A managed browser: adds browser_snapshot, browser_run, browser_screenshot, and
# browser_handoff. Must live at the project root (not in browser/ or sandbox/).
# "thread" = one browser per conversation; "user" would share logins across a user's threads.
browser = define_browser(
    scope="thread",
    idle_ttl_seconds=600,
)
