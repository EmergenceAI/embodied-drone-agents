#!/bin/bash

# Check if gz command is available
if ! command -v gz &> /dev/null; then
    echo "gz command not found. Ensure Gazebo is installed and the gz command is available in your PATH."
    exit 1
fi

# Function to get pose of all models
get_poses() {
    echo "Listing models..."
    models=$(gz model --list 2>&1)

    # Print the models output for debugging
    echo "Models list output: $models"

    # Iterate over each model
    while IFS= read -r line; do
        echo "Processing line: $line"
        if [[ $line == *"["* ]]; then
            model_name=$(echo $line | cut -d '[' -f2 | cut -d ']' -f1)
            echo "Model name: $model_name"
            # Get pose of the model
            pose=$(gz model --model "$model_name" --pose 2>&1)
            echo "Pose output: $pose"
            echo "Model: $model_name"
            echo "$pose"
        fi
    done <<< "$models"
}

get_poses
