#/bin/bash
sed -i -e "/listen/d" /etc/nginx/conf.d/nginx.conf
sed -i -e "/server {/a\ \tlisten 8080;\n\tlisten [::]:8080;\n\tlisten 8443 ssl;" /etc/nginx/conf.d/nginx.conf
sed -i -e "/ssl_/d" /etc/nginx/conf.d/nginx.conf
sed -i -e "/if /,+2d" /etc/nginx/conf.d/nginx.conf
sed -i -e "/8443 ssl/a\ \tssl_certificate \"/etc/ssl/nginx/server.pem\";\n\
\tssl_certificate_key \"/etc/ssl/nginx/server.pem\";\n\
\tssl_session_cache shared:SSL:1m;\n\
\tssl_session_timeout  10m;\n\
\tssl_ciphers PROFILE=SYSTEM;\n\
\tssl_prefer_server_ciphers on;\n\
\tif (\$server_port = 8080) {\n\
\t\trewrite ^(\.\*)\$ https://\$host:8443\$1 permanent;\n\
\t}\
" /etc/nginx/conf.d/nginx.conf
