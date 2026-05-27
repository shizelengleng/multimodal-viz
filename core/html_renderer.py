"""Convert knowledge graph to interactive HTML with 3 modes: layer, focus, explore."""

from __future__ import annotations

import json
import sys
from pathlib import Path

from .knowledge_graph import KnowledgeGraph


def _get_vis_network_js() -> str:
    if getattr(sys, 'frozen', False):
        assets_dir = Path(sys._MEIPASS) / 'assets'
    else:
        assets_dir = Path(__file__).parent / 'assets'
    vis_path = assets_dir / 'vis-network.min.js'
    return vis_path.read_text(encoding='utf-8')

ARTICLE_TEMPLATE = """# {title}

本文档由知识图谱自动生成，用于 web-video-presentation 导览生成。

## 知识图谱概览

{overview}

## 核心概念

{concepts}

## 概念关系

{relations}
"""


def kg_to_article(kg: KnowledgeGraph) -> str:
    """Convert a KnowledgeGraph to a narrative article for web-video-presentation."""
    overview = (
        f"本知识图谱包含 {len(kg.concepts)} 个核心概念和 "
        f"{len(kg.relations)} 条概念关系，"
        f"推荐使用 {_layout_name(kg.layout_hint)} 布局展示。"
    )

    concepts_text = []
    for c in kg.concepts:
        concepts_text.append(
            f"### {c.name}\n\n"
            f"- **类别**: {_category_name(c.category)}\n"
            f"- **难度**: {_difficulty_name(c.difficulty)}\n"
            f"- **说明**: {c.description}\n"
        )

    relations_text = []
    for r in kg.relations:
        src_name = _find_concept_name(kg, r.source)
        tgt_name = _find_concept_name(kg, r.target)
        relations_text.append(
            f"- **{src_name}** {r.label or r.type.value} **{tgt_name}**"
        )

    return ARTICLE_TEMPLATE.format(
        title=kg.title,
        overview=overview,
        concepts="\n".join(concepts_text),
        relations="\n".join(relations_text) if relations_text else "无",
    )


def _compute_entry_nodes(kg: KnowledgeGraph) -> set[str]:
    """Identify entry-point nodes for explore mode."""
    targets = {r.target for r in kg.relations}
    entry: set[str] = set()
    for c in kg.concepts:
        if c.id not in targets or c.difficulty == "basic" or c.category in ("definition", "theory"):
            entry.add(c.id)
    return entry


def _compute_adjacency(kg: KnowledgeGraph) -> dict[str, list[str]]:
    """Build undirected adjacency map."""
    adj: dict[str, list[str]] = {c.id: [] for c in kg.concepts}
    for r in kg.relations:
        adj[r.source].append(r.target)
        adj[r.target].append(r.source)
    return adj


def kg_to_html(
    kg: KnowledgeGraph,
    groups: dict | None = None,
    group_names: dict | None = None,
    group_colors: dict | None = None,
) -> str:
    """Generate interactive HTML with 3 switchable exploration modes."""

    if groups is None:
        groups = get_vis_groups()
    if group_names is None:
        group_names = CATEGORY_NAMES
    if group_colors is None:
        group_colors = CATEGORY_COLORS

    # Build vis.js data
    nodes = []
    for c in kg.concepts:
        nodes.append({
            "id": c.id,
            "label": c.name,
            "title": f"<b>{c.name}</b><br>{c.description}<br><i>{_category_name(c.category)}</i>",
            "group": c.category,
            "value": _difficulty_size(c.difficulty),
            "desc": c.description,
            "category": c.category,
            "difficulty": c.difficulty,
        })

    edges = []
    for r in kg.relations:
        edges.append({
            "id": f"{r.source}_{r.target}",
            "from": r.source,
            "to": r.target,
            "label": r.label or r.type.value,
            "arrows": "to",
            "relType": r.type.value,
        })

    # Pre-compute explore-mode data
    entry_nodes = _compute_entry_nodes(kg)
    adjacency = _compute_adjacency(kg)

    kg_data = json.dumps({"nodes": nodes, "edges": edges}, ensure_ascii=False)
    groups_js = json.dumps(groups, ensure_ascii=False)
    group_names_js = json.dumps(group_names, ensure_ascii=False)
    group_colors_js = json.dumps(group_colors, ensure_ascii=False)
    entry_nodes_js = json.dumps(list(entry_nodes), ensure_ascii=False)
    adjacency_js = json.dumps(adjacency, ensure_ascii=False)
    title_safe = json.dumps(kg.title, ensure_ascii=False)[1:-1]  # JSON-escape the title
    layout_hint_js = json.dumps(kg.layout_hint, ensure_ascii=False)

    vis_js = _get_vis_network_js()

    return _build_html(
        title=title_safe,
        kg_data=kg_data,
        groups_js=groups_js,
        group_names_js=group_names_js,
        group_colors_js=group_colors_js,
        entry_nodes_js=entry_nodes_js,
        adjacency_js=adjacency_js,
        vis_js=vis_js,
        layout_hint_js=layout_hint_js,
    )


