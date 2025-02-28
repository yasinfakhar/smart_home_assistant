#!/bin/bash

# Check and activate the virtual environment
if [ -d "venv" ]; then
  source venv/bin/activate
else
  echo "Error: Virtual environment folder 'venv' not found."
  exit 1
fi

# Start the first script in the background
python app.py &
pid1=$!

# Start the streamlit app in the background
streamlit run app.py &
pid2=$!

# Wait for all background processes to finish
wait $pid1 $pid2
