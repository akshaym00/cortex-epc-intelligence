import { useEffect, useRef, useState } from "react";
import { severityLabel } from "../../utils/severity";

const NODE_WIDTH = 170;
const NODE_HEIGHT = 58;
const COLUMN_GAP = 95;
const ROW_GAP = 64;

function buildLayout(entities, relationships) {
  const connectedNames = new Set(
    relationships.flatMap(({ source, target }) => [source, target]),
  );
  const names = new Set(
    entities
      .map((entity) => entity.name)
      .filter((name) => connectedNames.has(name)),
  );

  relationships.forEach(({ source, target }) => {
    names.add(source);
    names.add(target);
  });

  const incoming = new Map([...names].map((name) => [name, 0]));
  const outgoing = new Map([...names].map((name) => [name, []]));

  relationships.forEach(({ source, target }) => {
    if (!outgoing.has(source) || !incoming.has(target)) return;
    outgoing.get(source).push(target);
    incoming.set(target, incoming.get(target) + 1);
  });

  const levels = new Map();
  const queue = [...names].filter((name) => incoming.get(name) === 0);

  // If the extracted graph contains only cycles, still render every node.
  if (queue.length === 0 && names.size > 0) queue.push([...names][0]);

  queue.forEach((name) => levels.set(name, 0));

  while (queue.length > 0) {
    const source = queue.shift();
    const nextLevel = levels.get(source) + 1;

    outgoing.get(source).forEach((target) => {
      if (!levels.has(target) || levels.get(target) < nextLevel) {
        levels.set(target, nextLevel);
      }

      incoming.set(target, incoming.get(target) - 1);
      if (incoming.get(target) === 0) queue.push(target);
    });
  }

  [...names].forEach((name) => {
    if (!levels.has(name)) levels.set(name, 0);
  });

  const columns = [];
  levels.forEach((level, name) => {
    columns[level] ??= [];
    columns[level].push(name);
  });

  // Barycentric ordering keeps children close to their parents and reduces
  // crossings without adding a heavyweight graph-layout dependency.
  for (let level = 1; level < columns.length; level += 1) {
    const previousRows = new Map(
      (columns[level - 1] || []).map((name, index) => [name, index]),
    );
    columns[level]?.sort((left, right) => {
      const parentAverage = (name) => {
        const parents = relationships
          .filter((edge) => edge.target === name && previousRows.has(edge.source))
          .map((edge) => previousRows.get(edge.source));
        return parents.length
          ? parents.reduce((sum, row) => sum + row, 0) / parents.length
          : Number.MAX_SAFE_INTEGER;
      };
      return parentAverage(left) - parentAverage(right);
    });
  }

  const positions = new Map();
  columns.forEach((column = [], level) => {
    column.forEach((name, row) => {
      positions.set(name, {
        x: 35 + level * (NODE_WIDTH + COLUMN_GAP),
        y: 35 + row * (NODE_HEIGHT + ROW_GAP),
      });
    });
  });

  return { columns, positions };
}