def _build_html(
    title: str, kg_data: str, groups_js: str,
    group_names_js: str, group_colors_js: str,
    entry_nodes_js: str, adjacency_js: str,
    vis_js: str, layout_hint_js: str = '"force_directed"',
) -> str:
    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<script>{vis_js}</script>
<style>
:root {{
  --bg: #FDFAF7;
  --card: #FFFFFF;
  --orange: #F26B1D;
  --orange-light: #FFF4EC;
  --orange-dark: #D4550C;
  --text: #2D2D2D;
  --text-light: #7A7A7A;
  --border: #E8E2DC;
  --shadow: 0 2px 12px rgba(0,0,0,0.06);
  --radius: 10px;
  --font: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", "Microsoft YaHei", sans-serif;
}}

* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{
  font-family: var(--font);
  background: var(--bg);
  color: var(--text);
  overflow: hidden;
}}

/* ── Top bar ── */
#topbar {{
  position:fixed; top:0; left:0; right:0; z-index:20;
  display:flex; align-items:center; gap:10px;
  padding:10px 20px; height:50px;
  background: var(--card);
  border-bottom: 1px solid var(--border);
  box-shadow: 0 1px 4px rgba(0,0,0,0.04);
}}
#topbar .logo {{
  font-size:15px; font-weight:700; color: var(--text);
  margin-right:12px; white-space:nowrap; max-width:280px;
  overflow:hidden; text-overflow:ellipsis;
}}
.mode-btn {{
  padding:6px 14px; border-radius:7px;
  border:1.5px solid var(--border);
  background:transparent; color:var(--text-light);
  font-size:13px; cursor:pointer; font-family:var(--font);
  transition:all 0.18s;
}}
.mode-btn:hover {{ border-color: var(--orange); color: var(--orange); }}
.mode-btn.active {{
  background: var(--orange);
  border-color: var(--orange);
  color: #FFF;
}}
#search {{
  margin-left:auto;
  background: var(--bg);
  border:1.5px solid var(--border); border-radius:8px;
  padding:7px 14px; color: var(--text); font-size:13px;
  width:220px; outline:none; font-family:var(--font);
}}
#search:focus {{ border-color: var(--orange); }}
#search::placeholder {{ color: #C0B8B0; }}

/* ── Panel ── */
#panel {{
  position:fixed; left:0; top:50px; bottom:0; width:250px; z-index:15;
  background: var(--card); border-right:1px solid var(--border);
  padding:20px 16px; overflow-y:auto;
  box-shadow: var(--shadow);
}}
#panel h3 {{
  font-size:12px; color: var(--orange); text-transform:uppercase;
  letter-spacing:0.1em; margin-bottom:14px; font-weight:700;
}}
#panel .layer-row {{
  display:flex; align-items:center; gap:10px; padding:7px 8px;
  border-radius:6px; cursor:pointer; font-size:13px; color:var(--text);
  transition:background 0.15s;
}}
#panel .layer-row:hover {{ background: var(--orange-light); }}
#panel .layer-row input {{ accent-color: var(--orange); }}
#panel .layer-dot {{ width:10px; height:10px; border-radius:50%; flex-shrink:0; }}
#panel .layer-count {{
  margin-left:auto; font-size:11px; color:var(--text-light);
  background:var(--bg); padding:2px 7px; border-radius:10px;
}}
#panel .panel-actions {{ display:flex; gap:8px; margin-top:14px; }}
#panel .panel-actions button {{
  flex:1; padding:7px 0; border-radius:6px;
  border:1.5px solid var(--border); background:transparent;
  color:var(--text-light); font-size:11px; cursor:pointer; font-family:var(--font);
}}
#panel .panel-actions button:hover {{ border-color: var(--orange); color: var(--orange); }}
#panel .explore-info {{
  font-size:12px; color:var(--text-light); line-height:1.6; margin-bottom:14px;
}}
#panel .explore-actions {{ display:flex; gap:8px; }}
#panel .explore-actions button {{
  flex:1; padding:8px 0; border-radius:6px;
  border:none; background:var(--orange-light); color:var(--orange-dark);
  font-size:12px; cursor:pointer; font-weight:600; font-family:var(--font);
}}
#panel .explore-actions button:hover {{ background: var(--orange); color:#FFF; }}

