FROM python:3.7.10-slim-buster
# Only necessary pip install would be flask
RUN pip install flask

#Possibly create WORKDIR - TODO

# Add Flask App
ADD app.py /
ADD utils.py / 

# Expose a Port to run the application on
EXPOSE 8080 

#Run the following command at container start up
CMD ["python3", "-u", "app.py"]