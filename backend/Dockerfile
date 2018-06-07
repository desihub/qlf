FROM ubuntu
RUN mkdir /app
WORKDIR /app
ADD . /app/
ENV QLF_ROOT /app

# BEGIN INSTALL: miniconda3
RUN apt-get update --fix-missing && apt-get install -y wget bzip2 ca-certificates \
    libglib2.0-0 libxext6 libsm6 libxrender1 git

RUN apt-get install -y locales && locale-gen en_US.UTF-8  
ENV LANG en_US.UTF-8  
ENV LANGUAGE en_US:en  
ENV LC_ALL en_US.UTF-8

RUN echo 'export PATH=/opt/conda/bin:$PATH' > /etc/profile.d/conda.sh && \
    wget --quiet https://repo.continuum.io/miniconda/Miniconda3-4.3.27-Linux-x86_64.sh -O ~/miniconda.sh && \
    /bin/bash ~/miniconda.sh -b -p /opt/conda && \
    rm ~/miniconda.sh

RUN apt-get install -y curl grep sed dpkg && \
    TINI_VERSION=`curl https://github.com/krallin/tini/releases/latest | grep -o "/v.*\"" | sed 's:^..\(.*\).$:\1:'` && \
    curl -L "https://github.com/krallin/tini/releases/download/v${TINI_VERSION}/tini_${TINI_VERSION}.deb" > tini.deb && \
    dpkg -i tini.deb && \
    rm tini.deb && \
    apt-get clean

ENV PATH /opt/conda/bin:$PATH

ENTRYPOINT [ "/usr/bin/tini", "--" ]
# END INSTALL: miniconda3

# BEGIN INSTALL: dependencies
RUN /bin/bash -c "source /opt/conda/bin/activate root && \
        conda update conda -y && \ 
		conda config --add channels conda-forge && \
		conda create --name quicklook python=3.5 --yes --file requirements.txt && \
		source /opt/conda/bin/activate quicklook && \
        apt-get install build-essential -y && \
		pip install -r extras.txt"
# END INSTALL: dependencies

EXPOSE 8000
 
CMD [ "/bin/bash" ]