/* ── Network ── */
#mynetwork {{
  position:fixed; top:50px; left:250px; right:0; bottom:0; z-index:5;
}}

/* ── Detail sidebar ── */
#sidebar {{
  position:fixed; right:0; top:0; width:360px; height:100vh;
  background: var(--card); border-left:1px solid var(--border);
  padding:32px 24px; overflow-y:auto; z-index:25;
  box-shadow: -4px 0 24px rgba(0,0,0,0.08);
  transform:translateX(100%); transition:transform 0.3s ease;
}}
#sidebar.open {{ transform:translateX(0); }}
#sidebar h2 {{ font-size:22px; margin-bottom:4px; color:var(--text); }}
#sidebar .category {{
  display:inline-block;
  font-size:11px; text-transform:uppercase; letter-spacing:0.08em;
  color: var(--orange); background:var(--orange-light);
  padding:3px 10px; border-radius:12px; margin-bottom:14px;
}}
#sidebar .description {{
  font-size:15px; line-height:1.7; color:var(--text-light); margin-bottom:20px;
}}
#sidebar .related h3 {{
  font-size:12px; color: var(--orange); margin-bottom:10px;
  text-transform:uppercase; letter-spacing:0.08em; font-weight:700;
}}
#sidebar .related .rel-item {{
  display:flex; align-items:center; gap:8px; padding:9px 0;
  border-bottom:1px solid var(--border); font-size:14px; color:var(--text);
}}
#sidebar .related .rel-item .rel-dir {{ color:var(--orange); font-size:11px; min-width:16px; }}
#sidebar .related .rel-item .rel-label {{ color:var(--text-light); font-size:12px; }}
#close-btn {{
  position:absolute; top:14px; right:14px;
  background:none; border:none; color:var(--text-light); font-size:20px;
  cursor:pointer; width:32px; height:32px; display:flex;
  align-items:center; justify-content:center; border-radius:50%;
}}
#close-btn:hover {{ color:var(--orange); background:var(--orange-light); }}

/* ── Focus indicator ── */
#focus-indicator {{
  position:fixed; top:60px; left:50%; transform:translateX(-50%); z-index:18;
  background: var(--orange); color:#FFF;
  font-size:12px; padding:6px 18px; border-radius:16px;
  pointer-events:none; opacity:0; transition:opacity 0.3s;
  font-weight:600;
}}
#focus-indicator.show {{ opacity:1; }}

/* ── Legend ── */
#legend {{
  position:fixed; bottom:16px; left:258px; z-index:10;
  display:flex; gap:12px; flex-wrap:wrap;
  background:var(--card); border-radius:8px; padding:8px 12px;
  border:1px solid var(--border); box-shadow:var(--shadow);
}}
.legend-item {{ display:flex; align-items:center; gap:5px; font-size:11px; color:var(--text-light); }}
.legend-dot {{ width:8px; height:8px; border-radius:50%; }}

/* ── Export ── */
#export-btn {{
  position:fixed; bottom:16px; right:16px; z-index:10;
  background:var(--card); border:1.5px solid var(--orange);
  color:var(--orange); border-radius:7px; padding:7px 16px;
  font-size:12px; cursor:pointer; font-weight:600; font-family:var(--font);
}}
#export-btn:hover {{ background:var(--orange); color:#FFF; }}

