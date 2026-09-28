from typing import Dict, Any, List

def calculate_panel_layout(panels: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Computes comic layout metadata for each panel:
    - Grid column spans (e.g. hero panels can span 2 columns on 2-column or 3-column grids)
    - Speech bubble alignment (alternates for visual rhythm)
    - Sound effect sticker positions and angles
    """
    total = len(panels)
    positioned_panels = []
    
    bubble_positions = ["bubble-top-left", "bubble-top-right", "bubble-bottom-left", "bubble-bottom-right"]
    badge_rotations = [-12, 8, -6, 14, -10, 5]
    
    for i, panel in enumerate(panels):
        panel_copy = dict(panel)
        
        # Grid span calculation
        span_class = "col-span-1"
        if total in (3, 5) and (i == 0 or i == total - 1):
            span_class = "col-span-full md:col-span-2"
        elif total == 1:
            span_class = "col-span-full"
            
        panel_copy["grid_span"] = span_class
        panel_copy["bubble_position"] = bubble_positions[i % len(bubble_positions)]
        panel_copy["badge_rotation"] = badge_rotations[i % len(badge_rotations)]
        
        positioned_panels.append(panel_copy)
        
    return positioned_panels
