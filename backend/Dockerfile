FROM ubuntu
RUN mkdir /app
WORKDIR /app
ADD . /app/
RUN useradd -d /home/quicklook -m quicklook
RUN chgrp -R quicklook /app
RUN chmod -R g+w /app
ENV QLF_ROOT /app

# BEGIN INSTALL: anaconda3
RUN apt-get update --fix-missing && apt-get install -y wget bzip2 ca-certificates \
    libglib2.0-0 libxext6 libsm6 libxrender1 git build-essential htop

RUN apt-get install -y locales && locale-gen en_US.UTF-8  
ENV LANG en_US.UTF-8  
ENV LANGUAGE en_US:en  
ENV LC_ALL en_US.UTF-8

RUN echo 'export PATH=/conda/bin:$PATH' > /etc/profile.d/conda.sh && \
    wget --quiet https://repo.anaconda.com/archive/Anaconda3-5.1.0-Linux-x86_64.sh -O ~/anaconda.sh && \
    /bin/bash ~/anaconda.sh -b -p /conda && \
    rm ~/anaconda.sh

RUN apt-get install -y curl grep sed dpkg && \
    TINI_VERSION=`curl https://github.com/krallin/tini/releases/latest | grep -o "/v.*\"" | sed 's:^..\(.*\).$:\1:'` && \
    curl -L "https://github.com/krallin/tini/releases/download/v${TINI_VERSION}/tini_${TINI_VERSION}.deb" > tini.deb && \
    dpkg -i tini.deb && \
    rm tini.deb && \
    apt-get clean

ENV PATH /conda/bin:$PATH

ENTRYPOINT [ "/usr/bin/tini", "--" ]
# END INSTALL: Anaconda3

# BEGIN INSTALL: dependencies
# RUN /bin/bash -c "source /conda/bin/activate root && \
#     conda update conda -y && \ 
# 		conda create --name quicklook python=3.6 --yes --file requirements.txt && \
# 		source /conda/bin/activate quicklook && \
# 		pip install -r extras.txt"

RUN /bin/bash -c "pip install pip --upgrade"
RUN /bin/bash -c "conda install -y --file requirements.txt && \
    pip install -r extras.txt"

# END INSTALL: dependencies
EXPOSE 8000
USER quicklook
CMD [ "/bin/bash" ]
