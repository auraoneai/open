import { ChangeEvent, DragEvent, KeyboardEvent, useMemo, useRef, useState } from "react";
import teleopFixture from "../../../examples/teleop_review_mock_episode.json";
import v2Fixture from "../../../examples/vla_synthetic_episode_v2.json";
import "./proofline.css";

type JsonRecord = Record<string, any>;
type EventKind = "segment" | "failure" | "intervention" | "contact" | "recovery" | "safety" | "success" | "drift";

type ReviewEvent = {
  id: string;
  time: number;
  endTime?: number;
  kind: EventKind;
  label: string;
  severity: string;
  notes: string;
  path: string;
  segment?: string;
};

type ValidationIssue = {
  path: string;
  message: string;
  fix: string;
};

type Session = {
  id: string;
  task: string;
  version: string;
  dataStatus: "synthetic" | "permissioned";
  duration: number;
  events: ReviewEvent[];
  anchors: Array<{ criterion: string; score: string; label: string }>;
  source: JsonRecord;
  sourceName: string;
  releaseState: string;
  releaseRationale: string;
  sensorFlags: number;
};

const EVENT_KINDS: EventKind[] = [
  "segment",
  "failure",
  "intervention",
  "contact",
  "recovery",
  "safety",
  "success",
  "drift",
];

const KIND_LABELS: Record<EventKind, string> = {
  segment: "Segment",
  failure: "Failure",
  intervention: "Intervention",
  contact: "Contact",
  recovery: "Recovery",
  safety: "Safety",
  success: "Success",
  drift: "Drift",
};

const KIND_SYMBOLS: Record<EventKind, string> = {
  segment: "S",
  failure: "F",
  intervention: "I",
  contact: "C",
  recovery: "R",
  safety: "!",
  success: "OK",
  drift: "D",
};

function objectValue(value: unknown): JsonRecord {
  return value && typeof value === "object" && !Array.isArray(value) ? (value as JsonRecord) : {};
}

function arrayValue(value: unknown): JsonRecord[] {
  return Array.isArray(value) ? value.map(objectValue) : [];
}

function textValue(value: unknown, fallback = ""): string {
  return typeof value === "string" && value.trim() ? value : fallback;
}

function numberValue(value: unknown, fallback = 0): number {
  return typeof value === "number" && Number.isFinite(value) ? value : fallback;
}

function validateSource(source: JsonRecord): ValidationIssue[] {
  const issues: ValidationIssue[] = [];
  const add = (path: string, message: string, fix: string) => issues.push({ path, message, fix });

  if (!textValue(source.episode_id)) {
    add("$.episode_id", "Episode ID is required.", "Add a non-empty episode_id string.");
  }

  if (source.review_version === "v2") {
    if (!textValue(source.task)) add("$.task", "Task is required.", "Add a task string.");
    if (!Array.isArray(source.event_stream)) {
      add("$.event_stream", "Event stream must be an array.", "Add an event_stream array.");
    }
    if (numberValue(source.duration_seconds, -1) <= 0) {
      add("$.duration_seconds", "Duration must be greater than zero.", "Set duration_seconds to the episode duration.");
    }
    arrayValue(source.event_stream).forEach((event, index) => {
      if (!EVENT_KINDS.includes(event.label as EventKind) || event.label === "segment" || event.label === "failure") {
        add(
          `$.event_stream[${index}].label`,
          `Unsupported event label "${textValue(event.label, "(missing)")}".`,
          "Use contact, safety, drift, recovery, intervention, or success.",
        );
      }
      if (numberValue(event.timestamp_s, -1) < 0) {
        add(`$.event_stream[${index}].timestamp_s`, "Timestamp must be zero or greater.", "Set a numeric timestamp_s.");
      }
    });
  } else {
    if (!objectValue(source.task).task_id) {
      add("$.task.task_id", "Teleop task ID is required.", "Add task.task_id from the ReviewKit task library.");
    }
    if (!Array.isArray(source.segments) || source.segments.length === 0) {
      add("$.segments", "At least one segment is required.", "Add an ordered segments array.");
    }
    if (!objectValue(source.timestamps).end_s) {
      add("$.timestamps.end_s", "Episode end time is required.", "Set timestamps.end_s greater than timestamps.start_s.");
    }
    for (const field of ["failure_annotations", "interventions", "sensors"]) {
      if (!Array.isArray(source[field])) add(`$.${field}`, `${field} must be an array.`, `Add a ${field} array, even when empty.`);
    }
  }

  return issues;
}

