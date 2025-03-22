# Urban Economic Efficiency Dashboard

This Streamlit dashboard analyzes economic productivity across global metropolitan areas, focusing on GDP per capita as a key efficiency metric.

## Overview

The dashboard visualizes and analyzes metropolitan GDP data, exploring:

- Global distribution of economic productivity
- Top performing metropolitan areas
- Relationship between city size and economic efficiency
- Regional patterns and outliers
- Factors influencing urban economic productivity

## Getting Started

### Prerequisites

- Python 3.8+
- pip (Python package installer)

### Installation

1. Clone this repository or download the files
2. Install the required packages:

```bash
pip install -r requirements.txt
```

### Running the Dashboard

Launch the Streamlit app by running:

```bash
streamlit run app.py
```

The dashboard will open in your default web browser at http://localhost:8501

## Features

- **Interactive Map Visualization**: Explore metropolitan areas globally with bubble sizes representing total GDP and colors showing GDP per capita
- **Top Performers Analysis**: Examine the most economically efficient cities and what makes them successful
- **Size-Efficiency Relationship**: Visualize how population size relates to economic productivity
- **Regional Comparisons**: Compare economic efficiency across geographic regions
- **Outliers Analysis**: Identify cities that significantly outperform their regional peers

## Data Source

The dashboard uses the `dataset.csv` file containing information about metropolitan areas including:
- Metropolitan area name
- Country/region
- Official estimated GDP (in billion US$)
- Metropolitan population

## Customization

You can modify the dashboard by:
- Updating the dataset with more recent data
- Adjusting visualizations in the `app.py` file
- Customizing the styling in the `style.css` file

## Why This Approach?

This Streamlit dashboard provides a flexible, code-based alternative to traditional BI tools like Power BI or Tableau. Key advantages include:

- **Lower barrier to entry**: Simpler learning curve compared to specialized BI tools
- **Flexibility**: Complete control over visualizations and analysis
- **AI assistance**: Leverage AI tools to help with code development
- **Python ecosystem**: Access to powerful data science libraries
- **Version control**: Easy to track changes with git
- **Open source**: No licensing costs or vendor lock-in

Perfect for data analysts who want powerful visualizations without the steep learning curve of traditional BI tools. 