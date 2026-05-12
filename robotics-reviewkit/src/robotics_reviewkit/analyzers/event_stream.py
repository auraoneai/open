def summarize_events(events):
    counts={}
    for event in events:
        counts[event.get('label','unknown')] = counts.get(event.get('label','unknown'), 0) + 1
    return {"event_count": len(events), "counts": counts, "synthetic": True}
