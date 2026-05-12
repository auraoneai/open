from robotics_reviewkit.rubrics import DEXTERITY_ANCHORS, MANIPULATION_ANCHORS
from robotics_reviewkit.analyzers import summarize_events, intervention_density
from robotics_reviewkit.exporters.lerobot_v2 import export_episode_v2
from robotics_reviewkit.exporters.rlds_streaming import stream_episode

def test_v2_anchors_analyzers_exporters():
    episode={"episode_id":"e","task":"dexterity","synthetic":True,"duration_seconds":60,"event_stream":[{"label":"intervention"},{"label":"success"}],"steps":[{"a":1}]}
    assert DEXTERITY_ANCHORS and MANIPULATION_ANCHORS
    assert summarize_events(episode["event_stream"])["counts"]["intervention"] == 1
    assert intervention_density(episode["event_stream"], 60)["events_per_minute"] == 1
    assert export_episode_v2(episode)["format"] == "lerobot-v2"
    assert list(stream_episode(episode))[0]["step_index"] == 0
