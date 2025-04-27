"""
Module for automatically saving annotations in JSON and HTML formats.
"""
import json
import os
import pandas as pd
from datetime import datetime

def save_annotations(annotations_df, model_name, word, corpus_name, output_dir, metrics=None):
    """
    Save annotations from a DataFrame to JSON and HTML formats.
    
    Args:
        annotations_df (pd.DataFrame): DataFrame containing the annotations
        model_name (str): Name of the model used for annotations
        word (str): Word that was analyzed
        corpus_name (str): Name of the corpus
        output_dir (str): Directory to save the output files
        metrics (dict, optional): Dictionary containing evaluation metrics
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Format current date
    current_date = datetime.now().strftime("%d/%m/%Y")
    
    # Determine the model category column
    model_category_column = None
    possible_model_columns = [
        f"annotations_{model_name}_{word}_{corpus_name}", 
        "GPT_CATEGORY",
        f"annotations_{model_name}",
        "model_category",
        "category",
        "PRED"
    ]
    
    # Find the first matching column that exists in the DataFrame
    for col in possible_model_columns:
        if col in annotations_df.columns:
            model_category_column = col
            print(f"Using column '{model_category_column}' for model predictions")
            break
    
    if not model_category_column and len(annotations_df.columns) > 0:
        # If we couldn't find a matching column, look for any column that might contain annotations
        for col in annotations_df.columns:
            if any(term in col.lower() for term in ["gpt", "model", "pred", "category", "annotation"]):
                model_category_column = col
                print(f"Found potential model category column: '{model_category_column}'")
                break
    
    if not model_category_column:
        print("Warning: Could not find model category column. Using empty values.")
    
    # Extract ALL annotations for summary (not just the first 10)
    all_annotations = []
    
    for i, row in annotations_df.iterrows():
        # Extract human category
        human_category = row.get('HUMAN', '')
        
        # Extract model category
        model_category = ''
        if model_category_column:
            model_category = row.get(model_category_column, '')
        
        # Extract the text containing the word
        text = row.get('concatenated_text', '')
        if not text and 'Concordance' in annotations_df.columns:
            text = row.get('Concordance', '')
        
        all_annotations.append({
            "id": i + 1,
            "text": text,
            "human_category": human_category,
            "model_category": model_category,
            "match": human_category == model_category if human_category and model_category else False
        })
    
    # Calculate category distribution
    category_counts = {}
    if 'HUMAN' in annotations_df.columns:
        category_counts = annotations_df['HUMAN'].value_counts().to_dict()
    
    # Create JSON structure
    json_data = {
        "model": model_name,
        "word_analyzed": word,
        "corpus": corpus_name,
        "date": current_date,
        "total_samples": len(annotations_df),
        "annotations": all_annotations
    }
    
    # Add metrics if provided
    if metrics:
        json_data["global_metrics"] = metrics
    
    # Add category distribution
    json_data["category_distribution"] = category_counts
    
    # Write to JSON file - use corpus name in the filename
    json_path = os.path.join(output_dir, f"annotations_{corpus_name}_summary.json")
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, indent=2, ensure_ascii=False)
    
    # Generate HTML - use corpus name in the filename
    html_path = os.path.join(output_dir, f"annotations_{corpus_name}_viewer.html")
    generate_html_viewer(json_data, html_path)
    
    print(f"Annotations saved to {json_path} and {html_path}")
    
    return json_path, html_path

def generate_html_viewer(data, output_path):
    """
    Generate an HTML file to view annotations.
    
    Args:
        data (dict): JSON data structure
        output_path (str): Path to save the HTML file
    """
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Annotations for '{data["word_analyzed"]}' - {data["corpus"]} ({data["model"]})</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 20px;
            color: #333;
        }}
        h1, h2, h3 {{
            color: #2c3e50;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
        }}
        .header {{
            background-color: #f8f9fa;
            padding: 20px;
            border-radius: 5px;
            margin-bottom: 20px;
        }}
        .metrics {{
            display: flex;
            flex-wrap: wrap;
            gap: 20px;
            margin-bottom: 20px;
        }}
        .metric-card {{
            background-color: #fff;
            border: 1px solid #ddd;
            border-radius: 5px;
            padding: 15px;
            flex: 1;
            min-width: 200px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .annotations {{
            margin-bottom: 30px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 20px;
        }}
        th, td {{
            padding: 12px 15px;
            border: 1px solid #ddd;
            text-align: left;
        }}
        th {{
            background-color: #f8f9fa;
            font-weight: bold;
        }}
        tr:nth-child(even) {{
            background-color: #f8f9fa;
        }}
        .match-true {{
            background-color: #d4edda;
        }}
        .match-false {{
            background-color: #f8d7da;
        }}
        .highlight {{
            font-weight: bold;
            background-color: #ffeeba;
            padding: 2px 4px;
            border-radius: 3px;
        }}
        .category-distribution {{
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            margin-bottom: 20px;
        }}
        .category-chip {{
            background-color: #e9ecef;
            padding: 8px 12px;
            border-radius: 16px;
            font-size: 14px;
        }}
        #searchInput {{
            width: 100%;
            padding: 10px;
            margin-bottom: 20px;
            border: 1px solid #ddd;
            border-radius: 4px;
            font-size: 16px;
        }}
        .pagination {{
            display: flex;
            justify-content: center;
            margin-top: 20px;
            margin-bottom: 40px;
        }}
        .pagination button {{
            margin: 0 5px;
            padding: 8px 15px;
            background-color: #f8f9fa;
            border: 1px solid #ddd;
            border-radius: 4px;
            cursor: pointer;
        }}
        .pagination button.active {{
            background-color: #007bff;
            color: white;
            border-color: #007bff;
        }}
        .pagination button:hover:not(.active) {{
            background-color: #e9ecef;
        }}
        .controls {{
            margin-bottom: 20px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Semantic Analysis: '{data["word_analyzed"]}' - {data["corpus"]}</h1>
            <p>Model: <strong>{data["model"]}</strong> | Date: {data["date"]} | Samples: {data["total_samples"]}</p>
        </div>
"""
    
    # Add metrics if available
    if "global_metrics" in data:
        html_content += """
        <h2>Global Metrics</h2>
        <div class="metrics">
"""
        for metric, value in data["global_metrics"].items():
            formatted_value = f"{value:.4f}" if isinstance(value, float) else str(value)
            html_content += f"""
            <div class="metric-card">
                <h3>{metric.replace('_', ' ').title()}</h3>
                <p style="font-size: 24px; font-weight: bold;">{formatted_value}</p>
            </div>
"""
        html_content += """
        </div>
"""
    
    # Add category distribution
    if "category_distribution" in data:
        html_content += """
        <h2>Category Distribution</h2>
        <div class="category-distribution">
"""
        for category, count in data["category_distribution"].items():
            html_content += f"""
            <div class="category-chip">
                {category}: {count}
            </div>
"""
        html_content += """
        </div>
"""
    
    # Add search and pagination controls
    html_content += """
        <h2>Annotations</h2>
        <div class="controls">
            <input type="text" id="searchInput" placeholder="Search in annotations...">
            <div>
                <label>
                    <input type="checkbox" id="showMismatchesOnly"> 
                    Show Mismatches Only
                </label>
            </div>
        </div>
        <div class="annotations">
            <table id="annotationsTable">
                <thead>
                    <tr>
                        <th>#</th>
                        <th>Text</th>
                        <th>Human Category</th>
                        <th>Model Category</th>
                        <th>Match</th>
                    </tr>
                </thead>
                <tbody>
"""
    
    # Add all annotations to HTML
    for item in data["annotations"]:
        # Highlight the word or its variants in the text
        text = item["text"] if item["text"] else ""
        word = data["word_analyzed"]
        for variant in [word, f"{word}ed", f"{word}ing", f"{word}s"]:
            if variant in text.lower():
                text = text.replace(variant, f'<span class="highlight">{variant}</span>')
                text = text.replace(variant.capitalize(), f'<span class="highlight">{variant.capitalize()}</span>')
        
        match_class = "match-true" if item["match"] else "match-false"
        
        html_content += f"""
                    <tr class="{match_class}">
                        <td>{item["id"]}</td>
                        <td>{text}</td>
                        <td>{item["human_category"]}</td>
                        <td>{item["model_category"]}</td>
                        <td>{'✅' if item["match"] else '❌'}</td>
                    </tr>
"""
    
    html_content += """
                </tbody>
            </table>
        </div>
        <div class="pagination" id="pagination"></div>
"""
    
    # Add common errors if available
    if "common_errors" in data:
        html_content += """
        <h2>Common Errors</h2>
        <ul>
"""
        for error in data["common_errors"]:
            html_content += f"""
            <li>
                <strong>{error["type"]}</strong> ({error["count"]} instances)<br>
                Example: "{error["example"]}"
            </li>
"""
        html_content += """
        </ul>
"""
    
    # Add JavaScript for search and pagination
    html_content += """
    <script>
        document.addEventListener('DOMContentLoaded', function() {
            // Variables
            const table = document.getElementById('annotationsTable');
            const rows = table.getElementsByTagName('tr');
            const searchInput = document.getElementById('searchInput');
            const mismatchesCheckbox = document.getElementById('showMismatchesOnly');
            const paginationContainer = document.getElementById('pagination');
            
            const rowsPerPage = 15;
            let currentPage = 1;
            let filteredRows = [];
            
            // Initial setup
            function initializePagination() {
                updateFilteredRows();
                displayRows();
                setupPagination();
            }
            
            // Update filtered rows based on search and filter
            function updateFilteredRows() {
                filteredRows = [];
                const searchTerm = searchInput.value.toLowerCase();
                const showMismatchesOnly = mismatchesCheckbox.checked;
                
                // Start from index 1 to skip the header row
                for (let i = 1; i < rows.length; i++) {
                    const row = rows[i];
                    const text = row.textContent.toLowerCase();
                    const isMatch = row.classList.contains('match-true');
                    
                    // Apply filters
                    const matchesSearch = !searchTerm || text.includes(searchTerm);
                    const matchesMismatchFilter = !showMismatchesOnly || !isMatch;
                    
                    if (matchesSearch && matchesMismatchFilter) {
                        filteredRows.push(row);
                    }
                    
                    // Hide all rows initially
                    row.style.display = 'none';
                }
            }
            
            // Display rows for current page
            function displayRows() {
                const start = (currentPage - 1) * rowsPerPage;
                const end = start + rowsPerPage;
                
                for (let i = 0; i < filteredRows.length; i++) {
                    if (i >= start && i < end) {
                        filteredRows[i].style.display = '';
                    } else {
                        filteredRows[i].style.display = 'none';
                    }
                }
            }
            
            // Setup pagination buttons
            function setupPagination() {
                paginationContainer.innerHTML = '';
                const pageCount = Math.ceil(filteredRows.length / rowsPerPage);
                
                // No need for pagination if only one page
                if (pageCount <= 1) {
                    return;
                }
                
                // Previous button
                if (currentPage > 1) {
                    const prevButton = document.createElement('button');
                    prevButton.innerHTML = '&laquo; Prev';
                    prevButton.addEventListener('click', function() {
                        currentPage--;
                        displayRows();
                        setupPagination();
                    });
                    paginationContainer.appendChild(prevButton);
                }
                
                // Page buttons
                let startPage = Math.max(1, currentPage - 2);
                let endPage = Math.min(pageCount, startPage + 4);
                
                if (endPage - startPage < 4) {
                    startPage = Math.max(1, endPage - 4);
                }
                
                for (let i = startPage; i <= endPage; i++) {
                    const button = document.createElement('button');
                    button.textContent = i;
                    
                    if (i === currentPage) {
                        button.classList.add('active');
                    }
                    
                    button.addEventListener('click', function() {
                        currentPage = i;
                        displayRows();
                        setupPagination();
                    });
                    
                    paginationContainer.appendChild(button);
                }
                
                // Next button
                if (currentPage < pageCount) {
                    const nextButton = document.createElement('button');
                    nextButton.innerHTML = 'Next &raquo;';
                    nextButton.addEventListener('click', function() {
                        currentPage++;
                        displayRows();
                        setupPagination();
                    });
                    paginationContainer.appendChild(nextButton);
                }
            }
            
            // Event listeners
            searchInput.addEventListener('input', function() {
                currentPage = 1;
                initializePagination();
            });
            
            mismatchesCheckbox.addEventListener('change', function() {
                currentPage = 1;
                initializePagination();
            });
            
            // Initialize
            initializePagination();
        });
    </script>
"""
    
    html_content += """
    </div>
</body>
</html>
"""
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content) 