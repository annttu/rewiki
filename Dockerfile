FROM python:3.7-alpine as baseimage
ENV USER=rewiki
ENV UID=986
ENV GID=986
RUN addgroup --gid "$GID" "$USER"
RUN adduser --disabled-password --gecos "" --home "$(pwd)" --ingroup "$USER" --no-create-home --uid "$UID"  "$USER"
COPY . /rewiki
RUN mkdir /rewiki/files
RUN pip install --trusted-host pypi.python.org -r /rewiki/requirements.txt
RUN apk add --no-cache git

FROM baseimage as rewiki
WORKDIR /rewiki
EXPOSE 8080
RUN chown rewiki:rewiki /rewiki/files
USER rewiki
ENTRYPOINT ["/rewiki/server.py"]