/* ── Explore badge ── */
.explore-badge {{
  position:absolute; top:-6px; right:-6px;
  background:var(--orange); color:#FFF;
  font-size:10px; min-width:16px; height:16px; line-height:16px;
  text-align:center; border-radius:8px; padding:0 4px;
  pointer-events:none;
}}
</style>
</head>
<body>

<div id="topbar">
  <span class="logo">{title}</span>
  <button class="mode-btn active" id="btn-layer">图层</button>
  <button class="mode-btn" id="btn-focus">焦点</button>
  <button class="mode-btn" id="btn-explore">探索</button>
  <input id="search" type="text" placeholder="搜索概念..." />
</div>

<div id="panel"></div>
<div id="focus-indicator">点击空白处退出焦点 | 按 Esc 退出</div>
<div id="mynetwork"></div>

<div id="sidebar">
  <button id="close-btn">&times;</button>
  <h2 id="node-name"></h2>
  <div class="category" id="node-category"></div>
  <div class="description" id="node-desc"></div>
  <div class="related">
    <h3>关联概念</h3>
    <div id="node-related"></div>
  </div>
</div>

<div id="legend"></div>
<button id="export-btn">导出 PNG</button>

<script>
// ── Data ──
var rawData = {kg_data};
var groupNames = {group_names_js};
var groupColors = {group_colors_js};
var entryNodeIds = new Set({entry_nodes_js});
var adjacencyMap = {adjacency_js};

var nodesDS = new vis.DataSet(rawData.nodes);
var edgesDS = new vis.DataSet(rawData.edges);

// ── State ──
var currentMode = 'layer';
var focusNodeId = null;
var expandedNodes = new Set(entryNodeIds);
var layerVisibility = {{}};
var searchQuery = '';

// ── Network ──
var container = document.getElementById('mynetwork');
var baseNodeSize = 18;
var baseOptions = {{
  nodes: {{
    shape: "dot", size: baseNodeSize,
    font: {{ size:13, color:"#4A4A4A", face:"-apple-system, PingFang SC, Microsoft YaHei, sans-serif", strokeWidth:2, strokeColor:"#FFFFFF" }},
    borderWidth: 2.5,
    shadow: {{ enabled:true, size:6, color:"rgba(0,0,0,0.08)" }},
  }},
  edges: {{
    width: 1.8,
    color: {{ color:"#D4CCC4", highlight:"#F26B1D" }},
    smooth: {{ type:"continuous" }},
    font: {{ size:10, color:"#999", background:"#FFFFFF", strokeWidth:2, strokeColor:"#FFFFFF" }},
  }},
  physics: {{
    solver: "barnesHut",
    barnesHut: {{
      gravitationalConstant: -3000,
      centralGravity: 0.5,
      springLength: 200,
      springConstant: 0.02,
      damping: 0.3,
      avoidOverlap: 0.3,
    }},
    maxVelocity: 6,
    minVelocity: 0.5,
    stabilization: {{ iterations: 200, fit: true }},
  }},
  interaction: {{ hover:true, tooltipDelay:150, zoomView:true, dragView:true }},
  groups: {groups_js},
}};

// ── Apply layout hint ──
var layoutHint = {layout_hint_js};
var initialHierarchical = false;
if (layoutHint === 'hierarchical') {{
  baseOptions.layout = {{ hierarchical: {{ enabled:true, direction:'UD', sortMethod:'directed', nodeSpacing:180, levelSeparation:200 }} }};
  baseOptions.physics = {{ enabled:false }};
  initialHierarchical = true;
}} else if (layoutHint === 'radial') {{
  baseOptions.physics.barnesHut.centralGravity = 2.0;
  baseOptions.physics.barnesHut.springLength = 120;
}} else if (layoutHint === 'timeline') {{
  baseOptions.layout = {{ hierarchical: {{ enabled:true, direction:'LR', sortMethod:'directed', nodeSpacing:120, levelSeparation:250 }} }};
  baseOptions.physics = {{ enabled:false }};
  initialHierarchical = true;
}}

var network = new vis.Network(container, {{nodes:nodesDS, edges:edgesDS}}, baseOptions);

