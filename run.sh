docker run -it --rm -p 8080:8080 sentence_sim

# -it creates an interactive bash shell in the container
# --rm Automatically removes the container when it exits 
# -p exposes the container port (the latter) to TCP port of the host machine (former)