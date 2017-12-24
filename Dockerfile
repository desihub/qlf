FROM ubuntu
RUN mkdir /app
WORKDIR /app
ADD . /app/
ENV QLF_ROOT /app

# BEGIN INSTALL: miniconda3
ENV LANG=C.UTF-8 LC_ALL=C.UTF-8

RUN apt-get update --fix-missing && apt-get install -y wget bzip2 ca-certificates \
    libglib2.0-0 libxext6 libsm6 libxrender1 git

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

ENV PATH=$QLF_ROOT/desispec/bin:$PATH PYTHONPATH=$QLF_ROOT/desispec/py:$PYTHONPATH

ENV PATH=$QLF_ROOT/desiutil/bin:$PATH PYTHONPATH=$QLF_ROOT/desiutil/py:$PYTHONPATH

ENV DESI_SPECTRO_DATA=$QLF_ROOT/spectro/data DESI_SPECTRO_REDUX=$QLF_ROOT/spectro/redux

RUN cp $QLF_ROOT/framework/config/qlf.cfg.template $QLF_ROOT/framework/config/qlf.cfg

ENV DESI_SPECTRO_DATA=$QLF_ROOT/spectro/data DESI_SPECTRO_REDUX=$QLF_ROOT/spectro/redux
ENV QL_SPEC_DATA=$DESI_SPECTRO_DATA QL_SPEC_REDUX=$DESI_SPECTRO_REDUX OMP_NUM_THREADS=1

EXPOSE 8000
 
CMD [ "/bin/bash" ]