function normalizeEpisode(source: JsonRecord, sourceName: string): Session {
  if (source.review_version === "v2") {
    const duration = Math.max(numberValue(source.duration_seconds, 1), 1);
    const events = arrayValue(source.event_stream)
      .map((event, index): ReviewEvent => ({
        id: `event-${index}-${numberValue(event.timestamp_s)}`,
        time: numberValue(event.timestamp_s),
        kind: EVENT_KINDS.includes(event.label as EventKind) ? (event.label as EventKind) : "drift",
        label: textValue(event.label, "unlabeled"),
        severity: textValue(event.severity, "info"),
        notes: textValue(event.notes, "No reviewer note."),
        path: `$.event_stream[${index}]`,
      }))
      .sort((a, b) => a.time - b.time);

    return {
      id: textValue(source.episode_id, "unidentified-episode"),
      task: textValue(source.task, "Unspecified task"),
      version: "ReviewKit v2",
      dataStatus: source.synthetic === false ? "permissioned" : "synthetic",
      duration,
      events,
      anchors: arrayValue(source.rubric_anchors).map((anchor) => ({
        criterion: textValue(anchor.criterion_id, "unnamed criterion"),
        score: anchor.score == null ? "Not scored" : String(anchor.score),
        label: textValue(anchor.label, "No anchor label"),
      })),
      source,
      sourceName,
      releaseState: source.synthetic === false ? "Review required" : "Tutorial only",
      releaseRationale:
        source.synthetic === false
          ? "Permissioned data still requires provenance, privacy, and policy review."
          : "Synthetic metadata cannot be released as training data.",
      sensorFlags: 0,
    };
  }

  const timestamps = objectValue(source.timestamps);
  const start = numberValue(timestamps.start_s);
  const end = Math.max(numberValue(timestamps.end_s, 1), start + 1);
  const segments = arrayValue(source.segments).map((segment, index): ReviewEvent => ({
    id: textValue(segment.segment_id, `segment-${index}`),
    time: Math.max(0, numberValue(segment.start_s) - start),
    endTime: Math.max(0, numberValue(segment.end_s) - start),
    kind: "segment",
    label: textValue(segment.phase, "segment"),
    severity: "info",
    notes: textValue(segment.description, "No segment description."),
    path: `$.segments[${index}]`,
    segment: textValue(segment.segment_id),
  }));
  const failures = arrayValue(source.failure_annotations).map((failure, index): ReviewEvent => ({
    id: textValue(failure.failure_id, `failure-${index}`),
    time: Math.max(0, numberValue(failure.start_s) - start),
    endTime: Math.max(0, numberValue(failure.end_s) - start),
    kind: "failure",
    label: textValue(failure.taxonomy_id, "Unclassified failure"),
    severity: textValue(failure.severity, "review"),
    notes: textValue(failure.reviewer_note, "No reviewer note."),
    path: `$.failure_annotations[${index}]`,
    segment: textValue(failure.segment_id),
  }));
  const interventions = arrayValue(source.interventions).map((intervention, index): ReviewEvent => ({
    id: textValue(intervention.intervention_id, `intervention-${index}`),
    time: Math.max(0, numberValue(intervention.start_s) - start),
    endTime: Math.max(0, numberValue(intervention.end_s) - start),
    kind: "intervention",
    label: textValue(intervention.ontology_id, "Unclassified intervention"),
    severity: textValue(intervention.training_relevance, "review"),
    notes: [textValue(intervention.trigger), textValue(intervention.operator_action)].filter(Boolean).join(" "),
    path: `$.interventions[${index}]`,
    segment: textValue(intervention.segment_id),
  }));
  const task = objectValue(source.task);
  const readiness = objectValue(source.training_readiness);

  return {
    id: textValue(source.episode_id, "unidentified-episode"),
    task: textValue(task.name, textValue(task.task_id, "Unspecified task")),
    version: `Teleop ${textValue(source.schema_version, "schema")}`,
    dataStatus: source.data_status === "permissioned_real" ? "permissioned" : "synthetic",
    duration: end - start,
    events: [...segments, ...failures, ...interventions].sort((a, b) => a.time - b.time || a.kind.localeCompare(b.kind)),
    anchors: [],
    source,
    sourceName,
    releaseState: textValue(readiness.state, "Review required").replaceAll("_", " "),
    releaseRationale: textValue(readiness.rationale, "No release rationale provided."),
    sensorFlags: arrayValue(objectValue(source.sensor_qa).flags).length,
  };
}

