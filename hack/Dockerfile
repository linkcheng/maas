FROM rockylinux:8

# 一次性安装所有依赖
RUN yum install -y epel-release && \
    yum install -y wget xz net-tools curl telnet gcc gcc-c++ make \
    ncurses-devel gdbm-devel xz-devel sqlite-devel tk-devel libuuid-devel \
    readline-devel bzip2-devel libffi-devel openssl openssl-devel cronie crontabs && \
    rm -f /etc/localtime && \
    ln -s /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && \
    yum clean all && \
    rm -rf /var/cache/yum

# 设置环境变量
ENV PY_VERSION="3.12.9" \
    PYTHON_DIR=/usr/local/python3 \
    PATH=/usr/local/python3/bin:$PATH

# 编译安装Python
WORKDIR /tmp
RUN wget --no-check-certificate https://repo.huaweicloud.com/python/$PY_VERSION/Python-$PY_VERSION.tar.xz && \
    tar -Jxvf Python-$PY_VERSION.tar.xz && \
    cd Python-$PY_VERSION && \
    ./configure --prefix=$PYTHON_DIR --with-ssl --enable-shared && \
    make -j$(nproc) && make install && \
    cp $PYTHON_DIR/lib/libpython3.12.so.1.0 /usr/lib64 && \
    ln -sf $PYTHON_DIR/bin/pip3 /usr/bin/pip3 && \
    ln -sf $PYTHON_DIR/bin/python3 /usr/bin/python3 && \
    cd /tmp && \
    rm -rf Python-$PY_VERSION*

# 配置pip
RUN pip3 config set global.index-url http://mirrors.aliyun.com/pypi/simple && \
    pip3 config set install.trusted-host mirrors.aliyun.com && \
    pip3 install --upgrade pip

# 设置工作目录
WORKDIR /app

