FROM ubuntu:20.04
ARG DEBIAN_FRONTEND=noninteractive

# Install prerequisites
RUN apt update && \
	apt install -y \
        git \
        make \
        llvm \
        clang \
        autoconf \
        libtool \
        automake \
        python3 \
        python3.9-dev \
        pkg-config \
        vim

# Set AFL_NO_X86 environment variable
ENV AFL_NO_X86=1

# Clone and build AFL
RUN git clone https://github.com/google/AFL --branch v2.57b && \
    cd /AFL/ && make -j4 && \
    cd /AFL/llvm_mode && make -j4

# Clone libxml2
RUN git clone https://github.com/GNOME/libxml2/ --branch v2.8.0

# Copy harnesses to libxml2 directory
COPY harness.c harness2.c /libxml2/