const BUILT_IN_SESSIONS = [
  normalizeEpisode(teleopFixture, "teleop_review_mock_episode.json"),
  normalizeEpisode(v2Fixture, "vla_synthetic_episode_v2.json"),
];

function parseSource(raw: string, sourceName: string): { session: Session | null; issues: ValidationIssue[] } {
  try {
    const source = objectValue(JSON.parse(raw));
    const issues = validateSource(source);
    return { session: normalizeEpisode(source, sourceName), issues };
  } catch (error) {
    return {
      session: null,
      issues: [
        {
          path: "$",
          message: error instanceof Error ? error.message : "Source is not valid JSON.",
          fix: "Correct the JSON syntax, then review the parsed episode.",
        },
      ],
    };
  }
}

function downloadArtifact(filename: string, content: string, type = "application/json") {
  const url = URL.createObjectURL(new Blob([content], { type }));
  const link = document.createElement("a");
  link.href = url;
  link.download = filename;
  link.click();
  URL.revokeObjectURL(url);
}

function csvCell(value: unknown): string {
  return `"${String(value ?? "").replaceAll('"', '""')}"`;
}

function formatTime(value: number): string {
  return `${value.toFixed(value % 1 ? 1 : 0)}s`;
}

export default function App() {
  const [sessions, setSessions] = useState(BUILT_IN_SESSIONS);
  const [sessionIndex, setSessionIndex] = useState(0);
  const [sourceName, setSourceName] = useState(BUILT_IN_SESSIONS[0].sourceName);
  const [raw, setRaw] = useState(JSON.stringify(BUILT_IN_SESSIONS[0].source, null, 2));
  const [query, setQuery] = useState("");
  const [enabledKinds, setEnabledKinds] = useState<Set<EventKind>>(new Set(EVENT_KINDS));
  const [selectedId, setSelectedId] = useState(BUILT_IN_SESSIONS[0].events[0]?.id ?? "");
  const [zoom, setZoom] = useState(1);
  const [dropActive, setDropActive] = useState(false);
  const fileInput = useRef<HTMLInputElement>(null);
  const parsed = useMemo(() => parseSource(raw, sourceName), [raw, sourceName]);
  const session = parsed.session ?? sessions[sessionIndex];

  const filteredEvents = useMemo(() => {
    const needle = query.trim().toLowerCase();
    return session.events.filter(
      (event) =>
        enabledKinds.has(event.kind) &&
        (!needle ||
          [event.label, event.kind, event.severity, event.notes, event.segment]
            .filter(Boolean)
            .some((value) => String(value).toLowerCase().includes(needle))),
    );
  }, [enabledKinds, query, session.events]);

  const selectedEvent =
    filteredEvents.find((event) => event.id === selectedId) ??
    session.events.find((event) => event.id === selectedId) ??
    filteredEvents[0] ??
    null;
  const interventionCount = session.events.filter((event) => event.kind === "intervention").length;
  const interventionDensity = interventionCount / Math.max(session.duration / 60, 1 / 60);
  const visibleKinds = EVENT_KINDS.filter((kind) => session.events.some((event) => event.kind === kind));

  function selectSession(nextIndex: number) {
    const next = sessions[nextIndex];
    setSessionIndex(nextIndex);
    setSourceName(next.sourceName);
    setRaw(JSON.stringify(next.source, null, 2));
    setSelectedId(next.events[0]?.id ?? "");
    setQuery("");
    setEnabledKinds(new Set(EVENT_KINDS));
  }

  async function loadFile(file: File) {
    const nextRaw = await file.text();
    const result = parseSource(nextRaw, file.name);
    setSourceName(file.name);
    setRaw(nextRaw);
    if (result.session) {
      const nextSessions = [...sessions, result.session];
      setSessions(nextSessions);
      setSessionIndex(nextSessions.length - 1);
      setSelectedId(result.session.events[0]?.id ?? "");
    }
  }

  function handleFile(event: ChangeEvent<HTMLInputElement>) {
    const file = event.target.files?.[0];
    if (file) void loadFile(file);
    event.target.value = "";
  }

  function handleDrop(event: DragEvent<HTMLElement>) {
    event.preventDefault();
    setDropActive(false);
    const file = event.dataTransfer.files?.[0];
    if (file) void loadFile(file);
  }

  function toggleKind(kind: EventKind) {
    setEnabledKinds((current) => {
      const next = new Set(current);
      if (next.has(kind)) next.delete(kind);
      else next.add(kind);
      return next;
    });
  }

  function navigateTimeline(event: KeyboardEvent<HTMLDivElement>) {
    if (!filteredEvents.length) return;
    const currentIndex = Math.max(
      0,
      filteredEvents.findIndex((item) => item.id === selectedEvent?.id),
    );
    let nextIndex = currentIndex;
    if (event.key === "ArrowRight") nextIndex = Math.min(filteredEvents.length - 1, currentIndex + 1);
    else if (event.key === "ArrowLeft") nextIndex = Math.max(0, currentIndex - 1);
    else if (event.key === "Home") nextIndex = 0;
    else if (event.key === "End") nextIndex = filteredEvents.length - 1;
    else if (event.key === "+" || event.key === "=") {
      setZoom((value) => Math.min(4, value + 0.5));
      event.preventDefault();
      return;
    } else if (event.key === "-") {
      setZoom((value) => Math.max(1, value - 0.5));
      event.preventDefault();
      return;
    } else {
      return;
    }
    setSelectedId(filteredEvents[nextIndex].id);
    event.preventDefault();
  }

  function exportNormalized() {
    const payload = {
      artifact: "auraone-reviewkit-evidence",
      artifact_version: "1.0",
      metadata_only: true,
      source_file: session.sourceName,
      episode_id: session.id,
      task: session.task,
      review_version: session.version,
      data_status: session.dataStatus,
      duration_seconds: session.duration,
      release_decision: {
        state: session.releaseState,
        rationale: session.releaseRationale,
      },
      events: session.events,
      limitations: [
        "No sensor payloads, images, actions, or training records are generated by this viewer.",
        "Synthetic fixtures are tutorial metadata and are not training data.",
      ],
    };
    downloadArtifact(`${session.id}-review-evidence.json`, JSON.stringify(payload, null, 2));
  }

  function exportCsv() {
    const header = ["time_s", "end_time_s", "kind", "label", "severity", "segment", "notes", "source_path"];
    const rows = session.events.map((event) =>
      [event.time, event.endTime ?? "", event.kind, event.label, event.severity, event.segment ?? "", event.notes, event.path]
        .map(csvCell)
        .join(","),
    );
    downloadArtifact(`${session.id}-events.csv`, [header.join(","), ...rows].join("\n"), "text/csv");
  }

  function exportLeRobot() {
    const payload = {
      format: "lerobot-v2-metadata-bridge",
      metadata_only: true,
      episode_id: session.id,
      task: session.task,
      review_events: session.events,
      boundary: "Review metadata only. Sensor frames, observations, actions, and training shards are not included.",
    };
    downloadArtifact(`${session.id}-lerobot-metadata.json`, JSON.stringify(payload, null, 2));
  }

  function exportRlds() {
    const records = session.events.map((event, index) =>
      JSON.stringify({
        format: "rlds-openx-review-metadata",
        metadata_only: true,
        episode_id: session.id,
        record_index: index,
        review_event: event,
      }),
    );
    records.push(
      JSON.stringify({
        format: "rlds-openx-review-metadata",
        metadata_only: true,
        episode_id: session.id,
        is_terminal: true,
        boundary: "No RLDS observation/action tensors or media payloads are included.",
      }),
    );
    downloadArtifact(`${session.id}-rlds-openx-metadata.jsonl`, records.join("\n"), "application/x-ndjson");
  }

  return (
    <div
      className={`app-shell${dropActive ? " is-drop-active" : ""}`}
      onDragEnter={(event) => {
        event.preventDefault();
        setDropActive(true);
      }}
      onDragOver={(event) => event.preventDefault()}
      onDragLeave={(event) => {
        if (event.currentTarget === event.target) setDropActive(false);
      }}
      onDrop={handleDrop}
    >
      <a className="skip-link" href="#event-table">
        Skip to event table
      </a>

      <header className="app-header">
        <div className="identity">
          <span className="proof-mark" aria-hidden="true">
            AO
          </span>
          <div>
            <p className="product-label">AuraOne Robotics ReviewKit</p>
            <h1>{session.id}</h1>
            <p className="session-context">
              {session.task} <span aria-hidden="true">/</span> {session.version}
            </p>
          </div>
        </div>
        <div className="header-actions">
          <span className={`status-label status-${session.dataStatus}`}>
            <span aria-hidden="true" className="status-dot" />
            {session.dataStatus === "synthetic" ? "Synthetic metadata" : "Permissioned data"}
          </span>
          <button className="button button-primary" type="button" onClick={() => fileInput.current?.click()}>
            Open JSON
          </button>
          <input ref={fileInput} className="visually-hidden" type="file" accept=".json,application/json" onChange={handleFile} />
        </div>
      </header>

      <div className="disclosure" role="note">
        <strong>Local review:</strong> files stay in this browser. Bundled sessions are synthetic tutorial metadata, not
        expert-reviewed benchmarks or training data.
      </div>

      <main className="workspace">
        <aside className="session-rail" aria-label="Sessions and source">
          <section className="rail-section">
            <div className="section-heading">
              <h2>Sessions</h2>
              <span>{sessions.length}</span>
            </div>
            <div className="session-list">
              {sessions.map((item, index) => (
                <button
                  className={`session-item${index === sessionIndex ? " is-active" : ""}`}
                  type="button"
                  key={`${item.id}-${index}`}
                  onClick={() => selectSession(index)}
                  aria-current={index === sessionIndex ? "page" : undefined}
                >
                  <span className="session-title">{item.id}</span>
                  <span>{item.task}</span>
                  <span className="session-meta">
                    {item.events.length} records / {formatTime(item.duration)}
                  </span>
                </button>
              ))}
            </div>
          </section>

          <section className="rail-section source-section">
            <div className="section-heading">
              <h2>Source JSON</h2>
              <span>{sourceName}</span>
            </div>
            <textarea
              className="source-editor"
              aria-label="Episode source JSON"
              value={raw}
              onChange={(event) => setRaw(event.target.value)}
              spellCheck={false}
            />
            <div className="validation-summary" aria-live="polite">
              <span className={`status-label ${parsed.issues.length ? "status-review" : "status-success"}`}>
                <span aria-hidden="true" className="status-dot" />
                {parsed.issues.length ? `${parsed.issues.length} schema issue${parsed.issues.length === 1 ? "" : "s"}` : "Source ready"}
              </span>
            </div>
            {parsed.issues.length ? (
              <ol className="issue-list">
                {parsed.issues.map((issue, index) => (
                  <li key={`${issue.path}-${index}`}>
                    <code>{issue.path}</code>
                    <strong>{issue.message}</strong>
                    <span>{issue.fix}</span>
                  </li>
                ))}
              </ol>
            ) : null}
          </section>
        </aside>

        <section className="review-canvas" aria-label="Episode review">
          <div className="review-toolbar">
            <label className="search-control">
              <span>Search records</span>
              <input
                type="search"
                value={query}
                onChange={(event) => setQuery(event.target.value)}
                placeholder="Label, note, severity..."
              />
            </label>
            <fieldset className="filter-group">
              <legend>Record types</legend>
              {visibleKinds.map((kind) => (
                <label key={kind} className={`filter-toggle kind-${kind}`}>
                  <input type="checkbox" checked={enabledKinds.has(kind)} onChange={() => toggleKind(kind)} />
                  <span aria-hidden="true">{KIND_SYMBOLS[kind]}</span>
                  {KIND_LABELS[kind]}
                </label>
              ))}
            </fieldset>
          </div>

          <section className="timeline-section" aria-labelledby="timeline-title">
            <div className="section-heading timeline-heading">
              <div>
                <h2 id="timeline-title">Evidence timeline</h2>
                <p>{filteredEvents.length} visible records ordered across {formatTime(session.duration)}</p>
              </div>
              <div className="zoom-control" aria-label="Timeline zoom">
                <button type="button" onClick={() => setZoom((value) => Math.max(1, value - 0.5))} disabled={zoom <= 1} aria-label="Zoom out">
                  -
                </button>
                <output aria-live="polite">{zoom.toFixed(1)}x</output>
                <button type="button" onClick={() => setZoom((value) => Math.min(4, value + 0.5))} disabled={zoom >= 4} aria-label="Zoom in">
                  +
                </button>
              </div>
            </div>
            <p className="keyboard-hint">Use Left/Right, Home/End, and +/- while the timeline is focused.</p>
            <div
              className="timeline-scroll"
              tabIndex={0}
              onKeyDown={navigateTimeline}
              aria-label="Interactive event timeline"
              aria-describedby="timeline-instructions"
            >
              <span id="timeline-instructions" className="visually-hidden">
                Left and right arrow keys select adjacent records. Home and End select the first and last records.
                Plus and minus change timeline zoom.
              </span>
              <div className="timeline-track" style={{ width: `${zoom * 100}%` }}>
                <div className="timeline-axis" aria-hidden="true">
                  {[0, 25, 50, 75, 100].map((percent) => (
                    <span key={percent} style={{ left: `${percent}%` }}>
                      {formatTime((session.duration * percent) / 100)}
                    </span>
                  ))}
                </div>
                {filteredEvents.map((event) => {
                  const left = Math.min(99, Math.max(0, (event.time / session.duration) * 100));
                  const width =
                    event.endTime == null ? undefined : Math.max(1.2, ((event.endTime - event.time) / session.duration) * 100);
                  return (
                    <button
                      type="button"
                      className={`timeline-event kind-${event.kind}${selectedEvent?.id === event.id ? " is-selected" : ""}${
                        width ? " is-range" : ""
                      }`}
                      style={{ left: `${left}%`, width: width ? `${width}%` : undefined }}
                      key={event.id}
                      onClick={() => setSelectedId(event.id)}
                      aria-label={`${KIND_LABELS[event.kind]} ${event.label} at ${formatTime(event.time)}`}
                      title={`${formatTime(event.time)} / ${event.label}`}
                    >
                      <span aria-hidden="true">{KIND_SYMBOLS[event.kind]}</span>
                    </button>
                  );
                })}
              </div>
            </div>
          </section>

          <section className="event-table-section" aria-labelledby="event-table-title">
            <div className="section-heading">
              <div>
                <h2 id="event-table-title">Ordered event record</h2>
                <p>The table is the nonvisual source of truth for timeline content.</p>
              </div>
            </div>
            <div className="table-scroll">
              <table id="event-table">
                <thead>
                  <tr>
                    <th scope="col">Time</th>
                    <th scope="col">Type</th>
                    <th scope="col">Record</th>
                    <th scope="col">Severity</th>
                    <th scope="col">Segment</th>
                  </tr>
                </thead>
                <tbody>
                  {filteredEvents.map((event) => (
                    <tr key={event.id} className={selectedEvent?.id === event.id ? "is-selected" : undefined}>
                      <td>
                        <button type="button" className="table-select" onClick={() => setSelectedId(event.id)}>
                          {formatTime(event.time)}
                        </button>
                      </td>
                      <td>
                        <span className={`event-type kind-${event.kind}`}>
                          <span aria-hidden="true">{KIND_SYMBOLS[event.kind]}</span>
                          {KIND_LABELS[event.kind]}
                        </span>
                      </td>
                      <td>
                        <strong>{event.label}</strong>
                        <span className="table-note">{event.notes}</span>
                      </td>
                      <td>{event.severity.replaceAll("_", " ")}</td>
                      <td>{event.segment || "Episode"}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
              {!filteredEvents.length ? (
                <div className="empty-state">
                  <strong>No matching records</strong>
                  <span>Clear the search or enable another record type.</span>
                </div>
              ) : null}
            </div>
          </section>
        </section>

        <aside className="inspector" aria-label="Selected evidence inspector">
          <section className="inspector-section">
            <p className="section-kicker">Selected evidence</p>
            {selectedEvent ? (
              <>
                <div className="inspector-title">
                  <span className={`event-symbol kind-${selectedEvent.kind}`} aria-hidden="true">
                    {KIND_SYMBOLS[selectedEvent.kind]}
                  </span>
                  <div>
                    <h2>{selectedEvent.label}</h2>
                    <p>
                      {KIND_LABELS[selectedEvent.kind]} at {formatTime(selectedEvent.time)}
                    </p>
                  </div>
                </div>
                <dl className="detail-list">
                  <div>
                    <dt>Severity</dt>
                    <dd>{selectedEvent.severity.replaceAll("_", " ")}</dd>
                  </div>
                  <div>
                    <dt>Segment</dt>
                    <dd>{selectedEvent.segment || "Episode level"}</dd>
                  </div>
                  <div>
                    <dt>Source path</dt>
                    <dd>
                      <code>{selectedEvent.path}</code>
                    </dd>
                  </div>
                </dl>
                <p className="evidence-note">{selectedEvent.notes}</p>
              </>
            ) : (
              <p className="empty-copy">Select an event to inspect its evidence.</p>
            )}
          </section>

          <section className="inspector-section">
            <p className="section-kicker">Review measures</p>
            <dl className="metric-list">
              <div>
                <dt>Intervention density</dt>
                <dd>{interventionDensity.toFixed(2)}/min</dd>
              </div>
              <div>
                <dt>Review records</dt>
                <dd>{session.events.length}</dd>
              </div>
              <div>
                <dt>Sensor QA flags</dt>
                <dd>{session.sensorFlags}</dd>
              </div>
            </dl>
          </section>

          <section className="inspector-section">
            <p className="section-kicker">Rubric anchors</p>
            {session.anchors.length ? (
              <table className="anchor-table">
                <thead>
                  <tr>
                    <th scope="col">Criterion</th>
                    <th scope="col">Score</th>
                  </tr>
                </thead>
                <tbody>
                  {session.anchors.map((anchor) => (
                    <tr key={anchor.criterion}>
                      <td>
                        <strong>{anchor.criterion}</strong>
                        <span>{anchor.label}</span>
                      </td>
                      <td>{anchor.score}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            ) : (
              <p className="empty-copy">This teleop schema uses failure and readiness records instead of v2 rubric anchors.</p>
            )}
          </section>

          <section className="inspector-section decision-section">
            <p className="section-kicker">Release decision</p>
            <span className="status-label status-review">
              <span aria-hidden="true" className="status-dot" />
              {session.releaseState}
            </span>
            <p>{session.releaseRationale}</p>
          </section>
        </aside>
      </main>

      <footer className="artifact-footer">
        <div>
          <p className="section-kicker">Evidence artifacts</p>
          <h2>Export review metadata</h2>
          <p>
            Exports preserve review evidence and provenance. LeRobot and RLDS/OpenX outputs are metadata bridges only;
            they contain no observations, actions, media, or training shards.
          </p>
        </div>
        <div className="export-actions">
          <button className="button" type="button" onClick={exportNormalized}>
            Review JSON
          </button>
          <button className="button" type="button" onClick={exportCsv}>
            Event CSV
          </button>
          <button className="button" type="button" onClick={exportLeRobot}>
            LeRobot metadata
          </button>
          <button className="button" type="button" onClick={exportRlds}>
            RLDS/OpenX metadata
          </button>
        </div>
        <div className="provenance">
          <span>Source: {session.sourceName}</span>
          <span>Processing: local browser only</span>
          <span>ReviewKit viewer 1.0</span>
        </div>
      </footer>

      {dropActive ? (
        <div className="drop-overlay" role="status">
          <strong>Drop episode JSON</strong>
          <span>The file will be parsed locally.</span>
        </div>
      ) : null}
    </div>
  );
}
