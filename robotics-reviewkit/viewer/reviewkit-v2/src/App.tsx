import React from "react";
const sample = [{ timestamp_s: 0, label: "success" }, { timestamp_s: 4, label: "intervention" }, { timestamp_s: 9, label: "recovery" }];
export default function App() { return <main><h1>ReviewKit v2</h1><section>{sample.map((e, i) => <div key={i}>{e.timestamp_s}s {e.label}</div>)}</section></main>; }