function KnowledgeGraph({ id, entities = [], relationships = [], impacts = [], selectedEntityId = null, onEntitySelect }) {
  const [selectedNodeId, setSelectedNodeId] = useState(null);
  const [highlightedEntityId, setHighlightedEntityId] = useState(null);
  const graphCanvasRef = useRef(null);

  if (entities.length === 0 && relationships.length === 0) {
    return (
      <section id={id} className="card knowledge-graph-card">
        <h3>Knowledge Graph</h3>
        <p>No graph available. Analyze a document to build one.</p>
      </section>
    );
  }

  const { columns, positions } = buildLayout(entities, relationships);
  const maxRows = Math.max(1, ...columns.map((column) => column?.length || 0));
  const width = Math.max(
    600,
    columns.length * (NODE_WIDTH + COLUMN_GAP) + 30,
  );
  const height = maxRows * (NODE_HEIGHT + ROW_GAP) + 40;
  const entityByName = new Map(entities.map((entity) => [entity.name, entity]));
  const entityNameById = new Map(entities.map((entity) => [entity.id, entity.name]));
  const entityTypes = new Map(
    entities.map((entity) => [entity.name, entity.entity_type]),
  );
  const hiddenCount = entities.length - positions.size;
  const activeEntityId = selectedEntityId || selectedNodeId;
  const selectedName = activeEntityId ? entityNameById.get(activeEntityId) : null;
  const selectedImpact = impacts
    .flatMap((report) =>
      (report.impacted_entities || []).map((impact) => ({
        ...impact,
        event_title: report.event_title,
      })),
    )
    .find((impact) => impact.name === selectedName);
  const selectedConnections = relationships.filter(
    (relationship) =>
      relationship.source === selectedName || relationship.target === selectedName,
  );

  useEffect(() => {
    if (!activeEntityId) return undefined;

    setHighlightedEntityId(activeEntityId);
    const timer = setTimeout(() => setHighlightedEntityId(null), 3000);

    const nodeElement = document.getElementById(`graph-node-${activeEntityId}`);
    if (nodeElement?.scrollIntoView) {
      nodeElement.scrollIntoView({ behavior: "smooth", block: "center", inline: "center" });
    }

    return () => clearTimeout(timer);
  }, [activeEntityId]);

  return (
    <section id={id} className="card knowledge-graph-card">
      <div className="graph-heading">
        <h3>Knowledge Graph</h3>
        <span>{positions.size} nodes · {relationships.length} links</span>
      </div>
      {hiddenCount > 0 && (
        <p className="graph-note">
          {hiddenCount} unconnected entit{hiddenCount === 1 ? "y" : "ies"} hidden for clarity.
        </p>
      )}

      <div className="graph-canvas" ref={graphCanvasRef}>
        <svg viewBox={`0 0 ${width} ${height}`} role="img" aria-label="Project knowledge graph">
          <defs>
            <marker id="graph-arrow" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto">
              <path d="M0,0 L8,4 L0,8 Z" fill="#64748b" />
            </marker>
          </defs>

          {relationships.map((relationship, index) => {
            const source = positions.get(relationship.source);
            const target = positions.get(relationship.target);
            if (!source || !target) return null;

            const startX = source.x + NODE_WIDTH;
            const startY = source.y + NODE_HEIGHT / 2;
            const endX = target.x;
            const endY = target.y + NODE_HEIGHT / 2;
            const middleX = (startX + endX) / 2;
            const labelOffset = ((index % 5) - 2) * 11;
            const curveOffset = ((index % 3) - 1) * 18;

            return (
              <g key={`${relationship.source}-${relationship.target}-${index}`}>
                <path
                  className="graph-edge"
                  d={`M ${startX} ${startY} C ${middleX + curveOffset} ${startY}, ${middleX + curveOffset} ${endY}, ${endX - 8} ${endY}`}
                  markerEnd="url(#graph-arrow)"
                />
                <text className="graph-edge-label" x={middleX + curveOffset} y={(startY + endY) / 2 - 7 + labelOffset}>
                  {relationship.relationship_type.replaceAll("_", " ")}
                </text>
              </g>
            );
          })}

          {entities
            .filter((entity) => positions.has(entity.name))
            .map((entity) => {
              const position = positions.get(entity.name);
              const isSelected = activeEntityId === entity.id;
              const isHighlighted = highlightedEntityId === entity.id;

              return (
                <g
                  key={entity.id}
                  id={`graph-node-${entity.id}`}
                  className="graph-node-group"
                  transform={`translate(${position.x} ${position.y})`}
                  onClick={() => {
                    setSelectedNodeId(entity.id);
                    onEntitySelect?.(entity.id);
                  }}
                  role="button"
                  tabIndex="0"
                  onKeyDown={(event) => event.key === "Enter" && (() => { setSelectedNodeId(entity.id); onEntitySelect?.(entity.id); })()}
                >
                  <rect
                    className={`graph-node graph-node-${entity.entity_type || "entity"} ${isSelected ? "graph-node-selected" : ""} ${isHighlighted ? "graph-node-highlighted" : ""}`}
                    width={NODE_WIDTH}
                    height={NODE_HEIGHT}
                    rx="10"
                  />
                  <text className="graph-node-name" x={NODE_WIDTH / 2} y="25" textAnchor="middle">
                    {entity.name.length > 22 ? `${entity.name.slice(0, 21)}…` : entity.name}
                  </text>
                  <text className="graph-node-type" x={NODE_WIDTH / 2} y="43" textAnchor="middle">
                    {entity.entity_type || "entity"}
                  </text>
                </g>
              );
            })}
        </svg>
      </div>

      {selectedName && (
        <aside className="reasoning-panel">
          <button className="reasoning-close" onClick={() => setSelectedNodeId(null)} aria-label="Close explanation">×</button>
          <span className="reasoning-eyebrow">Explainable reasoning</span>
          <h4>{selectedName}</h4>

          {selectedImpact ? (
            <>
              <p><strong>Affected by:</strong> {selectedImpact.event_title}</p>
              <div className="reasoning-path">
                {selectedImpact.dependency_path.join(" → ")}
              </div>
              <p>{selectedImpact.reason}</p>
              <span className={`severity-badge severity-${selectedImpact.severity}`}>
                {severityLabel(selectedImpact.severity)} impact
              </span>
            </>
          ) : (
            <>
              <p>This node participates in {selectedConnections.length} project relationship{selectedConnections.length === 1 ? "" : "s"}.</p>
              {selectedConnections.map((connection, index) => (
                <div className="connection-line" key={`${connection.source}-${connection.target}-${index}`}>
                  {connection.source} → {connection.target}
                  <small>{connection.relationship_type.replaceAll("_", " ")}</small>
                </div>
              ))}
            </>
          )}
        </aside>
      )}
    </section>
  );
}

export default KnowledgeGraph;
