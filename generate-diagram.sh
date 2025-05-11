#!/bin/bash

# Create output directory if it doesn't exist
mkdir -p diagrams

# Generate PNG diagram using PlantUML CLI
plantuml -tpng database-architecture.puml -o diagrams

echo "Diagram generated at diagrams/database-architecture.png" 