// Hierarchical/timeline: use layout for initial positioning, then enable free physics
if (initialHierarchical) {{
  network.once('stabilized', function() {{
    network.setOptions({{ layout: {{ hierarchical: {{ enabled:false }} }}, physics: {{ enabled:true, solver:"barnesHut", barnesHut:{{ gravitationalConstant:-3000, centralGravity:0.5, springLength:200, springConstant:0.02, damping:0.3, avoidOverlap:0.3 }}, maxVelocity:6, minVelocity:0.5, stabilization:{{ iterations:200, fit:true }} }} }});
  }});
  // Fallback in case stabilized event never fires
  setTimeout(function() {{
    network.setOptions({{ layout: {{ hierarchical: {{ enabled:false }} }}, physics: {{ enabled:true, solver:"barnesHut", barnesHut:{{ gravitationalConstant:-3000, centralGravity:0.5, springLength:200, springConstant:0.02, damping:0.3, avoidOverlap:0.3 }}, maxVelocity:6, minVelocity:0.5, stabilization:{{ iterations:200, fit:true }} }} }});
    initialHierarchical = false;
  }}, 3000);
}}

// ── Legend ──
(function() {{
  var groups = {{}};
  nodesDS.forEach(function(n) {{ groups[n.group] = (groups[n.group]||0)+1; }});
  document.getElementById('legend').innerHTML = Object.keys(groups).map(function(g) {{
    var color = groupColors[g] || "#888";
    return '<div class="legend-item"><span class="legend-dot" style="background:'+color+'"></span>'+(groupNames[g]||g)+' ('+groups[g]+')</div>';
  }}).join("");
}})();

// ── Sidebar ──
function openSidebar(nodeId) {{
  var node = nodesDS.get(nodeId);
  if (!node) return;
  document.getElementById('node-name').textContent = node.label;
  document.getElementById('node-category').textContent = groupNames[node.group] || node.group;
  document.getElementById('node-desc').textContent = node.desc || '';

  var related = edgesDS.get({{ filter: function(e) {{ return e.from===nodeId || e.to===nodeId; }} }});
  var html = related.map(function(e) {{
    var otherId = e.from===nodeId ? e.to : e.from;
    var other = nodesDS.get(otherId);
    var dir = e.from===nodeId ? '&#8594;' : '&#8592;';
    return '<div class="rel-item"><span class="rel-dir">'+dir+'</span><span class="rel-label">'+(e.label||'')+'</span> '+(other?other.label:otherId)+'</div>';
  }}).join("");
  document.getElementById('node-related').innerHTML = html || '<div style="color:#C0B8B0">无关联概念</div>';
  document.getElementById('sidebar').classList.add('open');
}}

function closeSidebar() {{ document.getElementById('sidebar').classList.remove('open'); }}
document.getElementById('close-btn').addEventListener('click', closeSidebar);

// ── Click handler ──
network.on('click', function(params) {{
  var nodeId = params.nodes[0];

  if (currentMode === 'focus') {{
    if (nodeId) {{ enterFocus(nodeId); }}
    else {{ exitFocus(); }}
    return;
  }}

  if (currentMode === 'explore' && nodeId) {{
    toggleExploreNode(nodeId);
    return;
  }}

  if (nodeId) {{ openSidebar(nodeId); }}
}});

