FROM centos

USER root

RUN yum install -y \
       java-1.8.0-openjdk \
       java-1.8.0-openjdk-devel

ENV JAVA_HOME /etc/alternatives/jre

LABEL maintainer.group="Open DataHub" \
	  maintainer.email="vsahu@redhat.com"

RUN yum install curl which -y

RUN rpm --import https://packages.confluent.io/rpm/5.2/archive.key

COPY ./confluent.repo /etc/yum.repos.d/

RUN yum clean all && yum install confluent-platform-2.12 -y

COPY ./schema-registry.properties /etc/schema-registry/


CMD ["schema-registry-start", "/etc/schema-registry/schema-registry.properties"]
