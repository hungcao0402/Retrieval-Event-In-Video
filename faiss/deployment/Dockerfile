FROM nvidia/cuda:11.2.2-devel-ubuntu20.04


RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

ENV CONDA_DIR /opt/conda
RUN curl -o /miniconda.sh -O https://repo.anaconda.com/miniconda/Miniconda3-py38_4.10.3-Linux-x86_64.sh \
    && chmod +x /miniconda.sh \
    && /miniconda.sh -b -p ${CONDA_DIR} \
    && rm /miniconda.sh

ENV PATH=$CONDA_DIR/bin:$PATH
ENV TZ=Asia/Ho_Chi_Minh

RUN conda install -c pytorch -c nvidia faiss-gpu=1.7.4 mkl=2021 blas=1.0=mkl
RUN pip install fastapi pyaml uvicorn
COPY ./deployment/requirements.txt .
RUN pip install -r requirements.txt
RUN pip install torch==1.10.0+cu111 torchvision==0.11.0+cu111 torchaudio==0.10.0 -f https://download.pytorch.org/whl/torch_stable.html
RUN pip install git+https://github.com/openai/CLIP.git
# RUN pip install salesforce-lavis

WORKDIR /home