// ═══════════════════════════════
// MODE SWITCHING
// ═══════════════════════════════
function switchMode(mode) {{
  currentMode = mode;
  focusNodeId = null;
  document.getElementById('focus-indicator').classList.remove('show');

  ['layer','focus','explore'].forEach(function(m) {{
    var btn = document.getElementById('btn-'+m);
    if (btn) btn.classList.toggle('active', m===mode);
  }});

  // Reset all nodes & edges to defaults
  nodesDS.forEach(function(n) {{
    var nc = groupColors[n.group] || '#888';
    nodesDS.update({{ id:n.id, hidden:false, size:baseNodeSize, opacity:1,
      color:{{ background:nc, border:nc, highlight:{{ background:nc, border:nc }} }},
      font:{{ size:13, color:"#4A4A4A", strokeWidth:2, strokeColor:"#FFF" }}, borderWidth:2.5 }});
  }});
  edgesDS.forEach(function(e) {{
    edgesDS.update({{ id:e.id, hidden:false, width:baseOptions.edges.width, color:baseOptions.edges.color }});
  }});

  if (mode === 'layer') {{
    buildLayerPanel();
    network.setOptions({{ physics:{{ enabled:true }} }});
    network.fit();
  }}
  if (mode === 'focus') {{
    buildFocusPanel();
    network.setOptions({{ physics:{{ enabled:true }} }});
    network.fit();
  }}
  if (mode === 'explore') {{
    buildExplorePanel();
    network.setOptions({{ physics:{{ enabled:true }} }});
    network.fit();
    // Disable physics after initial layout settles
    network.once('stabilized', function() {{
      if (currentMode === 'explore') network.setOptions({{ physics:{{ enabled:false }} }});
    }});
    setTimeout(function() {{
      if (currentMode === 'explore') network.setOptions({{ physics:{{ enabled:false }} }});
    }}, 2500);
  }}

  if (mode !== 'explore') applySearch();
  else applyExploreVisibility();
}}

// ═══════════════════════════════
// MODE 1: LAYER
// ═══════════════════════════════
function buildLayerPanel() {{
  var counts = {{}};
  nodesDS.forEach(function(n) {{ counts[n.group] = (counts[n.group]||0)+1; }});
  var cats = Object.keys(counts).sort();
  cats.forEach(function(c) {{ if (!(c in layerVisibility)) layerVisibility[c] = true; }});

  document.getElementById('panel').innerHTML =
    '<h3>图层筛选</h3>' +
    cats.map(function(c) {{
      return '<label class="layer-row">' +
        '<input type="checkbox" '+(layerVisibility[c]?'checked':'')+' data-cat="'+c+'" onchange="toggleLayer(this.dataset.cat,this.checked)">' +
        '<span class="layer-dot" style="background:'+(groupColors[c]||'#888')+'"></span>' +
        (groupNames[c]||c) + '<span class="layer-count">'+counts[c]+'</span></label>';
    }}).join("") +
    '<div class="panel-actions">' +
      '<button id="btn-all-on">全部开启</button>' +
      '<button id="btn-all-off">全部关闭</button>' +
    '</div>';

  document.getElementById('btn-all-on').addEventListener('click', function(){{ setAllLayers(true); }});
  document.getElementById('btn-all-off').addEventListener('click', function(){{ setAllLayers(false); }});
}}

function toggleLayer(cat, visible) {{
  layerVisibility[cat] = visible;
  applyLayerVisibility();
  applySearch();
}}

function setAllLayers(visible) {{
  Object.keys(layerVisibility).forEach(function(c) {{ layerVisibility[c] = visible; }});
  buildLayerPanel();
  applyLayerVisibility();
  applySearch();
}}

function applyLayerVisibility() {{
  var hiddenCats = new Set(Object.keys(layerVisibility).filter(function(c){{ return !layerVisibility[c]; }}));
  nodesDS.forEach(function(n) {{
    nodesDS.update({{ id:n.id, hidden:hiddenCats.has(n.group) }});
  }});
  edgesDS.forEach(function(e) {{
    var fn = nodesDS.get(e.from), tn = nodesDS.get(e.to);
    edgesDS.update({{ id:e.id, hidden: hiddenCats.has(fn?fn.group:'') || hiddenCats.has(tn?tn.group:'') }});
  }});
}}

// ═══════════════════════════════
// MODE 2: FOCUS
// ═══════════════════════════════
function buildFocusPanel() {{
  document.getElementById('panel').innerHTML =
    '<h3>焦点探索</h3>' +
    '<p class="explore-info">点击任意概念节点，它居中放大，关联节点高亮环绕。<br><br>点击空白处或按 Esc 返回全景。</p>';
}}

