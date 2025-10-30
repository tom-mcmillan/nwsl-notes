#!/usr/bin/env python3
"""
Generate images for Article 1: The Linguistic Exposure Layer
Creates professional diagrams and visualizations for the Substack article.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import json

plt.style.use('seaborn-v0_8-darkgrid')
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Arial', 'Helvetica', 'DejaVu Sans']
plt.rcParams['font.size'] = 10

def create_mcp_architecture_diagram():
    """Create MCP architecture diagram showing layers."""
    fig, ax = plt.subplots(figsize=(12, 10))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 12)
    ax.axis('off')
    
    color_user = '#E8F4F8'
    color_ai = '#FFE5CC'
    color_mcp = '#D4E6F1'
    color_tools = '#D5F4E6'
    color_db = '#F9E79F'
    
    user_box = FancyBboxPatch((0.5, 10), 9, 1.5, 
                              boxstyle="round,pad=0.1", 
                              facecolor=color_user, 
                              edgecolor='#2C3E50', linewidth=2)
    ax.add_patch(user_box)
    ax.text(5, 10.75, 'User / AI Agent', ha='center', va='center', 
            fontsize=14, fontweight='bold')
    ax.text(5, 10.3, 'Natural Language Query: "Compare Sophia Smith and Trinity Rodman"', 
            ha='center', va='center', fontsize=9, style='italic')
    
    arrow1 = FancyArrowPatch((5, 10), (5, 9.2), 
                            arrowstyle='->', mutation_scale=20, 
                            linewidth=2, color='#2C3E50')
    ax.add_patch(arrow1)
    ax.text(5.5, 9.6, 'JSON-RPC', fontsize=8, style='italic')
    
    mcp_box = FancyBboxPatch((0.5, 7.5), 9, 1.5, 
                             boxstyle="round,pad=0.1", 
                             facecolor=color_mcp, 
                             edgecolor='#2C3E50', linewidth=2)
    ax.add_patch(mcp_box)
    ax.text(5, 8.5, 'MCP Server (nwsl-mcp-py)', ha='center', va='center', 
            fontsize=14, fontweight='bold')
    ax.text(5, 8.05, '38 Research-Grade Tools | Tool Registry | Routing Logic', 
            ha='center', va='center', fontsize=9)
    
    arrow2 = FancyArrowPatch((5, 7.5), (5, 6.7), 
                            arrowstyle='->', mutation_scale=20, 
                            linewidth=2, color='#2C3E50')
    ax.add_patch(arrow2)
    ax.text(5.5, 7.1, 'Tool Invocation', fontsize=8, style='italic')
    
    tool_categories = [
        ('Measurement\n11 tools', 1, 5),
        ('Statistical\n4 tools', 2.8, 5),
        ('Temporal\n3 tools', 4.6, 5),
        ('Comparative\n3 tools', 6.4, 5),
        ('Contextual\n4 tools', 8.2, 5)
    ]
    
    for label, x, y in tool_categories:
        tool_box = FancyBboxPatch((x, y), 1.6, 1.2, 
                                  boxstyle="round,pad=0.05", 
                                  facecolor=color_tools, 
                                  edgecolor='#27AE60', linewidth=1.5)
        ax.add_patch(tool_box)
        ax.text(x + 0.8, y + 0.6, label, ha='center', va='center', 
                fontsize=8, fontweight='bold')
    
    arrow3 = FancyArrowPatch((5, 5), (5, 4.2), 
                            arrowstyle='->', mutation_scale=20, 
                            linewidth=2, color='#2C3E50')
    ax.add_patch(arrow3)
    ax.text(5.5, 4.6, 'SQL Query', fontsize=8, style='italic')
    
    db_box = FancyBboxPatch((0.5, 2.5), 9, 1.5, 
                            boxstyle="round,pad=0.1", 
                            facecolor=color_db, 
                            edgecolor='#2C3E50', linewidth=2)
    ax.add_patch(db_box)
    ax.text(5, 3.5, 'PostgreSQL Data Warehouse', ha='center', va='center', 
            fontsize=14, fontweight='bold')
    ax.text(5, 3.05, '76 Tables | 7.5 GB | 2.58M Actions | Kimball Star Schema', 
            ha='center', va='center', fontsize=9)
    
    return_arrow = FancyArrowPatch((6, 4.2), (6, 10), 
                                  arrowstyle='->', mutation_scale=20, 
                                  linewidth=2, color='#E74C3C', 
                                  linestyle='dashed')
    ax.add_patch(return_arrow)
    ax.text(6.8, 7, 'Envelope\nResponse', fontsize=8, style='italic', 
            color='#E74C3C', ha='center')
    
    ax.text(5, 11.5, 'MCP Linguistic Exposure Layer Architecture', 
            ha='center', va='center', fontsize=16, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('/home/ubuntu/repos/nwsl-notes/docs/images/mcp-architecture.png', 
                dpi=300, bbox_inches='tight', facecolor='white')
    print("✓ Created: mcp-architecture.png")
    plt.close()

def create_tool_categories_visualization():
    """Create visualization of 38 tools organized by category."""
    fig, ax = plt.subplots(figsize=(14, 10))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 11)
    ax.axis('off')
    
    ax.text(7, 10.5, '38 MCP Research Tools by Category', 
            ha='center', va='center', fontsize=18, fontweight='bold')
    
    categories = {
        'Measurement & Observation (11 tools)': [
            'query_player_metrics', 'query_team_metrics', 'query_goalkeeper_metrics',
            'query_action_sequences', 'query_spatial_distribution', 'query_xT_values',
            'query_vaep_values', 'query_point_shares', 'query_match_events',
            'query_player_actions', 'query_team_possession'
        ],
        'Statistical Operations (4 tools)': [
            'calculate_distribution', 'calculate_correlation',
            'calculate_consistency', 'calculate_percentile_rank'
        ],
        'Temporal Analysis (3 tools)': [
            'query_time_series', 'compare_time_periods', 'query_sequence_patterns'
        ],
        'Comparative Analysis (3 tools)': [
            'compare_entities', 'compare_distributions', 'compare_cohorts'
        ],
        'Contextual Data Retrieval (4 tools)': [
            'query_match_context', 'query_player_context',
            'query_feature_vectors', 'query_ml_classifications'
        ]
    }
    
    colors = ['#D5F4E6', '#FFE5CC', '#E8F4F8', '#F9E79F', '#D4E6F1']
    y_positions = [9, 7, 5.2, 3.4, 1.6]
    
    for (category, tools), color, y_pos in zip(categories.items(), colors, y_positions):
        box_height = 0.2 + len(tools) * 0.15
        cat_box = FancyBboxPatch((0.5, y_pos - box_height), 13, box_height, 
                                 boxstyle="round,pad=0.05", 
                                 facecolor=color, 
                                 edgecolor='#2C3E50', linewidth=2)
        ax.add_patch(cat_box)
        
        ax.text(1, y_pos - 0.15, category, fontsize=12, fontweight='bold', 
                va='top')
        
        tools_per_col = 4
        col_width = 3.5
        for i, tool in enumerate(tools):
            col = i // tools_per_col
            row = i % tools_per_col
            x = 1.5 + col * col_width
            y = y_pos - 0.4 - row * 0.15
            ax.text(x, y, f'• {tool}', fontsize=8, va='top', 
                   family='monospace')
    
    legend_y = 0.5
    ax.text(7, legend_y, 'Research-Grade Characteristics:', 
            ha='center', fontsize=10, fontweight='bold')
    characteristics = [
        '✓ Standardized envelope responses',
        '✓ Provenance tracking (source tables, timestamps)',
        '✓ Schema metadata for all returned fields',
        '✓ Request fingerprints for reproducibility',
        '✓ Statistical rigor (confidence intervals, p-values)',
        '✓ No storytelling bias - measurements only'
    ]
    for i, char in enumerate(characteristics):
        ax.text(7, legend_y - 0.15 - i * 0.12, char, 
                ha='center', fontsize=8, style='italic')
    
    plt.tight_layout()
    plt.savefig('/home/ubuntu/repos/nwsl-notes/docs/images/tool-categories.png', 
                dpi=300, bbox_inches='tight', facecolor='white')
    print("✓ Created: tool-categories.png")
    plt.close()

def create_envelope_structure_diagram():
    """Create annotated diagram of the envelope response structure."""
    fig, ax = plt.subplots(figsize=(12, 10))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 11)
    ax.axis('off')
    
    ax.text(6, 10.5, 'MCP Envelope Response Structure', 
            ha='center', va='center', fontsize=18, fontweight='bold')
    
    json_example = {
        "kind": "table",
        "summary": "Top 10 players by offensive VAEP per 90",
        "data": {
            "columns": ["player_name", "offensive_vaep", "minutes_played"],
            "rows": [["Sophia Smith", 12.45, 2340], ["...more rows..."]]
        },
        "schema": {
            "offensive_vaep": {
                "type": "float",
                "description": "Offensive VAEP value"
            }
        },
        "meta": {
            "row_count": 10,
            "query_time_ms": 23,
            "season_year": 2024
        },
        "source": {
            "relation": "agg_player_season_vaep",
            "timestamp": "2025-10-30T12:34:56Z"
        },
        "request_fingerprint": "sha256:abc123..."
    }
    
    json_str = json.dumps(json_example, indent=2)
    
    json_box = FancyBboxPatch((0.5, 1), 5.5, 8.5, 
                              boxstyle="round,pad=0.1", 
                              facecolor='#F8F9FA', 
                              edgecolor='#2C3E50', linewidth=2)
    ax.add_patch(json_box)
    
    ax.text(1, 9, json_str, fontsize=7, family='monospace', 
            va='top', wrap=True)
    
    annotations = [
        (8.5, 9, 'kind', 'Response type:\ntable, image, object, or text'),
        (8.5, 8, 'summary', 'Human-readable description\nof what the data shows'),
        (8.5, 6.5, 'data', 'Actual payload:\nrows & columns for tables,\nURLs for images'),
        (8.5, 5, 'schema', 'Metadata about structure:\nfield types & descriptions'),
        (8.5, 3.5, 'meta', 'Contextual information:\nrow counts, performance,\nparameters used'),
        (8.5, 2.2, 'source', 'Provenance:\nwhich table, when queried'),
        (8.5, 1.3, 'request_fingerprint', 'Hash for caching &\nreproducibility')
    ]
    
    for x, y, field, description in annotations:
        arrow = FancyArrowPatch((x - 0.3, y), (6.2, y), 
                               arrowstyle='->', mutation_scale=15, 
                               linewidth=1.5, color='#E74C3C')
        ax.add_patch(arrow)
        
        ax.text(x, y + 0.2, f'"{field}"', fontsize=10, fontweight='bold', 
                color='#E74C3C')
        
        ax.text(x, y - 0.15, description, fontsize=8, va='top')
    
    ax.text(6, 0.3, 'Every MCP tool returns this standardized structure, enabling AI agents\n' +
                    'to understand responses without tool-specific parsing logic.', 
            ha='center', fontsize=9, style='italic', wrap=True)
    
    plt.tight_layout()
    plt.savefig('/home/ubuntu/repos/nwsl-notes/docs/images/envelope-structure.png', 
                dpi=300, bbox_inches='tight', facecolor='white')
    print("✓ Created: envelope-structure.png")
    plt.close()

def create_code_generation_example():
    """Create visualization of natural language to code generation."""
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 9)
    ax.axis('off')
    
    ax.text(6, 8.5, 'From Natural Language to Executable Code', 
            ha='center', va='center', fontsize=18, fontweight='bold')
    
    query_box = FancyBboxPatch((0.5, 6.5), 11, 1.5, 
                               boxstyle="round,pad=0.1", 
                               facecolor='#E8F4F8', 
                               edgecolor='#2C3E50', linewidth=2)
    ax.add_patch(query_box)
    ax.text(6, 7.5, 'User Query (Natural Language)', 
            ha='center', va='center', fontsize=12, fontweight='bold')
    ax.text(6, 7.1, '"Who had the highest offensive VAEP per 90 minutes in the 2024 season?"', 
            ha='center', va='center', fontsize=10, style='italic')
    
    arrow1 = FancyArrowPatch((6, 6.5), (6, 6), 
                            arrowstyle='->', mutation_scale=20, 
                            linewidth=2, color='#2C3E50')
    ax.add_patch(arrow1)
    ax.text(6.8, 6.25, 'AI Agent\nRouting', fontsize=8, style='italic')
    
    tool_box = FancyBboxPatch((0.5, 4.2), 11, 1.5, 
                              boxstyle="round,pad=0.1", 
                              facecolor='#D5F4E6', 
                              edgecolor='#27AE60', linewidth=2)
    ax.add_patch(tool_box)
    ax.text(6, 5.3, 'MCP Tool Invocation', 
            ha='center', va='center', fontsize=12, fontweight='bold')
    
    tool_call = '''query_player_metrics(
    metrics=["offensive_vaep", "minutes_played"],
    season_years=[2024],
    limit=10
)'''
    ax.text(6, 4.7, tool_call, ha='center', va='center', 
            fontsize=9, family='monospace')
    
    arrow2 = FancyArrowPatch((6, 4.2), (6, 3.7), 
                            arrowstyle='->', mutation_scale=20, 
                            linewidth=2, color='#2C3E50')
    ax.add_patch(arrow2)
    ax.text(6.8, 3.95, 'SQL\nGeneration', fontsize=8, style='italic')
    
    sql_box = FancyBboxPatch((0.5, 1.5), 11, 2, 
                             boxstyle="round,pad=0.1", 
                             facecolor='#F9E79F', 
                             edgecolor='#F39C12', linewidth=2)
    ax.add_patch(sql_box)
    ax.text(6, 3.2, 'Generated SQL Query', 
            ha='center', va='center', fontsize=12, fontweight='bold')
    
    sql_query = '''SELECT player_name, offensive_vaep, minutes_played,
       (offensive_vaep / (minutes_played / 90.0)) as offensive_vaep_per_90
FROM agg_player_season_vaep
WHERE season_year = 2024
ORDER BY offensive_vaep_per_90 DESC
LIMIT 10'''
    ax.text(6, 2.3, sql_query, ha='center', va='center', 
            fontsize=8, family='monospace')
    
    ax.text(6, 0.8, 'The MCP layer translates natural language into executable code,\n' +
                    'eliminating the need for users to know SQL or database schemas.', 
            ha='center', fontsize=9, style='italic')
    
    return_arrow = FancyArrowPatch((7.5, 1.5), (7.5, 6.5), 
                                  arrowstyle='->', mutation_scale=20, 
                                  linewidth=2, color='#E74C3C', 
                                  linestyle='dashed')
    ax.add_patch(return_arrow)
    ax.text(8.5, 4, 'Envelope\nResponse', fontsize=8, style='italic', 
            color='#E74C3C', ha='center')
    
    plt.tight_layout()
    plt.savefig('/home/ubuntu/repos/nwsl-notes/docs/images/code-generation.png', 
                dpi=300, bbox_inches='tight', facecolor='white')
    print("✓ Created: code-generation.png")
    plt.close()

if __name__ == '__main__':
    print("Generating images for Article 1...")
    create_mcp_architecture_diagram()
    create_tool_categories_visualization()
    create_envelope_structure_diagram()
    create_code_generation_example()
    print("\n✓ All images generated successfully!")
    print("Images saved to: /home/ubuntu/repos/nwsl-notes/docs/images/")
