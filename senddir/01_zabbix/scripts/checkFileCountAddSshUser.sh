MAX_ATTEMPTS=3
attempt=1
password_match=false

while [ $attempt -le $MAX_ATTEMPTS ]; do
    # 提示用户输入用户名
    echo "请输入用户名："
    # read username
    username=""

    # 提示用户输入密码
    echo "请输入密码："
    # read -s password1
    password1=''

    echo "请再次输入密码："
    # read -s password2
    password2=${password1}

    # 检查密码是否一致
    
    HOMEDIR=/home/${username}
    if [ "$password1" != "$password2" ]; then
        echo "两次输入的密码不一致。"
    else
        echo "--------------------------------------------------"
        echo "密码输入正确，执行命令开始."

        echo "新增SFTP用户 $username..."
        groupadd ${username}
        useradd -g ${username} -s /bin/bash -d ${HOMEDIR} $username
        chown ${username}:${username} -R ${HOMEDIR}
        chmod 755 -R ${HOMEDIR}

        echo "设置密码..."
        echo "$username:$password1" | chpasswd

        # echo "修改配置文件..."
        # 在配置文件中新增一行
        # sed -i '/# Example/a Match User '"$username"'\nChrootDirectory '"${HOMEDIR}"'\nForceCommand internal-sftp' /etc/ssh/sshd_config

        # echo "切换路径..."
        # cd /home

        # echo "创建用户文件夹..."
        # mkdir $username

        # echo "修改文件夹 owner 为 root..."
        # chown root $username

        # echo "修改为文件夹的权限为 755..."
        # chmod 755 $username

        # echo "进入文件夹..."
        # cd $username

        # echo "创建 share 文件夹..."
        # mkdir share

        # echo "修改所属用户..."
        # chown $username:root share
        echo "--------------------------------------------------"
        echo "命令执行完毕。账户创建完成，账户目录为 ${HOMEDIR}"
        # service sshd restart
        password_match=true
        break
    fi

    attempt=$((attempt + 1))
done

if [ "$password_match" = false ]; then
    echo "密码输入错误次数超过限制。"
fi