function enterFocus(nodeId) {{
  focusNodeId = nodeId;
  document.getElementById('focus-indicator').classList.add('show');

  var neighbors = new Set(adjacencyMap[nodeId] || []);
  neighbors.add(nodeId);

  nodesDS.forEach(function(n) {{
    if (n.id === nodeId) {{
      var c = groupColors[n.group] || '#F26B1D';
      nodesDS.update({{ id:n.id, size:40,
        color:{{ background:c, border:"#F26B1D", highlight:{{ background:c, border:"#E06000" }} }},
        font:{{ size:17, color:"#2D2D2D", strokeWidth:3, strokeColor:"#FFF" }}, borderWidth:4, hidden:false, opacity:1 }});
    }} else if (neighbors.has(n.id)) {{
      var nc = groupColors[n.group] || '#888';
      nodesDS.update({{ id:n.id, size:22,
        color:{{ background:nc, border:"#F26B1D", highlight:{{ background:nc, border:"#E06000" }} }},
        borderWidth:2.5, hidden:false, opacity:1 }});
    }} else {{
      nodesDS.update({{ id:n.id, opacity:0.06, size:6 }});
    }}
  }});

  edgesDS.forEach(function(e) {{
    if (e.from===nodeId || e.to===nodeId) {{
      edgesDS.update({{ id:e.id, width:3.5, color:{{ color:"#F26B1D", highlight:"#E06000" }}, hidden:false }});
    }} else {{
      edgesDS.update({{ id:e.id, hidden:true }});
    }}
  }});

  network.fit({{ nodes: Array.from(neighbors) }});
}}

function exitFocus() {{
  focusNodeId = null;
  document.getElementById('focus-indicator').classList.remove('show');

  nodesDS.forEach(function(n) {{
    var nc = groupColors[n.group] || '#888';
    nodesDS.update({{ id:n.id, size:baseNodeSize, opacity:1,
      color:{{ background:nc, border:nc, highlight:{{ background:nc, border:nc }} }},
      font:{{ size:13, color:"#4A4A4A", strokeWidth:2, strokeColor:"#FFF" }}, borderWidth:2.5 }});
  }});
  edgesDS.forEach(function(e) {{
    edgesDS.update({{ id:e.id, hidden:false, width:baseOptions.edges.width, color:baseOptions.edges.color }});
  }});

  network.fit();
}}

// ═══════════════════════════════
// MODE 3: EXPLORE (static, draggable graph)
// ═══════════════════════════════
function buildExplorePanel() {{
  document.getElementById('panel').innerHTML =
    '<h3>渐进探索</h3>' +
    '<p class="explore-info">静态图谱可自由拖拽。<br>从入口概念开始，点击逐步展开关联。<br>+N 表示还有未展开的连接。</p>' +
    '<div class="explore-actions">' +
      '<button id="btn-expand-all">全部展开</button>' +
      '<button id="btn-reset">重置</button>' +
    '</div>';
  document.getElementById('btn-expand-all').addEventListener('click', expandAllNodes);
  document.getElementById('btn-reset').addEventListener('click', resetExplore);
}}

function applyExploreVisibility() {{
  nodesDS.forEach(function(n) {{
    nodesDS.update({{ id:n.id, hidden:!expandedNodes.has(n.id) }});
  }});
  edgesDS.forEach(function(e) {{
    edgesDS.update({{ id:e.id, hidden:!expandedNodes.has(e.from) || !expandedNodes.has(e.to) }});
  }});

  // Badge: +N for hidden neighbors
  nodesDS.forEach(function(n) {{
    if (!expandedNodes.has(n.id)) return;
    var hiddenCount = (adjacencyMap[n.id]||[]).filter(function(a){{ return !expandedNodes.has(a); }}).length;
    var baseLabel = n.label.replace(/ \\+\\d+$/, '');
    nodesDS.update({{ id:n.id, label: hiddenCount>0 ? baseLabel+' +'+hiddenCount : baseLabel }});
  }});
}}

function toggleExploreNode(nodeId) {{
  if (!expandedNodes.has(nodeId)) return;
  var hidden = (adjacencyMap[nodeId]||[]).filter(function(a){{ return !expandedNodes.has(a); }});
  if (hidden.length === 0) return;
  hidden.forEach(function(a){{ expandedNodes.add(a); }});
  applyExploreVisibility();
  applySearch();
}}

function expandAllNodes() {{
  nodesDS.forEach(function(n){{ expandedNodes.add(n.id); }});
  applyExploreVisibility();
  applySearch();
}}

