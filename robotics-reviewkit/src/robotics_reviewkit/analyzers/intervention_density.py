def intervention_density(events, duration_seconds):
    interventions=sum(1 for e in events if e.get('label') == 'intervention')
    minutes=max(duration_seconds / 60, 1e-9)
    return {"interventions": interventions, "duration_minutes": minutes, "events_per_minute": interventions / minutes}
def per_task_density(episodes):
    out={}
    for ep in episodes:
        task=ep.get('task','unknown'); density=intervention_density(ep.get('event_stream', []), ep.get('duration_seconds', 60))['events_per_minute']
        out.setdefault(task, []).append(density)
    return {task: sum(vals)/len(vals) for task, vals in out.items()}
