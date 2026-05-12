def export_episode_v2(episode):
    return {"format": "lerobot-v2", "episode_id": episode.get("episode_id"), "metadata": {"task": episode.get("task"), "synthetic": episode.get("synthetic", True)}, "steps": episode.get("steps", []), "events": episode.get("event_stream", [])}
