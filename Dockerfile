FROM pytorch/pytorch:1.11.0-cuda11.3-cudnn8-runtime

RUN apt-get update -qq \
    && apt-get install -yqq --no-install-recommends \
        git wget nvidia-utils-440 \
        gcc g++ nano \
    && apt-get clean -y \
    && rm -rf /var/lib/apt/lists/* \
    && ln -s /usr/bin/python3 /usr/bin/python

ENV PATH /opt/conda/bin:$PATH

RUN conda create -n muss python=3.7 cudatoolkit cudnn gunicorn -y \
    \
    && useradd --home /home/muss --create-home --shell /bin/bash --uid 2001 muss \
    && chown -R muss:muss /home/muss

USER muss
WORKDIR /home/muss

RUN git clone --quiet --depth 1 https://github.com/cleyrop/muss.git -b unapei-ia \
    && cd muss \
    && sed -i 's/git+git/git+https/g' requirements.txt \
    && sed -i 's#^fairseq.*#fairseq@ git+https://github.com/cleyrop/fairseq.git@v0.10.2.0#' requirements.txt \
    && rm -rf .git* \
    && cd .. \
    && conda init bash \
    && sed -i '/# If not running interactively/,+5d' ~/.bashrc \
    && echo 'conda activate muss' >> ~/.bashrc \
    && echo 'cd muss' >> ~/.bashrc \
    && echo 'if [ -f ~/.bashrc ]; then' >> ~/.bash_profile \
    && echo '  . ~/.bashrc' >> ~/.bash_profile \
    && echo 'fi' >> ~/.bash_profile

ENV FLASK_APP=muss
ENV FLASK_ENV=production

COPY resources/entrypoint /entrypoint
COPY --chown=muss resources/scripts/api.py /home/muss/muss/scripts/
COPY --chown=muss resources/scripts/simplify.py /home/muss/muss/scripts/
COPY --chown=muss resources/muss/simplify.py /home/muss/muss/muss/
COPY --chown=muss resources/gunicorn.conf.py /usr/local/etc/

ENTRYPOINT ["/entrypoint"]
CMD ["tail", "-f", "/dev/null"]