function resetExplore() {{
  expandedNodes = new Set(entryNodeIds);
  applyExploreVisibility();
  applySearch();
}}

// ═══════════════════════════════
// SEARCH
// ═══════════════════════════════
document.getElementById('search').addEventListener('input', function(e) {{
  searchQuery = e.target.value.toLowerCase().trim();
  applySearch();
}});

function applySearch() {{
  if (!searchQuery) {{
    // Clear search — restore mode visibility
    if (currentMode==='layer')  {{ applyLayerVisibility(); }}
    if (currentMode==='focus')  {{ if (focusNodeId) enterFocus(focusNodeId); else exitFocus(); }}
    if (currentMode==='explore') {{ applyExploreVisibility(); }}
    return;
  }}

  // Find matching nodes
  var matched = new Set();
  nodesDS.forEach(function(n) {{
    var label = (n.label||'').toLowerCase().replace(/ \\+\\d+$/, '');
    var desc = (n.desc||'').toLowerCase();
    if (label.includes(searchQuery) || desc.includes(searchQuery)) matched.add(n.id);
  }});

  nodesDS.forEach(function(n) {{
    nodesDS.update({{ id:n.id, hidden:!matched.has(n.id) }});
  }});
  edgesDS.forEach(function(e) {{
    edgesDS.update({{ id:e.id, hidden:!matched.has(e.from) || !matched.has(e.to) }});
  }});

  if (matched.size > 0) network.fit();
}}

// ═══════════════════════════════
// UTILS
// ═══════════════════════════════
document.getElementById('export-btn').addEventListener('click', function() {{
  var canvas = document.querySelector('#mynetwork canvas');
  if (!canvas) {{ return; }}
  var link = document.createElement('a');
  link.download = '{title}.png';
  link.href = canvas.toDataURL('image/png');
  link.click();
}});

document.addEventListener('keydown', function(e) {{
  if (e.key === 'Escape') {{
    closeSidebar();
    if (currentMode==='focus') {{ exitFocus(); }}
  }}
}});

// ── Init ──
buildLayerPanel();

document.getElementById('btn-layer').addEventListener('click', function(){{ switchMode('layer'); }});
document.getElementById('btn-focus').addEventListener('click', function(){{ switchMode('focus'); }});
document.getElementById('btn-explore').addEventListener('click', function(){{ switchMode('explore'); }});
</script>
</body>
</html>"""


# ── Helper functions ──

def _category_name(cat: str) -> str:
    names = {
        "definition": "概念定义", "principle": "原理规律",
        "example": "例子案例", "application": "实际应用",
        "theory": "理论学派", "person": "人物学者",
        "event": "历史事件", "process": "流程步骤", "other": "其他",
    }
    return names.get(cat, cat)


def _difficulty_name(diff: str) -> str:
    return {"basic": "基础", "intermediate": "进阶", "advanced": "高级"}.get(diff, diff)


def _difficulty_size(diff: str) -> int:
    return {"basic": 12, "intermediate": 20, "advanced": 30}.get(diff, 16)


def _layout_name(hint: str) -> str:
    return {"force_directed": "力导向图", "radial": "思维导图", "hierarchical": "层级图", "timeline": "时间线"}.get(hint, hint)


def _find_concept_name(kg: KnowledgeGraph, cid: str) -> str:
    for c in kg.concepts:
        if c.id == cid:
            return c.name
    return cid


CATEGORY_COLORS = {
    "definition": "#5b9bd5", "principle": "#ed7d31",
    "example": "#70ad47", "application": "#ffc000",
    "theory": "#9b59b6", "person": "#e74c3c",
    "event": "#1abc9c", "process": "#3498db", "other": "#95a5a6",
}

CATEGORY_NAMES = {
    "definition": "概念定义", "principle": "原理规律",
    "example": "例子案例", "application": "实际应用",
    "theory": "理论学派", "person": "人物学者",
    "event": "历史事件", "process": "流程步骤", "other": "其他",
}


def get_vis_groups():
    """Generate vis.js groups config from category definitions."""
    return {
        cat: {"color": {"background": color, "border": color, "highlight": {"background": color, "border": color}}}
        for cat, color in CATEGORY_COLORS.items()
    }
