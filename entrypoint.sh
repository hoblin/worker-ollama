#!/bin/bash
./start.sh &
exec "/bin/ollama serve"
