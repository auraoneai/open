def stream_episode(episode):
    for index, step in enumerate(episode.get('steps', [])):
        yield {"episode_id": episode.get('episode_id'), "step_index": index, "step": step, "synthetic": episode.get('synthetic', True)}
