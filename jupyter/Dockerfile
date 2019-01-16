FROM jupyter/base-notebook
COPY . /app
USER 0
RUN apt-get update && apt-get install -y git
RUN git clone https://github.com/desihub/qlf.git /app/qlf
WORKDIR /app/notebooks
RUN pip install -r /app/requirements.txt
USER 1000
CMD ["/bin/bash"]