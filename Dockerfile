FROM centos

USER root

ENV LOG_DIR=/var/log/confluent 

EXPOSE 8081

RUN rpm --import https://packages.confluent.io/rpm/5.2/archive.key 

COPY ./confluent.repo /etc/yum.repos.d/ 

RUN yum install -y --setopt=tsflags=nodocs confluent-schema-registry && \
  chown -R :0 /usr/bin/schema-registry-start -R && \
  chown -R :0 /usr/bin/schema-registry-stop -R && \
  chown -R :0 /usr/bin/schema-registry-run-class -R && \
  chown -R :0 /usr/bin/schema-registry-stop-service -R && \
  chown -R :0 /etc/schema-registry/schema-registry.properties -R && \
  chown -R :0 /var/log/confluent -R && \
  yum clean all -y

COPY ./schema-registry.properties /etc/schema-registry/ 

CMD ["schema-registry-start", "/etc/schema-registry/schema-registry.properties"]
