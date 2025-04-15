count=1
declare -A GV_ARR_ENV=()

escape_spec_char() {
    local var_value=$1

    var_value="${var_value//\\/\\\\}"
    var_value="${var_value//[$'\n']/}"
    var_value="${var_value//\//\\/}"
    var_value="${var_value//./\\.}"
    var_value="${var_value//\*/\\*}"
    var_value="${var_value//^/\\^}"
    var_value="${var_value//\$/\\\$}"
    var_value="${var_value//\&/\\\&}"
    var_value="${var_value//\[/\\[}"
    var_value="${var_value//\]/\\]}"

    echo "$var_value"
}

while IFS= read -r line_value;
do
    #line_value=$(sed -n "${count}p" ${GV_ENV_SHELL})
    if [[ $line_value =~ ^#.* ]] || [[ $line_value =~ ^$ ]]; then  
        # echo "Skipping comment line: $line_value"  
        continue  
    fi
    #line_value=$(sed -n "${count}p" ${GV_ENV_SHELL})
    key=$(echo ${line_value} | awk -F '=' '{print $1}')
    value=$(echo ${line_value} | awk -F '=' '{print $2}')
    GV_ARR_ENV[${key}]=${value}
    # echo ${GV_ARR_ENV[${key}]}
    #count=$[ ${count} + 1 ]
done < ${GV_ENV_SHELL}
