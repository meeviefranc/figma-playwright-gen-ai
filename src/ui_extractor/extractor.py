class UIExtractor:
    def __init__(self, figma_data):
        self.figma_data = figma_data

    def extract_ui_elements(self):
        """Extract UI elements grouped by frame"""
        frames = {}
        
        if not self.figma_data:
            return frames
            
        for element in self.figma_data:
            self._process_element(element, frames)
        
        return frames

    def _process_element(self, element, frames, parent_frame=None):
        """Process each element and group by frame"""
        element_type = element.get('type', '')
        element_name = element.get('name', 'Unnamed')
        
        # If this is a frame, create a new group
        if element_type == 'FRAME':
            frame_name = element_name
            if frame_name not in frames:
                frames[frame_name] = {
                    'frame_info': self._extract_element(element),
                    'elements': [],
                    'is_table': self._is_data_table(element),
                    'table_rows': [] if self._is_data_table(element) else None
                }
            current_frame = frame_name
        else:
            current_frame = parent_frame
        
        # Extract interactive elements
        if element_type in ['COMPONENT', 'INSTANCE', 'TEXT', 'RECTANGLE', 'ELLIPSE']:
            extracted = self._extract_element(element)
            if current_frame and current_frame in frames:
                frames[current_frame]['elements'].append(extracted)
            elif current_frame is None:
                # Create a default frame for orphaned elements
                if 'Default' not in frames:
                    frames['Default'] = {'frame_info': {}, 'elements': [], 'is_table': False, 'table_rows': None}
                frames['Default']['elements'].append(extracted)
        
        # Process children recursively
        if 'children' in element:
            for child in element['children']:
                self._process_element(child, frames, current_frame)
        
        # Post-process: Group elements by rows if this is a data table
        if current_frame and current_frame in frames and frames[current_frame]['is_table']:
            self._group_elements_by_rows(frames[current_frame])

    def _is_data_table(self, element):
        """Determine if a frame contains a data table"""
        element_name = element.get('name', '').lower()
        
        # Check if frame name suggests it's a table
        table_indicators = ['table', 'data', 'grid', 'list', 'row', 'column', 'data table']
        if any(indicator in element_name for indicator in table_indicators):
            return True
        
        # Specific check for exact "data table" match (case-insensitive)
        if element_name == 'data table':
            return True
        
        # Check if children have table-like structure
        children = element.get('children', [])
        if len(children) < 2:
            return False
        
        # Look for repeated row-like structures
        row_count = 0
        for child in children:
            child_name = child.get('name', '').lower()
            if 'row' in child_name or child.get('type') == 'FRAME':
                row_count += 1
        
        # If we have multiple rows, likely a table
        return row_count >= 2

    def _group_elements_by_rows(self, frame_data):
        """Group table elements by rows based on Y position"""
        elements = frame_data['elements']
        if not elements:
            return
        
        # Sort elements by Y position (top to bottom)
        sorted_elements = sorted(elements, key=lambda el: el['properties'].get('y', 0))
        
        # Group elements into rows based on similar Y positions
        rows = []
        current_row = []
        current_y = None
        y_tolerance = 10  # Pixels tolerance for same row
        
        for element in sorted_elements:
            element_y = element['properties'].get('y', 0)
            
            if current_y is None or abs(element_y - current_y) <= y_tolerance:
                # Same row
                current_row.append(element)
                current_y = element_y if current_y is None else current_y
            else:
                # New row
                if current_row:
                    # Sort current row by X position (left to right)
                    current_row.sort(key=lambda el: el['properties'].get('x', 0))
                    rows.append({
                        'row_index': len(rows) + 1,
                        'y_position': current_y,
                        'elements': current_row
                    })
                current_row = [element]
                current_y = element_y
        
        # Add the last row
        if current_row:
            current_row.sort(key=lambda el: el['properties'].get('x', 0))
            rows.append({
                'row_index': len(rows) + 1,
                'y_position': current_y,
                'elements': current_row
            })
        
        frame_data['table_rows'] = rows
        
        # Add row information to each element
        for row in rows:
            for element in row['elements']:
                element['row_info'] = {
                    'row_index': row['row_index'],
                    'y_position': row['y_position'],
                    'column_index': row['elements'].index(element) + 1
                }

    def _extract_element(self, element):
        """Extract element information"""
        return {
            'id': element.get('id', ''),
            'name': element.get('name', ''),
            'type': element.get('type', ''),
            'properties': self._get_properties(element),
            'row_info': None  # Will be populated for table elements
        }

    def _get_properties(self, element):
        """Extract element properties"""
        properties = {}
        if 'absoluteBoundingBox' in element:
            bbox = element['absoluteBoundingBox']
            properties.update({
                'x': bbox.get('x', 0),
                'y': bbox.get('y', 0),
                'width': bbox.get('width', 0),
                'height': bbox.get('height', 0)
            })
        
        # Add text content if available
        if 'characters' in element:
            properties['text'] = element['characters']
            
        return properties