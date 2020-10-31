FROM python:3-slim
MAINTAINER x0rzkov <x0rzkov@protonmail.com>

WORKDIR /opt/service

RUN apt-get update && \
    apt-get install -y --no-install-recommends ca-certificates git nano bash gcc g++ unzip

RUN python3 -m pip install -U pip && \
    pip3 install --no-cache git+https://github.com/boudinfl/pke && \
    pip3 install --no-cache git+https://github.com/LIAAD/yake.git && \
    pip3 install --no-cache langcodes && \
    pip3 install --no-cache flask && \
    pip3 install --no-cache flask-cors && \
    pip3 install --no-cache simplejson && \
    python3 -m spacy download en && \
    python3 -m spacy download es && \
    python3 -m spacy download fr && \
    python3 -m spacy download pt && \
    python3 -m spacy download de && \
    python3 -m spacy download it && \
    python3 -m spacy download nl && \
    python3 -m spacy download el

nltk.download('treebank', download_dir='/mnt/data/treebank')

RUN git clone --depth=1 https://github.com/LIAAD/KeywordExtractor-Datasets /opt/shared && \
    cd /opt/shared  && \
    find . -name '*.zip' -exec sh -c 'unzip -d Datasets {}' ';'  && \
    rm -fR /opt/shared/datasets

RUN python3 -m nltk.downloader stopwords -d /opt/shared/stopwords

VOLUME ["/opt/shared"]

COPY . .

RUN pip3 install -e .

EXPOSE 5009

CMD ["python3", "server.py"]
